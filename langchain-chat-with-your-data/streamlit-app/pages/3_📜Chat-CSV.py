#pip install streamlit langchain openai faiss-cpu tiktoken

import streamlit as st

from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile

from sidebar import chat_parameters

# Load chat parameters
chat_parameters()

st.title("CSV Chatbot")

chat_history = []

with st.sidebar.expander("CSV file"):
    uploaded_file = st.file_uploader("Upload Your CSV File", type="csv")

if all(key in st.session_state for key in [
    "openai_api_key", "openai_model", "openai_temperature"
    ]
):
    from utils import (
        clear_openai_history, diplay_messages, llm
    )

    diplay_messages()

    openai_api_key = st.session_state.openai_api_key
    if not openai_api_key.startswith('sk-') or uploaded_file == None:
        st.warning('Please enter your OpenAI API Key and upload a CSV file!', icon="⚠️")
    else:

    # Save the uploaded file if it exists
    # if uploaded_file is not None:
        # saved_file = save_pdf(uploaded_file)

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8")
        data = loader.load()

        embeddings = OpenAIEmbeddings()
        vectors = FAISS.from_documents(data, embeddings)        

        crc = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectors.as_retriever()
        )

        # qa = load_db()

        def conversational_chat(query):
            
            result = crc(
                {
                    "question": query,
                    "chat_history": st.session_state['history']
                }
            )
            st.session_state['history'].append((query, result["answer"]))
            
            return result["answer"]
        
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        
        # User input
        if prompt := st.chat_input("Ask a question"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
                print(f"\n\nUser 🙂: {prompt}\n")

            # Add user message to chat history
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                # Get response from langchain
                response = conversational_chat(prompt)
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

if st.sidebar.button("🛑 Clear History"):
    print(f"""🛑 Chat history length befor reset: {
        len(st.session_state.messages)
    }\n""")
    st.session_state["messages"] = []
    print(f"""🛑 Chat history length after reset: {
        len(st.session_state.messages)
    }""")
    clear_openai_history()
