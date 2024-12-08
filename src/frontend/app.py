import streamlit as st
import requests
import json
import re
from utils.chat_interface import initialize_session, display_messages, handle_user_input
import plotly.graph_objects as go

# Backend API base URL
BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="Finance Chatbot",
    page_icon=":moneybag:",
)
st.title("Finance Chatbot")

initialize_session()
display_messages(st.session_state.messages)

if user_input := st.chat_input("Ask about stocks, companies, or financial news..."):
    handle_user_input(user_input)
    payload = {"prompt": user_input}

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        plot_image = None

        try:
            # Stream the response from the backend
            with requests.post(f"{BASE_URL}/agent/chat/stream", json=payload, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()
                        if decoded_line.startswith("data:"):
                            decoded_line = decoded_line[len("data:"):].strip()
                            data = json.loads(decoded_line)
                            chunk = data.get("content", "")
                            # Accumulate the response content
                            full_response = chunk
                            message_placeholder.markdown(full_response)

        except requests.exceptions.RequestException as e:
            st.error("Error communicating with the backend. Please try again later.")
            print(f"Connection error: {e}")
        except json.JSONDecodeError as e:
            st.error("Invalid response format received from backend.")
            print(f"JSONDecodeError: {e}")

        # Append the final assistant response to the session messages
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Attempt to extract plotting instructions from the assistant's final response
        # The LLM should provide a code block with JSON instructions, for example:
        # ```json
        # { "plot": { "companies": [...], "start_date": "...", "end_date": "..." } }
        # ```
        match = re.search(r"```json\s*(\{.*?\})\s*```", full_response, flags=re.DOTALL)
        plot_data = None

        if match:
            try:
                plot_data = json.loads(match.group(1))
            except json.JSONDecodeError:
                plot_data = None

        # If we have a plot instruction, request the plot data from the backend and display it
        if plot_data and "plot" in plot_data:
            companies = plot_data["plot"].get("companies", [])
            start_date = plot_data["plot"].get("start_date", None)
            end_date = plot_data["plot"].get("end_date", None)

            if companies:
                plot_response = requests.get(
                    f"{BASE_URL}/plot_stock_prices",
                    params={
                        "companies": ",".join(companies),
                        "start_date": start_date,
                        "end_date": end_date
                    }
                )

                if plot_response.status_code == 200:
                    fig_json = plot_response.json()
                    fig = go.Figure(fig_json)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Failed to fetch plot data from backend.")
