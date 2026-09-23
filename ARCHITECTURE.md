# Architecture / Workflow

```text
PDF Uploads
    |
    v
pypdf page extraction + document/page metadata
    |
    v
LangChain text splitter (800 chars, 120 overlap)
    |
    v
Sentence Transformers: all-MiniLM-L6-v2
    |
    v
FAISS vector index
    |
    v
User question -> embedding -> top-5 retrieval
    |
    v
Groq LLM + strict context-only prompt
    |
    v
Answer + source document + page number
```
