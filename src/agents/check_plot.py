from stockplotter import StockPlotter  
from datetime import datetime, timedelta

stock_plotter_tool = StockPlotter()
stock_plotter_tool.plot_stock_prices(["APPL"], (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'))
