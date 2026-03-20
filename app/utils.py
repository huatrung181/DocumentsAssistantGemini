import chromadb
import tempfile
import os
import uuid

from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings

def process_file(file_data, file_type: str = None) -> list:
    if file_type and file_type != "application/pdf":
        raise TypeError("Only PDF files are supported")
    
    if isinstance(file_data, bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_data)
            tmp_file_path = tmp_file.name
        try:
            loader = PDFPlumberLoader(tmp_file_path)
            documents = loader.load()
        finally:
            os.unlink(tmp_file_path)
    else:
        loader = PDFPlumberLoader(file_data)
        documents = loader.load()
    
    for doc in documents:
        doc.page_content = doc.page_content.replace('\n', ' ')
        doc.page_content = ' '.join(doc.page_content.split())
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents)
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"trang_{doc.metadata.get('page', i)}"
    
    if not docs:
        raise ValueError("PDF file parsing failed.")
    return docs



def create_search_engine(file_data, file_type: str = None) -> tuple[VectorStore, list]:
    docs = process_file(file_data, file_type)
    
    encoder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    client = chromadb.EphemeralClient()

    collection_name = f"pdf_chat_{uuid.uuid4().hex}"
    
    search_engine = Chroma.from_documents(
        client=client,
        collection_name=collection_name,
        documents=docs,
        embedding=encoder
    )
    
    return search_engine, docs