import os
from dotenv import load_dotenv
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from document_loader import extract_documents
from vector_store import FAISSVectorStore
from prompt import build_prompt
load_dotenv()

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 5
MODEL_NAME = "all-MiniLM-L6-v2"

def process_documents(uploaded_files):
    pages = extract_documents(uploaded_files)
    if not pages:
        raise ValueError("No readable text was found in the uploaded PDFs.")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for page in pages:
        pieces = splitter.split_text(page["text"])
        for piece in pieces:
            if piece.strip():
                chunks.append({
                    "text": piece.strip(),
                    "metadata": page["metadata"], })
    if not chunks:
        raise ValueError("No text chunks could be created from the uploaded PDFs.")
    store = FAISSVectorStore(model_name=MODEL_NAME)
    store.build(chunks)
    return store

def answer_question(question: str, vector_store: FAISSVectorStore):
    retrieved = vector_store.search(question, top_k=TOP_K)
    if not retrieved:
        return ("I could not find this information in the uploaded documents.",[])
    context_prompt = build_prompt(question, retrieved)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,max_tokens=700,)
    answer = response.choices[0].message.content.strip()
    sources = []
    seen = set()
    for item in retrieved:
        key = (item["metadata"]["document"], item["metadata"]["page"])
        if key not in seen:
            sources.append({
                "document": key[0],
                "page": key[1],
            })
            seen.add(key)
    return answer, sources
