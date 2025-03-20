from dataclasses import dataclass

import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from src import conf
from src.data_loaders import DataLoader, DataMeta


@dataclass(frozen=True)
class StrategyParams:
    X: float
    Y: float
    N: int
    L: int
    S: int
    C: float


class TradingStrategy(ABC):
    def __init__(
        self,
        data_loader: DataLoader,
        futures_a_meta: DataMeta,
        futures_b_meta: DataMeta,
        params: StrategyParams,
    ):
        self.X = params.X  # Standard deviation threshold for buying / maintaining
        self.Y = params.Y  # Standard deviation threshold for selling / maintaining
        self.N = params.N  # Previous days period for standard deviation calculation
        self.L = params.L  # Long position size
        self.S = params.S  # Short position size
        self.C = params.C  # Costs multiplier
        self.data_loader = data_loader
        self.futures_a_meta = futures_a_meta
        self.futures_b_meta = futures_b_meta
        self.futures_a = self.data_loader.load_data(futures_a_meta)
        self.futures_b = self.data_loader.load_data(futures_b_meta)
        self.results = None

    @abstractmethod
    def execute_strategy(self):
        pass

    def plot_results(self):
        if self.results is None:
            raise RuntimeError("Run execute_strategy() first.")

        plt.figure(figsize=(12, 6))
        plt.plot(
            self.results.index,
            self.results["Cumulative_PnL"],
            label="Cumulative PnL",
            color="blue",
        )
        plt.xlabel("Date")
        plt.ylabel("PnL")
        plt.title("Trading Strategy Performance")
        plt.legend()
        plt.show()

    def annualized_return(self):
        if self.results is None:
            raise RuntimeError("Run execute_strategy() first.")

        total_days = (self.results.index[-1] - self.results.index[0]).days
        if total_days == 0 or conf.ANNUAL_TRADING_DAYS == 0:
            return 0.0
        annualized_return = self.results["PnL"].sum() / (
            total_days / conf.ANNUAL_TRADING_DAYS
        )
        print(f"Annualized Return: {annualized_return:.2%}")
        return annualized_return


class MeanReversionStrategy(TradingStrategy):
    def execute_strategy(self):
        df = self.futures_b.copy()
        df["Returns"] = df[self.futures_b_meta.price_col_name].pct_change()
        df["Rolling_Std"] = df["Returns"].rolling(self.N).std()
        df["Signal"] = 0

        df.loc[df["Returns"] < -self.X * df["Rolling_Std"], "Signal"] = self.L
        df.loc[df["Returns"] > self.Y * df["Rolling_Std"], "Signal"] = self.S
        df["Signal"] = df["Signal"].ffill().fillna(0)  # Maintain positions

        df["Trade"] = df["Signal"].diff().fillna(0).abs()
        df["PnL"] = (
            df["Signal"].shift(1)
            * self.futures_a[self.futures_a_meta.price_col_name].pct_change()
        )
        df["PnL"] -= df["Trade"] * self.C  # Apply transaction costs
        df["Cumulative_PnL"] = df["PnL"].cumsum()

        self.results = df
