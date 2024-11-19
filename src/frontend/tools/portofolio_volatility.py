from typing import List
from phi.tools import Toolkit
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st


class PortfolioVolatility(Toolkit):
    def __init__(self):
        super().__init__(name="portfolio_volatility")
        self.register(self.plot_volatility)

    def plot_volatility(
        self,
        companies: List[str],
        start_date: str = None,
        end_date: str = None,
        kernel_length: int = 10,
        stride: int = 10,
    ) -> str:
        """
        Plots the rolling volatility for a list of companies using kernel_length and stride.

        Args:
            companies (List[str]): List of company stock symbols.
            start_date (str): Start date for the stock data in 'YYYY-MM-DD' format.
            end_date (str): End date for the stock data in 'YYYY-MM-DD' format.
            kernel_length (int): The window length (in days) for calculating volatility.
            stride (int): The step size to move the window (in days).

        Returns:
            str: Confirmation message after plotting.
        """
        if not start_date:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

        fig = go.Figure()

        for company in companies:
            stock_data = yf.download(company, start=start_date, end=end_date)
            stock_data["log_returns"] = np.log(
                stock_data["Close"] / stock_data["Close"].shift(1)
            )

            volatility = []
            dates = []

            for i in range(0, len(stock_data) - kernel_length, stride):
                window_data = stock_data["log_returns"].iloc[i : i + kernel_length]
                vol = np.std(window_data.dropna())
                volatility.append(vol)

                center_date = stock_data.index[i + kernel_length // 2]
                dates.append(center_date)

            fig.add_trace(go.Scatter(x=dates, y=volatility, mode="lines", name=company))

        fig.update_layout(
            title=f"Rolling Volatility ({kernel_length}-day kernel, {stride}-day stride) from {start_date} to {end_date}",
            xaxis_title="Date",
            yaxis_title="Volatility (Standard Deviation)",
            showlegend=True,
        )

        st.plotly_chart(fig)
        return "Volatility plot displayed successfully"
