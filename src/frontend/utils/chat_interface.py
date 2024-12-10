import streamlit as st

def initialize_session():
    """
    Initializes the session state for chat messages.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_messages(messages):
    """
    Displays chat messages from session state.
    
    Args:
        messages (list): List of message dictionaries with 'role' and 'content'.
    """
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(user_input):
    """
    Handles user input by appending it to session state and displaying it.

    Args:
        user_input (str): The user's input message.
    """
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
