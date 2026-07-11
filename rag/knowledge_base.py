import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = "./chroma_db"
DATA_DIRECTORY = "./data"

def initialize_knowledge_base():
    """Reads markdown files, chunks them, and stores them in ChromaDB."""
    print("Loading documents from data directory...")
    
    # Load all markdown files in the data directory
    loader = DirectoryLoader(DATA_DIRECTORY, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found in the data directory.")
        return None

    print(f"Loaded {len(documents)} documents.")
    
    # Chunk the documents
    text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    print(f"Split into {len(docs)} chunks.")

    # Initialize Gemini Embeddings
    # Requires GOOGLE_API_KEY to be set in environment variables
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print("Initializing ChromaDB and embedding chunks...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("Knowledge base initialized successfully!")
    return vectorstore

def get_retriever():
    """Returns a retriever for querying the knowledge base."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    return vectorstore.as_retriever()

if __name__ == "__main__":
    initialize_knowledge_base()
