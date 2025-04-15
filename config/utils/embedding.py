from typing import List
from pypdf import PdfReader
from config.settings import model

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def get_embeddings(text: str) -> List[float]:
    """Generate embeddings for text using Gemini."""
    try:
        embeddings = model.embed_documents(text)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")