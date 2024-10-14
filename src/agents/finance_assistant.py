import streamlit as st
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from multisend import multisend
from prompt import SYSTEM_PROMPT
# please analyze the stock between NVIDIA and APPLE and provide portfolio and send to receiver_emails
sender_email = "yananlancelu@gmail.com"
sender_name = "yuandong, April, Lance"
sender_passkey = "neij kvys dupr owqc"
receiver_email = [
    "mingyuan_ma@g.harvard.edu",
    "april_zhang@g.harvard.edu",
    "huandongchang@g.harvard.edu",
    "lance_lu@hms.harvard.edu",
]

assistant =  Assistant(
        llm=OpenAIChat(model="gpt-4o-mini", stream=True),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
            ),
            multisend(
                receiver_email=receiver_email,
                sender_email=sender_email,
                sender_name=sender_name,
                sender_passkey=sender_passkey,
            ),
        ],
        show_tool_calls=True,
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
        for chunk in response_generator:
            full_response += chunk
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
