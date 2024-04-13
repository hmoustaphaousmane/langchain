import streamlit as st


# @st.cache_data(experimental_allow_widgets=True)
def chat_parameters():
    with st.sidebar.expander("Params", expanded=True):
        # Get user's OpenAI API key
        openai_api_key = st.text_input(
            'OpenAI API Key',
            type='password'
        )
        st.session_state["openai_api_key"] = openai_api_key

        # Set OpenAI model
        openai_model = st.selectbox(
            label="Models",
            options=["gpt-3.5-turbo", "gpt-4"]
        )
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = openai_model

        # Temperature (controls the randomness of the output)
        temperature = st.slider(
            label="Temperatur",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1
        )
        st.session_state["openai_temperature"] = temperature
