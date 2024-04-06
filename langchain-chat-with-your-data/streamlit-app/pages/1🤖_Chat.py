import streamlit as st

from utils import generate_response, diplay_messages, sidebar


# Display history messages
diplay_messages()

# Chat parameters
sidebar.chat_parameters()

openai_api_key = st.session_state.openai_api_key
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
            response = generate_response(prompt)
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
