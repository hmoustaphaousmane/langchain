import streamlit as st

from sidebar import chat_parameters

# Load chat parameters
chat_parameters()

if all(key in st.session_state for key in [
    "openai_api_key", "openai_model", "openai_temperature"
    ]
):
    from utils import generate_response, diplay_messages, clear_openai_history

    # Display history messages
    diplay_messages()

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
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

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

if st.sidebar.button("🛑 Clear History"):
    print(f"""🛑 Chat history length befor reset: {
        len(st.session_state.messages)
    }\n""")
    st.session_state["messages"] = []
    print(f"""🛑 Chat history length after reset: {
        len(st.session_state.messages)
    }""")
    clear_openai_history()
