from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import streamlit as st


# Retrieve the OpenAI API Key, model and temperature
model = st.session_state["openai_model"]
openai_api_key = st.session_state.openai_api_key
temperature = st.session_state.openai_temperature,

# Chat model
llm = ChatOpenAI(
    model=model,
    temperature=temperature,
    openai_api_key=openai_api_key,
)

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
        with st.chat_message(message["role"]):  # `role` is the message author
            st.markdown(message["content"])  # `content` is the message content
