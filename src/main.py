from src import conf
from src.data_loaders import DataMeta, CSVLoader
from src.strategies import MeanReversionStrategy, TradingStrategy, StrategyParams


def main(strategy: TradingStrategy):
    strategy.execute_strategy()
    strategy.plot_results()
    strategy.annualized_return()


if __name__ == "__main__":
    futures_a_meta = DataMeta(
        source=conf.FUTURES_A_SOURCE,
        date_col_name=conf.FUTURES_A_DATE_COLUMN_NAME,
        price_col_name=conf.FUTURES_A_PRICE_COLUMN_NAME,
    )
    futures_b_meta = DataMeta(
        source=conf.FUTURES_B_SOURCE,
        date_col_name=conf.FUTURES_B_DATE_COLUMN_NAME,
        price_col_name=conf.FUTURES_B_PRICE_COLUMN_NAME,
    )

    data_loader = CSVLoader()
    params = StrategyParams(X=conf.X, Y=conf.Y, N=conf.N, L=conf.L, S=conf.S, C=conf.C)
    trading_strategy = MeanReversionStrategy(
        data_loader=data_loader,
        futures_a_meta=futures_a_meta,
        futures_b_meta=futures_b_meta,
        params=params,
    )

    main(trading_strategy)
