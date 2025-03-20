import pytest
import pandas as pd
from src.data_loaders import CSVLoader, DataMeta
from src.strategies import MeanReversionStrategy, StrategyParams


@pytest.fixture
def sample_data():
    futures_a = pd.DataFrame(
        {
            "Date": pd.date_range(start="2025-02-01", periods=10, freq="D"),
            "Price": [100, 101, 99, 98, 97, 100, 102, 104, 103, 105],
        }
    ).set_index("Date")
    futures_b = pd.DataFrame(
        {
            "Date": pd.date_range(start="2025-02-01", periods=10, freq="D"),
            "Price": [50, 51, 49, 48, 50, 52, 51, 53, 55, 54],
        }
    ).set_index("Date")
    return futures_a, futures_b


@pytest.fixture
def mock_csv_loader(mocker, sample_data):
    mock_loader = CSVLoader()
    mocker.patch.object(
        mock_loader,
        "load_data",
        side_effect=lambda file_meta: sample_data[0]
        if file_meta.source == "futures_a.csv"
        else sample_data[1],
    )
    return mock_loader


@pytest.fixture
def strategy(mock_csv_loader):
    futures_a_meta = DataMeta(
        source="futures_a.csv", date_col_name="Date", price_col_name="Price"
    )
    futures_b_meta = DataMeta(
        source="futures_b.csv", date_col_name="Date", price_col_name="Price"
    )
    params = StrategyParams(X=1, Y=1, N=3, L=1, S=-1, C=0.001)
    return MeanReversionStrategy(
        mock_csv_loader, futures_a_meta, futures_b_meta, params
    )


def test_strategy_implementation(strategy):
    strategy.execute_strategy()
    assert strategy.results is not None, "Strategy results should not be None"
    assert "Cumulative_PnL" in strategy.results.columns, (
        "Results should contain Cumulative_PnL"
    )
    assert len(strategy.results) == 10, "Results should match input data length"


def test_annualized_return(strategy):
    strategy.execute_strategy()
    annual_return = strategy.annualized_return()

    expected_return = -0.946  # Based on ANNUAL_TRADING_DAYS = 252
    assert round(annual_return, 3) == round(expected_return, 3), (
        f"Expected {expected_return}, got {annual_return}"
    )
