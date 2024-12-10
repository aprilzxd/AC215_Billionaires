import pytest
import pandas as pd
from unittest.mock import patch
from frontend.tools.stockplotter import StockPlotter

# Fixture to initialize the StockPlotter object
@pytest.fixture
def stock_plotter():
    return StockPlotter()

def test_plot_stock_prices_with_mock_data(stock_plotter):
    # Mock yfinance download and Streamlit's plotly_chart within a context
    with patch("frontend.tools.stockplotter.yf.download") as mock_yf_download, \
         patch("frontend.tools.stockplotter.st.plotly_chart") as mock_plotly_chart:
        
        # Create mock data to simulate the downloaded stock prices
        mock_data = pd.DataFrame({
            "Close": [150, 155, 160],
            "Date": ["2024-06-01", "2024-07-01", "2024-08-01"]
        })
        mock_data.set_index("Date", inplace=True)
        mock_yf_download.return_value = mock_data

        # Call the method with explicit date range
        result = stock_plotter.plot_stock_prices(companies=["AAPL"], start_date="2024-06-01", end_date="2024-08-01")

        # Check that yfinance's download method was called with the correct parameters
        mock_yf_download.assert_called_once_with("AAPL", start="2024-06-01", end="2024-08-01")
        
        # Ensure Streamlit's plotly_chart was called
        mock_plotly_chart.assert_called_once()

        # Assert that the method returns the expected result
        assert result == "Stock plot displayed successfully"