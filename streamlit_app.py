import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


st.title("Finance Bill 2025 Q&A App")

uploaded_file = st.file_uploader("Upload The Finance Bill PDF", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

   
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings)

    retriever = vectorstore.as_retriever()
    llm = Ollama(model="llama3.1")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    query = st.text_input("Ask a question:")

    if query:
        answer = qa.run(query)
        st.subheader("Answer")
        st.write(answer)
