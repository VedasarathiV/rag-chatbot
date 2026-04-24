import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
def process_resumes(uploaded_files):
    documents = []

    for i, file in enumerate(uploaded_files):
        file_path = f"temp_{i}.pdf"
        
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        for d in docs:
            d.metadata["source"] = file.name
            d.metadata["candidate_id"] = i

        documents.extend(docs)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def retrieve_candidates(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=5)

    candidates = {}

    for doc in docs:
        cid = doc.metadata["candidate_id"]

        if cid not in candidates:
            candidates[cid] = {
                "source": doc.metadata["source"],
                "content": []
            }

        candidates[cid]["content"].append(doc.page_content)

    return candidates