import torch
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores  import FAISS
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplate import css, bot_template, user_template


torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

API_BASE = "http://grace.bldev.infoprint.com:8100/v1/"
API_KEY = "EMPTY" 

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_chunk_text(text):
    splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    return splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(text_chunks,embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(
        model="neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8",
        openai_api_base=API_BASE,
        openai_api_key=API_KEY
    )#Ollama(model="llama3.2")
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain


def handle_user_input(user_query):
    response = st.session_state.conversation({'question':user_query})
    st.session_state.chat_history = response['chat_history']

    for i,message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
    


def main():
    # This enables the app to use the variables in the .env file
    load_dotenv()

    st.set_page_config(page_title="Retrieving from Documents", page_icon=":balls:")

    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chathistory" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Retrieving from Documents")

    user_query = st.text_input("How can I help you?....")
    if user_query:
        handle_user_input(user_query)
    st.write(user_template.replace("{{MSG}}","Hey Smart Bot!!"),unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}","Hello!!"),unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Documents")
        pdf_docs = st.file_uploader("Upload the PDFs here",accept_multiple_files=True)
        if st.button("Upload"):
            # When pressed
            with st.spinner("Reading the documents...."):    
                # upload the documents to the vector store
                # get the pdf
                raw_text = get_pdf_text(pdf_docs)
                
                # get the text chunks from the pdf
                text_chunks = get_chunk_text(raw_text)
                
                # Create vector store from the embeddings
                vector_store = get_vector_store(text_chunks)

                # creating instance of conversation chain
                st.session_state.conversation = get_conversation_chain(vector_store)

    return None
if __name__ == "__main__":
    main()