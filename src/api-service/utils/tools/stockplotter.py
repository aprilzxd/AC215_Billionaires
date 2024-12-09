from typing import List, Union
from phi.tools import Toolkit
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import io
import base64

class StockPlotter(Toolkit):
    def __init__(self):
        super().__init__(name="stock_plotter")
        self.register(self.plot_stock_prices)

    def plot_stock_prices(
        self, 
        companies: List[str], 
        start_date: str = None, 
        end_date: str = None,
        return_type: str = "figure"
    ) -> Union[str, go.Figure]:
        """
        Fetch and plot stock prices for given companies over a date range.

        Args:
            companies (List[str]): List of company stock symbols.
            start_date (str): Start date (YYYY-MM-DD).
            end_date (str): End date (YYYY-MM-DD).
            return_type (str): 'figure' or 'image'.

        Returns:
            go.Figure or str (base64 image).
        """
        # Default to past 3 months if no date range is provided
        if not start_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

        df_list = []
        for company in companies:
            try:
                stock_data = yf.download(company, start=start_date, end=end_date)
                stock_data['Company'] = company
                df_list.append(stock_data)
            except Exception as e:
                return f"Error fetching data for {company}: {e}"

        if not df_list:
            return "No data fetched for the given companies."

        df = pd.concat(df_list)
        fig = go.Figure()

        for company in companies:
            company_data = df[df['Company'] == company]
            fig.add_trace(go.Scatter(
                x=company_data.index,
                y=company_data['Close'],
                mode='lines',
                name=company
            ))

        fig.update_layout(
            title=f"Stock Prices from {start_date} to {end_date}",
            xaxis_title='Date',
            yaxis_title='Stock Price (USD)'
        )

        if return_type == "figure":
            return fig
        elif return_type == "image":
            # Convert the plot to a base64-encoded image
            img_buffer = io.BytesIO()
            fig.write_image(img_buffer, format="png")
            img_buffer.seek(0)
            base64_image = base64.b64encode(img_buffer.read()).decode('utf-8')
            return base64_image
        else:
            return "Invalid return type. Use 'figure' or 'image'."
