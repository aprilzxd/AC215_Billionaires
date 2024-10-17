from typing import List
from phi.tools import Toolkit
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st


class StockPlotter(Toolkit):
    def __init__(self):
        super().__init__(name="stock_plotter")
        self.register(self.plot_stock_prices)

    def plot_stock_prices(self, companies: List[str], start_date: str = None, end_date: str = None) -> str:
        """
        Plots the stock prices for a list of companies over a given date range.
        
        Args:
            companies (List[str]): List of company stock symbols.
            start_date (str): Start date for the stock data in 'YYYY-MM-DD' format.
            end_date (str): End date for the stock data in 'YYYY-MM-DD' format.
        
        Returns:
            str: Confirmation message after plotting.
        """
        # Default to past 3 months if no date range is provided
        if not start_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

        df_list = []
        for company in companies:
            stock_data = yf.download(company, start=start_date, end=end_date)
            stock_data['Company'] = company  
            df_list.append(stock_data)

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

        st.plotly_chart(fig)
        return "Stock plot displayed successfully"
