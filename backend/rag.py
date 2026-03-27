# backend/rag.py

import os
from typing import Optional, List
from dotenv import load_dotenv

# 🔥 Load env properly
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    DirectoryLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.schema import Document


# ── GLOBAL STATE ─────────────────────────────
vectorstore: Optional[Chroma] = None
retriever = None
_embeddings = None
_llm = None


# ── EMBEDDINGS ─────────────────────────────
def get_embeddings():
    global _embeddings

    if _embeddings is None:
        print("🔄 Loading embeddings...")
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings


# ── LLM ─────────────────────────────
def get_llm():
    global _llm

    if _llm is not None:
        return _llm

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("❌ GROQ_API_KEY not found in .env")

    print("🤖 Loading LLM...")
    _llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key,
        temperature=0.3,
    )

    return _llm


# ── LOAD DOCUMENTS (FIXED) ─────────────────────────
def load_documents(paths: List[str]) -> List[Document]:
    docs = []

    for path in paths:
        if os.path.isdir(path):

            # PDFs
            pdf_loader = DirectoryLoader(
                path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader
            )
            docs.extend(pdf_loader.load())

            # TXTs
            txt_loader = DirectoryLoader(
                path,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            docs.extend(txt_loader.load())

            # DOCX
            docx_loader = DirectoryLoader(
                path,
                glob="**/*.docx",
                loader_cls=Docx2txtLoader
            )
            docs.extend(docx_loader.load())

        elif os.path.isfile(path):
            path_lower = path.lower()

            if path_lower.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path_lower.endswith(".txt"):
                loader = TextLoader(path)
            elif path_lower.endswith(".docx") or path_lower.endswith(".doc"):
                loader = Docx2txtLoader(path)
            else:
                continue

            docs.extend(loader.load())

    print("📄 Total documents loaded:", len(docs))
    return docs


# ── SPLIT ─────────────────────────────
def split_documents(docs: List[Document]):
    print("✂️ Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)
    print("✂️ Total chunks:", len(chunks))

    return chunks


# ── INGEST ─────────────────────
def ingest(paths: List[str]) -> int:
    global vectorstore, retriever

    print("🚀 Starting ingestion...")

    docs = load_documents(paths)

    if not docs:
        raise Exception("❌ No documents loaded")

    chunks = split_documents(docs)
    embeddings = get_embeddings()

    if vectorstore is None:
        print("🆕 Creating new vector DB...")
        vectorstore = Chroma.from_documents(chunks, embedding=embeddings)
    else:
        print("➕ Adding to existing DB...")
        vectorstore.add_documents(chunks)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    print("✅ Ingest complete")
    return len(chunks)


# ── RAG ───────────────────────────────
def corrective_rag(query: str, history=None):
    global retriever

    if history is None:
        history = []

    if retriever is None:
        return {
            "answer": "⚠️ No documents loaded. Please upload first.",
            "sources": []
        }

    print("🔍 Retrieving documents...")
    docs = retriever.invoke(query)

    context = "\n\n".join(d.page_content for d in docs)

    # Conversation history
    history_text = ""
    for h in history[-5:]:
        history_text += f"User: {h.get('question','')}\nAI: {h.get('answer','')}\n\n"

    prompt = f"""
Answer ONLY from context.

Context:
{context}

Conversation:
{history_text}

Question: {query}
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    sources = list(set([
        os.path.basename(d.metadata.get("source", "unknown"))
        for d in docs
    ]))

    return {
        "answer": response.content,
        "sources": sources
    }


# ── PUBLIC FUNCTION (UI CALLS THIS) ─────────────────────────────
def get_answer(query: str, history=None):
    global retriever

    try:
        if retriever is None:
            print("⚡ No DB found. Auto-ingesting...")
            ingest(["documents"])   # 🔥 auto load

        return corrective_rag(query, history)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }


# ── RESET ─────────────────────────────
def reset_session():
    global vectorstore, retriever
    vectorstore = None
    retriever = None
    print("🔄 Session reset complete")