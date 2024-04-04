from langchain_openai import ChatOpenAI


def generate_response(user_input, openai_api_key):
    """
    Generate a response to the promt
    """
    llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key, )
    # st.info(llm.invoke(user_input).content)
    response = llm.invoke(user_input).content  # Get response content
    return response
