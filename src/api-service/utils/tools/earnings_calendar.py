from typing import List, Union
from phi.tools import Toolkit
import yfinance as yf
import pandas as pd

class EarningsTracker(Toolkit):
    def __init__(self):
        super().__init__(name="earnings_tracker")
        self.register(self.get_earnings)

    def get_earnings(self, companies: List[str]) -> Union[str, pd.DataFrame]:
        """
        Fetches the earnings dates for a list of companies.
        
        Args:
            companies (List[str]): List of company stock symbols.
        
        Returns:
            Union[str, pd.DataFrame]: A DataFrame of earnings dates or an error message.
        """
        earnings_data = []

        for company in companies:
            try:
                earnings_df = yf.Ticker(company).earnings_dates
                earnings_df["Company"] = company  # Add company name for context
                earnings_data.append(earnings_df)
            except Exception as e:
                return f"Error fetching earnings for {company}: {e}"

        if not earnings_data:
            return "No earnings data found for the provided companies."

        # Combine all earnings data into a single DataFrame
        df = pd.concat(earnings_data).reset_index()

        return df
