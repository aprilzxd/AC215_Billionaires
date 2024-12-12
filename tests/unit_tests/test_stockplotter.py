import pytest
import pandas as pd
from unittest.mock import patch
from tools.stockplotter import StockPlotter

@pytest.fixture
def stock_plotter():
    return StockPlotter()

def test_plot_prices_with_dates(stock_plotter):
    fake_data = pd.DataFrame(
        {"Close": [100, 101, 102]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"])
    )

    with patch("tools.stockplotter.yf.download", return_value=fake_data):
        fig = stock_plotter.plot_stock_prices(["FAKE"], "2024-01-01", "2024-01-03", return_type="figure")
        # Check it's a figure
        assert fig is not None
        assert fig.__class__.__name__ == "Figure"

def test_plot_prices_no_dates(stock_plotter):
    fake_data = pd.DataFrame(
        {"Close": [150, 155]},
        index=pd.to_datetime(["2024-02-01", "2024-02-02"])
    )
    with patch("tools.stockplotter.yf.download", return_value=fake_data):
        fig = stock_plotter.plot_stock_prices(["FAKE"])
        assert fig is not None
        assert fig.__class__.__name__ == "Figure"

def test_plot_prices_error(stock_plotter):
    with patch("tools.stockplotter.yf.download", side_effect=Exception("Network Error")):
        result = stock_plotter.plot_stock_prices(["FAKE"], "2024-03-01", "2024-03-03", return_type="figure")
        assert "Error fetching data for FAKE" in result
