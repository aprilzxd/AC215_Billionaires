from typing import List
from phi.tools import Toolkit
import yfinance as yf
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

class CorrelationMatrix(Toolkit):
    def __init__(self):
        super().__init__(name="correlation_matrix")
        self.register(self.plot_correlation_matrix)

    def plot_correlation_matrix(self, companies: List[str], start_date: str = None, end_date: str = None) -> str:
        """
        Plots the correlation matrix of stock prices for a list of companies over a given date range.
        
        Args:
            companies (List[str]): List of company stock symbols.
            start_date (str): Start date for the stock data in 'YYYY-MM-DD' format.
            end_date (str): End date for the stock data in 'YYYY-MM-DD' format.
        
        Returns:
            str: Confirmation message after plotting.
        """
        if not start_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

        df_list = []
        for company in companies:
            stock_data = yf.download(company, start=start_date, end=end_date)['Close']
            df_list.append(stock_data)

        df = pd.concat(df_list, axis=1)
        df.columns = companies

        correlation_matrix = df.corr()

        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        st.pyplot(plt)

        return "Correlation matrix displayed successfully"
