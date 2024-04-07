# Import required libraries
import streamlit as st

st.set_page_config(
   page_title="Chat App",
   page_icon="🤖",
   layout="wide",
   initial_sidebar_state="expanded",
)

# === Begin Main Content === #

# Title
st.title("Chat App Powered by LangChain 🦜🔗")

st.page_link("🏠_Home.py", label="Home", icon="🏠")
st.page_link("pages/1🤖_Chat.py", label="General Knowledge Chat", icon="🤖")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=True)
st.page_link("http://chat.openai.com", label="ChatGPT", icon="🌎")

st.markdown("To interact with the chatbot, an OpenAI API key is required.\
            If you do not have one, clik on the button below to generate your\
            OpenAI API key 👇")
st.link_button(
    "Generate an API key",
    "https://platform.openai.com/api-keys",
    help="Generate an OpenAI API key on https://plateform.openai.com/api-keys"
)

# === End Main Content === #
