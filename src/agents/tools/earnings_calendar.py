from typing import List
from phi.tools import Toolkit
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class EarningsTracker(Toolkit):
    def __init__(self):
        super().__init__(name="earnings_tracker")
        self.register(self.get_earnings)

    def get_earnings(self, companies: List[str]) -> str:
        """
        Fetches and displays the earnings dates for a list of companies.
        
        Args:
            companies (List[str]): List of company stock symbols.
        
        Returns:
            str: Confirmation message after fetching earnings dates.
        """
        earnings_data = []
        for company in companies:
            earnings_df = yf.Ticker(company).earnings_dates
            earnings_data.append(earnings_df)
        
        df = pd.concat(earnings_data)
        st.dataframe(df)
        return "Earnings data fetched successfully"
