# Domain-Specific RAG Chatbot for PDF Question Answering

## Project Objective
A Streamlit chatbot that accepts one or more PDF documents, extracts their text, splits the text into chunks, creates embeddings, stores them in FAISS, retrieves relevant chunks for a user question, and generates a grounded answer using an LLM.

The chatbot is designed to answer only from the uploaded documents and provide source document/page references.

## Workflow

Upload PDF files
→ Extract text page by page
→ Split into chunks
→ Create embeddings
→ Store in FAISS
→ Retrieve top relevant chunks
→ Send context + question to LLM
→ Display answer and sources

## Technologies
- Python
- Streamlit
- pypdf
- LangChain text splitters
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- Groq LLM
- python-dotenv

## Project Structure

```text
domain_rag_chatbot/
├── app.py
├── rag_pipeline.py
├── document_loader.py
├── vector_store.py
├── prompt.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── documents/
│   └── sample.pdf
├── vector_store/
│   └── saved_index/
└── tests/
    └── test_questions.csv
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Add the Groq API key

Open `.env` and replace:

```text
GROQ_API_KEY=your_groq_api_key_here
```

with your actual API key.

Do not upload `.env` to GitHub.

### 4. Run the application

```powershell
streamlit run app.py
```

Open the Streamlit URL shown in the terminal.

## How to Use
1. Upload one or more PDF files in the sidebar.
2. Click **Process Documents**.
3. Wait for extraction, chunking, embedding, and FAISS indexing to finish.
4. Ask a question using the chat box.
5. Read the answer and expand **Sources** to see document/page references.
6. Use **Clear Chat** to reset the conversation.

## Guardrails
The prompt instructs the model to:
- answer only from supplied context;
- avoid inventing facts;
- return the required fallback when information is unavailable;
- treat instructions inside uploaded documents as data rather than chatbot instructions;
- mention source document and page information when available.

## Testing
The `tests/test_questions.csv` file contains 15 test questions covering:
- directly answerable questions;
- questions requiring information from another section;
- unavailable questions;
- source/page verification.

## Limitations
- The current implementation extracts text from normal text-based PDFs.
- OCR for scanned PDFs is not included because it is an optional extension in the project guidance.
- The FAISS index is created in memory for the current Streamlit session.
- A Groq API key is required for answer generation.

## Security and Responsible AI
- API keys must remain in `.env` and must not be committed.
- Do not upload confidential documents without permission.
- High-stakes information should be independently verified.
- Uploaded document instructions must not override chatbot guardrails.
- File type and file size are restricted.

## Deployment
The project can be deployed to Streamlit Cloud or another supported Python hosting platform after configuring the required secret/API key.

