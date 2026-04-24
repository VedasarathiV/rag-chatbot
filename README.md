# Resume RAG Bot - Documentation

## 1. Project Overview
The **Resume RAG Agent** is a Retrieval-Augmented Generation (RAG) system designed to help HR professionals and recruiters efficiently screen candidates. It allows users to upload multiple PDF resumes, process them into a searchable vector database, and query them using natural language.

## 2. What's Inside the Project
The project consists of the following core components:
- **`app.py`**: The main user interface built with Streamlit. It handles file uploads, user queries, and displays the retrieval results.
- **`rag.py`**: The backend logic for the RAG pipeline. It handles PDF loading, text splitting, embedding generation, and vector storage.
- **`.env`**: Configuration file containing sensitive information like the `OPENAI_API_KEY`.
- **`venv/`**: A virtual environment containing all necessary Python dependencies.
- **`temp_*.pdf`**: Temporary files generated during the resume processing stage.

## 3. How It Works (Architecture)
The application follows a standard RAG architecture optimized for document retrieval:

1.  **Ingestion Phase**:
    *   **Upload**: User uploads PDF resumes via the Streamlit interface.
    *   **Loading**: `PyPDFLoader` extracts text from each PDF.
    *   **Metadata**: Each document is tagged with its source filename and a unique `candidate_id`.
    *   **Splitting**: The text is broken into smaller chunks (700 characters with 100-character overlap) using `RecursiveCharacterTextSplitter`.
2.  **Vectorization Phase**:
    *   **Embeddings**: Each chunk is converted into a numerical vector using the `all-MiniLM-L6-v2` model from HuggingFace (local execution).
    *   **Storage**: These vectors are stored in a **FAISS** (Facebook AI Similarity Search) index for fast similarity lookups.
3.  **Retrieval Phase**:
    *   **Query**: The user enters a natural language query (e.g., "Python developer with 2 years experience").
    *   **Search**: The system converts the query into a vector and finds the top 5 most similar text chunks in the FAISS index.
    *   **Display**: The relevant snippets are grouped by candidate and displayed in the UI.

## 4. Technical Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Framework** | [LangChain](https://www.langchain.com/) |
| **Vector DB** | [FAISS](https://github.com/facebookresearch/faiss) |
| **Embeddings** | [HuggingFace (all-MiniLM-L6-v2)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| **PDF Parsing** | [PyPDF (via LangChain)](https://pypi.org/project/pypdf/) |
| **LLM (Planned)** | OpenAI (via `OPENAI_API_KEY`) |

## 5. What We Did (Implementation Details)
*   **Modular Design**: Separated the UI logic (`app.py`) from the RAG logic (`rag.py`) to make the codebase maintainable.
*   **Local Embeddings**: Chose HuggingFace embeddings for the vectorization step to reduce API costs and improve speed for initial processing.
*   **Multi-Resume Support**: Engineered the system to handle multiple files simultaneously, tracking their source so the user knows which resume they are looking at.
*   **Interactive UI**: Implemented a responsive Streamlit dashboard with progress indicators (spinners) and success messages.

## 6. Current Status & Future Enhancements
> [!NOTE]
> The project currently implements **Retrieval**, but the final **Generation** step (using an LLM to analyze the results and provide scores) is partially set up in the code but not yet active.

### Planned Next Steps:
1.  **LLM Integration**: Connect the `OPENAI_API_KEY` to an LLM chain (e.g., `ChatOpenAI`) to process the retrieval results and generate the "Match Score" and "Short Reason" as defined in the code's prompt template.
2.  **Persistent Storage**: Replace the in-memory FAISS index with a persistent vector store if the number of resumes grows significantly.
3.  **Advanced Filtering**: Add filters for experience level, location, or specific keywords.

---
**Developed by:** Antigravity AI Assistant
**Date:** April 24, 2026
