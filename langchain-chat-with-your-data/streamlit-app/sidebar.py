import streamlit as st


class Sidebar:

    def chat_parameters(self):
        with st.sidebar.expander("Params", expanded=True):
            # Get user's OpenAI API key
            self.openai_api_key = st.text_input(
                'OpenAI API Key',
                type='password'
            )

            # Store the API Key in a file (to avoid circular imports)
            with open('openai_api_key.txt', 'w') as f:
                f.write(self.openai_api_key)

            # Set OpenAI model
            self.openai_model = st.selectbox(
                label="Models",
                options=["gpt-3.5-turbo", "gpt-4"]
            )
            st.session_state["openai_model"] = self.openai_model

            # Temperature (controls the randomness of the output)
            self.temperature = st.slider(
                label="Temperatur",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1
            )
            st.session_state["openai_temperature"] = self.temperature
