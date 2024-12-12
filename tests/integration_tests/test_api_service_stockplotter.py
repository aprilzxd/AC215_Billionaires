import pytest
import pandas as pd
from unittest.mock import patch
from tools.stockplotter import StockPlotter

@pytest.fixture
def stock_plotter():
    return StockPlotter()

def test_plot_stock_prices_with_mock_data(stock_plotter):
    mock_data = pd.DataFrame({
        "Close": [150, 155, 160],
        "Date": ["2024-06-01", "2024-07-01", "2024-08-01"]
    })
    mock_data.set_index("Date", inplace=True)

    with patch("tools.stockplotter.yf.download", return_value=mock_data) as mock_yf_download:
        fig = stock_plotter.plot_stock_prices(
            companies=["AAPL"], 
            start_date="2024-06-01", 
            end_date="2024-08-01",
            return_type="figure"
        )

        mock_yf_download.assert_called_once_with("AAPL", start="2024-06-01", end="2024-08-01")
        assert fig is not None
        assert fig.__class__.__name__ == "Figure"
