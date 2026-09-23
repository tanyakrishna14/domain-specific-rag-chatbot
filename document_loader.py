from io import BytesIO
from typing import List, Dict, Any

from pypdf import PdfReader


def extract_documents(uploaded_files) -> List[Dict[str, Any]]:
    """Extract non-empty PDF pages while preserving document and page metadata."""
    documents = []

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.getvalue()
        reader = PdfReader(BytesIO(pdf_bytes))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = " ".join(text.split())

            if not text:
                continue

            documents.append({
                "text": text,
                "metadata": {
                    "document": uploaded_file.name,
                    "page": page_number,
                },
            })

    return documents
