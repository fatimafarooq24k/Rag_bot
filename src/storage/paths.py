from pathlib import Path
from dataclasses import dataclass

from src.core.config import settings


@dataclass
class DocumentPaths:
    folder: Path
    index: Path
    chunks: Path
    metadata: Path

def get_document_paths(doc_id):
    folder = Path(settings.processed_folder) / str(doc_id)
    return DocumentPaths(
        folder=folder,
        index=folder / "index.faiss",
        chunks=folder / "chunks.pkl",
        metadata = folder / "metadata.json"
    )