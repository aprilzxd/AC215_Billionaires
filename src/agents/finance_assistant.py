import streamlit as st
import json
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from multisend import multisend
from stockplotter import StockPlotter  
from datetime import datetime, timedelta
from prompt import SYSTEM_PROMPT


sender_email = "yananlancelu@gmail.com"
sender_name = "Huandong, April, Lance"
sender_passkey = "neij kvys dupr owqc"
receiver_email = [
    "mingyuan_ma@g.harvard.edu",
    "april_zhang@g.harvard.edu",
    "huandongchang@g.harvard.edu",
    "lance_lu@hms.harvard.edu",
]

stock_plotter_tool = StockPlotter()

assistant = Assistant(
    llm=OpenAIChat(model="gpt-4o-mini", stream=True),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
        stock_plotter_tool,  
        multisend(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
            sender_passkey=sender_passkey,
        ),
    ],
    show_tool_calls=False,
    markdown=True,
    description=SYSTEM_PROMPT  
)

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

        instructions_processed = False

        for chunk in response_generator:
            full_response += chunk
            message_placeholder.markdown(full_response)

        try:
            if not instructions_processed and "companies" in full_response and "start_date" in full_response:
                extracted_data = json.loads(full_response)
                companies = extracted_data.get("companies", ["AAPL", "GOOGL"])
                start_date = extracted_data.get("start_date", (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d'))
                end_date = extracted_data.get("end_date", datetime.today().strftime('%Y-%m-%d'))
                
                instructions_processed = True
                
                stock_plotter_tool.plot_stock_prices(companies, start_date, end_date)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            pass

    st.session_state.messages.append({"role": "assistant", "content": full_response})
