from typing import List, Union
from phi.tools import Toolkit
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64

class CorrelationMatrix(Toolkit):
    def __init__(self):
        super().__init__(name="correlation_matrix")
        self.register(self.plot_correlation_matrix)

    def plot_correlation_matrix(
        self, 
        companies: List[str], 
        start_date: str = None, 
        end_date: str = None, 
        return_type: str = "image"
    ) -> Union[str, plt.Figure, str]:
        """
        Plots the correlation matrix of stock prices.

        Args:
            companies (List[str]): List of company stock symbols.
            start_date (str): Start date for the stock data in 'YYYY-MM-DD' format.
            end_date (str): End date for the stock data in 'YYYY-MM-DD' format.
            return_type (str): "figure" for a Matplotlib figure or "image" for base64-encoded PNG.

        Returns:
            Union[str, plt.Figure]: A Matplotlib figure, Base64-encoded image, or error message.
        """
        if not start_date:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d")

        df_list = []
        for company in companies:
            try:
                stock_data = yf.download(company, start=start_date, end=end_date)["Close"]
                df_list.append(stock_data)
            except Exception as e:
                return f"Error fetching data for {company}: {e}"

        if not df_list:
            return "No data fetched for the given companies."

        df = pd.concat(df_list, axis=1)
        df.columns = companies

        correlation_matrix = df.corr()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
        plt.title(f"Correlation Matrix ({start_date} to {end_date})")

        if return_type == "figure":
            return fig
        elif return_type == "image":
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="png", bbox_inches="tight")
            img_buffer.seek(0)
            base64_image = base64.b64encode(img_buffer.read()).decode("utf-8")
            plt.close(fig)
            return base64_image
        else:
            plt.close(fig)
            return "Invalid return type. Use 'figure' or 'image'."
