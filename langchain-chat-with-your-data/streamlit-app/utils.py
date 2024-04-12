import os
import streamlit as st

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch

# Retrieve the OpenAI API Key, model and temperature
# Model
if "openai_model" in st.session_state:
    model = st.session_state["openai_model"]
else:
    model = "gpt-3.5-turbo"  # Default model: gpt-3.5-turbo

# API key
if "openai_api_key" in st.session_state:
    openai_api_key = st.session_state.openai_api_key

# Temperature
if "openai_temperature" in st.session_state:
    temperature = float(st.session_state.get("openai_temperature"))
else:
    temperature = 0.0

# Chat model
llm = ChatOpenAI(
    model=model,
    temperature=temperature,
    openai_api_key=openai_api_key,
)

# Memory
memory = ConversationBufferMemory()

# Conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # To see what's going under the hood in the terminal
)


def generate_response(user_input):
    """
    Generate a response to the user's input
    """
    # Response: predicted answer
    response = conversation.predict(input=user_input)  # Get response content
    return response


# Display chat messages from history on app rerun
def diplay_messages():
    # Initialize chat history (an empty list if `messages` is not in
    # `st.session_state`)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # `role` is the message author
            st.markdown(message["content"])  # `content` is the message content


def save_pdf(uploaded_file, upload_dir="uploads"):
    """
    Saves a PDF file to the specified directory.

    Args:
        uploaded_file (streamlit.UploadedFile): The uploaded PDF file from st.
        upload_dir (str, optional): Directory to save the uploaded file.
        Defaults to "uploads".
    """
    # Check if 'uploads' directory exists, create it if not
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Get filename from uploaded_file object
    filename = uploaded_file.name

    # Validate if it's a PDF file (optional)
    if not filename.endswith(".pdf"):
        st.error("Only PDF files allowed!")
        return

    # Save the uploaded file with original name
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"""PDF uploaded successfully to: {
        os.path.join(upload_dir, filename)
    }""")

    return file_path


def load_db(file, chain_type, k=3):
    """
    Initialize the database and the retriever chain.

    Args:
        file (file): The PDF document to be loaded.
        chain_type (str): The chain type to use to create the
        'combine_docs_chain' in the CRC.
        k (int): Additional parameter to be passed to the retriever.

    Returns:
        ConversationalRetrievalChain: Initialized CRC.
    """
    # Load the documents
    loader = PyPDFLoader(file)  # Load the PDF file
    documents = loader.load()  # Load into documents

    # Split those documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)

    # Create some embeddings
    embeddings = OpenAIEmbeddings()

    # Put the embeddings in a vectorstore
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)

    # Turn the vectorstore into a retriever
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    # Create a conversational retrieval chain - Chatbot chain
    # (memory is managed externally)
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )  # Memory will be managed externally for the convenience of the GUI
    # i.e. chat history will be managed outside the chain

    return qa


def chatbot_interaction(qa, question, chat_history):
    """Interacts with the chatbot and displays responses."""
    response = qa({"question": question, "chat_history": chat_history})
    return response['answer']
    # if response.get('source_documents'):
    #     st.text("Relevant Documents:")
    #     for doc in response['source_documents']:
    #         st.write(doc)
