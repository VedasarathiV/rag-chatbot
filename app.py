import os
import streamlit as st
from rag import process_resumes, retrieve_candidates
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume RAG Bot")

st.title("🤖 Resume RAG Agent")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Process Resumes"):
        with st.spinner("Processing resumes..."):
            st.session_state.vs = process_resumes(uploaded_files)
        st.success("✅ Resumes processed!")

if "vs" in st.session_state:
    query = st.text_input("Ask something (e.g., Python dev with 2 years exp)")

    if query:
        candidates = retrieve_candidates(st.session_state.vs, query)


        st.subheader("🎯 Results")

        for cid, data in candidates.items():
            context = "\n".join(data["content"])

            prompt = f"""
            You are an HR assistant.

            Query:
            {query}

            Candidate Resume:
            {context}

            Give:
            - Match score (out of 100)
            - Skills
            - Experience
            - Short reason
            """

            st.write("Relevant Resume Content:")

            st.markdown(f"### 📄 {data['source']}")
            st.write(context[:1000])
            st.write("---")