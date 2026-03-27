import os
import shutil
import uuid

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Folder Setup
DATA_DIR = "data"
DB_DIR = "chroma_db"

os.makedirs(DATA_DIR, exist_ok=True)
# Startup Cleanup
def clear_old_database():
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
        print("Old database cleared.")
# Load Documents
def load_documents():
    print("Loading documents...")

    pdf_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader

    )

    text_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader
    )

    documents = []
    documents.extend(pdf_loader.load())
    documents.extend(text_loader.load())

    if not documents:
        raise ValueError("No documents found in the data directory.")

    print(f"Loaded {len(documents)} documents.")
    return documents
# Metadata Cleaning
def clean_metadata(documents):
    for doc in documents:
        doc.metadata = {
            "source": str(doc.metadata.get("source", "unknown"))
        }
    return documents
# Chunking
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )

    splits = splitter.split_documents(documents)
    print(f"{len(splits)} chunks created.")
    return splits
# Create Vector Database
def create_vector_db(splits):
    print("Generating embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    collection_name = f"rag_collection_{uuid.uuid4()}"

    vector_db = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name=collection_name
    )

    vector_db.persist()
if __name__ == "__main__":
    print("Starting RAG document processing...")

    clear_old_database()

    documents = load_documents()
    documents = clean_metadata(documents)

    splits = chunk_documents(documents)

    create_vector_db(splits)

    print("Vector database created successfully!")