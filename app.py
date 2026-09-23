import streamlit as st
from rag_pipeline import process_documents, answer_question

st.set_page_config(page_title="Domain-Specific RAG Chatbot", page_icon="📄", layout="wide")

st.title("📄 Domain-Specific RAG Chatbot")
st.caption("Ask questions from your uploaded PDF documents. Answers are grounded only in the uploaded content.")

MAX_FILE_SIZE_MB = 10

if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help=f"Maximum {MAX_FILE_SIZE_MB} MB per file."
    )

    valid_files = []
    if uploaded_files:
        for file in uploaded_files:
            if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"{file.name} exceeds the {MAX_FILE_SIZE_MB} MB limit.")
            else:
                valid_files.append(file)

        st.write("Uploaded files:")
        for file in valid_files:
            st.write(f"• {file.name}")

    if st.button("Process Documents", type="primary", use_container_width=True):
        if not valid_files:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Extracting, chunking, embedding, and indexing documents..."):
                try:
                    st.session_state.vector_store = process_documents(valid_files)
                    st.session_state.uploaded_names = [f.name for f in valid_files]
                    st.session_state.messages = []
                    st.success("Documents processed successfully.")
                except Exception as e:
                    st.error(f"Could not process the documents: {e}")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.uploaded_names:
        st.divider()
        st.caption("Active documents")
        for name in st.session_state.uploaded_names:
            st.write(f"📄 {name}")

if not st.session_state.vector_store:
    st.info("Upload PDF document(s) in the sidebar and click **Process Documents** to begin.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(f"📄 **{source['document']}** — Page {source['page']}")

if prompt := st.chat_input("Ask a question about the uploaded documents..."):
    if not st.session_state.vector_store:
        st.warning("Please process your PDF documents first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                try:
                    answer, sources = answer_question(
                        prompt, st.session_state.vector_store
                    )
                    st.markdown(answer)
                    if sources:
                        with st.expander("Sources"):
                            for source in sources:
                                st.write(
                                    f"📄 **{source['document']}** — Page {source['page']}"
                                )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"Could not answer the question: {e}")