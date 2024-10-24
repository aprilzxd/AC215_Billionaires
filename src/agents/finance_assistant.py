# finance_assistant.py
import streamlit as st
import json
from phi.assistant import Assistant
from phi.tools.yfinance import YFinanceTools
from tools.multisend import multisend
from tools.stockplotter import StockPlotter
from tools.portofolio_volatility import PortfolioVolatility
from tools.correlation import CorrelationMatrix
from tools.earnings_calendar import EarningsTracker
from gemini_module import get_gemini_assistant
from datetime import datetime, timedelta
from prompt import SYSTEM_PROMPT

# Configure email and other settings
sender_email = "yananlancelu@gmail.com"
sender_name = "Huandong, April, Lance"
sender_passkey = "neij kvys dupr owqc"
receiver_email = [
    "mingyuan_ma@g.harvard.edu",
    "april_zhang@g.harvard.edu",
    "huandongchang@g.harvard.edu",
    "lance_lu@hms.harvard.edu",
]

# Initialize Assistant Using the Fine-Tuned Gemini Model
fine_tuned_gemini_wrapper = get_gemini_assistant(show_tool_calls=True, debug_mode=True, tool_choice="manual")
assistant = Assistant(
    llm=fine_tuned_gemini_wrapper,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
        StockPlotter(),
        multisend(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
            sender_passkey=sender_passkey,
        ),
        PortfolioVolatility(),
        CorrelationMatrix(),
        EarningsTracker(),
    ],
    description="You are a finance assistant providing market insights.",
   instructions=[
    "For stock-related queries, use YFinanceTools for up-to-date information.",
    "If the user asks to plot stock prices or visualize market trends, use StockPlotter.",
    "For requests to deliver financial information via email, use multisend with the provided contacts.",
    "Analyze financial volatility using PortfolioVolatility and correlations using CorrelationMatrix."],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    add_to_system_prompt=SYSTEM_PROMPT,
)

# Streamlit Code for Interaction
st.title("Finance Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about stocks, company info, or financial news..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation_history = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response_generator = assistant.run(conversation_history, stream=True)

        for chunk in response_generator:
            full_response += chunk
            message_placeholder.markdown(full_response)

        # Check for tool-related tasks
        try:
            instructions_processed = False
            if (
                not instructions_processed
                and "companies" in full_response
                and "start_date" in full_response
            ):
                extracted_data = json.loads(full_response)
                companies = extracted_data.get("companies", ["AAPL", "GOOGL"])
                start_date = extracted_data.get(
                    "start_date",
                    (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d"),
                )
                end_date = extracted_data.get(
                    "end_date", datetime.today().strftime("%Y-%m-%d")
                )

                # Use the StockPlotter tool to plot stock prices
                instructions_processed = True
                stock_plotter_tool = assistant.llm.run_tool("StockPlotter", companies, start_date, end_date)
                stock_plotter_tool.plot_stock_prices(companies, start_date, end_date)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            pass

    st.session_state.messages.append({"role": "assistant", "content": full_response})
