from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import streamlit as st

# Retrieve the OpenAI API Key
with open('openai_api_key.txt', 'r') as f:
    openai_api_key = f.read()

# Chat model
llm = ChatOpenAI(
    model=st.session_state.openai_model,
    temperature=st.session_state.openai_temperature,
    openai_api_key=openai_api_key,
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
