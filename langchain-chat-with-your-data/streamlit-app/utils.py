from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import streamlit as st

from sidebar import Sidebar

# === Begin Sidebar === #

# Initialize sidebar
sidebar = Sidebar()
sidebar.chat_parameters()

# === End Sidebar === #

# Retrieve the OpenAI API Key
# with open('openai_api_key.txt', 'r') as f:
#     openai_api_key = f.read()

# Chat model
llm = ChatOpenAI(
    model=st.session_state["openai_model"],
    temperature=st.session_state.openai_temperature,
    openai_api_key=st.session_state.openai_api_key,
)
# st.info(llm.invoke(user_input).content)

# Memory
memory = ConversationBufferMemory()

# Conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # To see what's going under the hood in the terminal
)


def generate_response(user_input):
    """
    Generate a response to the user's input
    """
    # Response: predicted answer
    response = conversation.predict(input=user_input)  # Get response content
    return response


# Display chat messages from history on app rerun
def diplay_messages():
    # Initialize chat history (an empty list if `messages` is not in
    # `st.session_state`)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # `role` is the message's author
            st.markdown(message["content"])  # `content` is the message content
