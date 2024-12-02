import streamlit as st
import json
import requests
from datetime import datetime, timedelta
from tools.stockplotter import StockPlotter

BASE_URL = "http://api-service:8001"
ENDPOINT = "/agent/chat"

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

        # Define query parameters
        payload = {
            "prompt": conversation_history,
            "stream": True
        }

        try:
            # Send the request
            response = requests.post(BASE_URL + ENDPOINT, json=payload)

            # Check if the request was successful
            if response.status_code == 200:
                response_generator = response.json()["response"]
            else:
                print(f"Failed with status code: {response.status_code}")
                print("Response content:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error occurred:", e)

        instructions_processed = False

        for chunk in response_generator:
            full_response += chunk
            message_placeholder.markdown(full_response)

        try:
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

                instructions_processed = True

                stock_plotter_tool = StockPlotter()
                stock_plotter_tool.plot_stock_prices(companies, start_date, end_date)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            pass

    st.session_state.messages.append({"role": "assistant", "content": full_response})
