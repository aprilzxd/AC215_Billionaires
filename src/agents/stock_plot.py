# under construction!

from phi.assistant import Assistant
from phi.tools.yfinance import YFinanceTools
from phi.llm.openai import OpenAIChat
import yfinance as yf
import matplotlib.pyplot as plt

def plot_stock_prices(symbols, period="1mo"):
    plt.figure(figsize=(12, 6))
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        plt.plot(data.index, data['Close'], label=symbol)
    
    plt.title(f"Stock Prices for {', '.join(symbols)}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.saconvefig("stock_prices.png")
    plt.close()
    return f"Stock price plot for {', '.join(symbols)} has been saved as stock_prices.png"

assistant = Assistant(
    name="Stock Price Plotter",
    llm=OpenAIChat(model="gpt-4-turbo"),
    tools=[
        YFinanceTools(stock_price=True),
        plot_stock_prices
    ],
    show_tool_calls=True,
    description="You are a financial assistant that can plot stock prices.",
    instructions=[
        "Use the YFinanceTools to get stock information if needed.",
        "Use the plot_stock_prices function to create plots.",
        "Always provide the full path to the saved plot image."
    ],
)

assistant.print_response("Plot the stock prices for Nvidia (NVDA) and Apple (AAPL) for the past month.", markdown=True)