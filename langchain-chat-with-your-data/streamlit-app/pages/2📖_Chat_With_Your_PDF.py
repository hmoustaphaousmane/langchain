import streamlit as st

from sidebar import chat_parameters, clear_history

# Load chat parameters
chat_parameters()

st.title("PDF Chatbot")

chat_history = []

with st.sidebar.expander("PDF file"):
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

clear_history()

if all(key in st.session_state for key in [
    "openai_api_key", "openai_model", "openai_temperature"
    ]
):
    from utils import (
        chatbot_interaction, diplay_messages, generate_response, load_db,
        save_pdf
    )

    # Save the uploaded file if it exists
    if uploaded_file is not None:
        saved_file = save_pdf(uploaded_file)

    # Display history messages
    diplay_messages()

    openai_api_key = st.session_state.openai_api_key
    if not openai_api_key.startswith('sk-') or uploaded_file == None:
        st.warning('Please enter your OpenAI API Key and upload a PDF file!', icon="⚠️")
    else:
        if saved_file is not None:
            # Load the PDF and initialize the chatbot
            qa = load_db(saved_file, "stuff", 3)  # Adjust chain_type and k as needed

            # # Get user question
            # user_question = st.text_input("Ask your question:")

            # if user_question:
            #     chatbot_interaction(qa, user_question)
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
                response = chatbot_interaction(qa, prompt, chat_history)
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
  