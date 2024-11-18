import pytest
import pandas as pd
from unittest.mock import patch
from agents.tools.stockplotter import StockPlotter


@pytest.fixture
def stock_plotter():
    return StockPlotter()


@patch("agents.tools.stockplotter.yf.download")
@patch("agents.tools.stockplotter.st.plotly_chart")
def test_plot_stock_prices_with_mock_data(mock_plotly_chart, mock_yf_download, stock_plotter):
    # Create mock data for consistent testing
    mock_data = pd.DataFrame({
        "Close": [150, 155, 160],
        "Date": ["2024-06-01", "2024-07-01", "2024-08-01"]
    })
    mock_data.set_index("Date", inplace=True)
    mock_yf_download.return_value = mock_data

    # Explicitly pass the date range to the method
    result = stock_plotter.plot_stock_prices(companies=["AAPL"], start_date="2024-06-01", end_date="2024-08-01")

    # Assertions
    mock_yf_download.assert_called_once_with("AAPL", start="2024-06-01", end="2024-08-01")
    mock_plotly_chart.assert_called_once()
    assert result == "Stock plot displayed successfully"
