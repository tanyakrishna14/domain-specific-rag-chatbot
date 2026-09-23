from pathlib import Path
from document_loader import extract_documents

class FakeUpload:
    def __init__(self, path):
        self.name = Path(path).name
        self._data = Path(path).read_bytes()

    def getvalue(self):
        return self._data

def test_sample_pdf_extraction():
    pdf = FakeUpload(Path(__file__).parents[1] / "documents" / "sample.pdf")
    docs = extract_documents([pdf])
    assert docs
    assert all("document" in d["metadata"] for d in docs)
    assert all("page" in d["metadata"] for d in docs)
    assert any("Leave Policy" in d["text"] for d in docs)
