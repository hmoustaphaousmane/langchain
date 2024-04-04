# Import required libraries
import streamlit as st

# === Begin Main Content === #

# Title
st.title("Chat With Your Data")

# Initialize chat history (an empty list if `messages` is not in `st.session_state`)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # `role` is the message's author
        st.markdown(message["content"])  # `content` is the message content

# User input
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chatbot's response
    response = f"Echo: {prompt}"
    # Display assistant's response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# === End Main Content === #