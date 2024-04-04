# Import required libraries
import streamlit as st

from utils import generate_response

# === Begin Sidebar === #

with st.sidebar:
    # Get user's OpenAI API key
    openai_api_key = st.text_input('OpenAI API Key', type='password')

# === End Sidebar === #


# === Begin Main Content === #

# Title
st.title("Chat App Powered by LangChain 🦜🔗")

# Set OpenaAI API key from stramlit secrets
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history (an empty list if `messages` is not in `st.session_state`)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # `role` is the message's author
        st.markdown(message["content"])  # `content` is the message content

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API Key!', icon="⚠️")
else:
    # User input
    if prompt := st.chat_input("Ask a question"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            print(f"\n\nUser 🙂: {prompt}\n")
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Get response from langchain
            response = generate_response(prompt, openai_api_key)
            # Chatbot's response
            if response is not None:
                st.write(response)
            else:
                response = "No response available at this time."
                st.write(response)
            print(f"Assistant 🤖: {response}\n")
            

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

# === End Main Content === #
