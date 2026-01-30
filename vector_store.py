from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_vector_store(text, title, url):
    """
    Splits website text into chunks, generates embeddings,
    and stores them persistently in ChromaDB.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    docs = splitter.create_documents(
        [text],
        metadatas=[{"source": url, "title": title}]
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings
    )

    vectordb.add_documents(docs)
    vectordb.persist()

    return vectordb
