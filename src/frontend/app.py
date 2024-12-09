# src/frontend/app.py
import streamlit as st
import requests
import json
import re
from utils.chat_interface import initialize_session, display_messages, handle_user_input
import plotly.graph_objects as go

# Backend API base URL
BASE_URL = "http://api-service:8001"

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

        try:
            # Stream the response from the backend as SSE (synchronous generator on backend)
            with requests.post(f"{BASE_URL}/agent/chat/stream", json=payload, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()
                        if decoded_line.startswith("data:"):
                            decoded_line = decoded_line[len("data:"):].strip()
                            data = json.loads(decoded_line)
                            chunk = data.get("content", "")
                            # Update the full response and display incrementally
                            full_response = chunk
                            message_placeholder.markdown(full_response, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            # print the error
            st.error(f"Error communicating with the backend. Please try again later. Error: {e}")
            # st.error("Error communicating with the backend. Please try again later.")
        except json.JSONDecodeError as e:
            st.error("Invalid response format received from backend.")

        # Store the final assistant response in the session
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Extract the hidden instructions from the final response
        plot_match = re.search(
            r"<!--PLOT_INSTRUCTIONS\s*(\{.*?\})\s*PLOT_INSTRUCTIONS-->",
            full_response,
            flags=re.DOTALL
        )

        plot_data = None
        if plot_match:
            try:
                plot_data = json.loads(plot_match.group(1))
            except json.JSONDecodeError:
                plot_data = None

        # Remove the hidden instructions block from the displayed message
        if plot_match:
            cleaned_response = re.sub(
                r"<!--PLOT_INSTRUCTIONS\s*\{.*?\}\s*PLOT_INSTRUCTIONS-->",
                "",
                full_response,
                flags=re.DOTALL
            ).strip()
        else:
            cleaned_response = full_response.strip()

        # Update the displayed message without hidden instructions
        st.session_state.messages[-1]["content"] = cleaned_response
        message_placeholder.markdown(cleaned_response, unsafe_allow_html=True)

       # If we have plot instructions, request the plot data and display it
        if plot_data and "companies" in plot_data:
            companies = plot_data.get("companies", [])
            start_date = plot_data.get("start_date", None)
            end_date = plot_data.get("end_date", None)

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

                    # Flatten the y values in case they are nested lists
                    for trace in fig_json['data']:
                        if isinstance(trace['y'], list) and all(isinstance(item, list) for item in trace['y']):
                            # Choose the first non-null value in each nested list
                            trace['y'] = [next((value for value in item if value is not None), None) for item in trace['y']]

                    # Create the Plotly figure from the JSON data
                    fig = go.Figure(data=fig_json.get("data", []), layout=fig_json.get("layout", {}))

                    # Render the plot using Streamlit
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Failed to fetch plot data from backend.")
