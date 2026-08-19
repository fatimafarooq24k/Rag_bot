from src.rag import loader, chunker, embedder
from src.storage import store
from pathlib import Path
import logging
import uuid
import json
from datetime import datetime

from src.models.document import DocumentMetadata, ProcessingStatus
from src.storage.paths import get_document_paths

logger = logging.getLogger(__name__)

def index_document(document):

    doc_id = uuid.uuid4()
    upload_time = datetime.now()

    logger.info("Indexing started for document id: %s.", doc_id)

    if not document:
        raise ValueError("Enter a valid document.")

    if not isinstance(document, str):
        raise TypeError("Document path not supported. Must be string")

    filename = Path(document).name

    try:
        pages = loader.extract_text_from_file(document)
    except Exception:
        logger.exception("Text Extraction failed.")
        raise

    logger.info("Text Extraction completed!")

    try:
        all_chunks = []
        for page in pages:
            page_chunks = chunker.chunk_text(page["text"]) 

            for chunk in page_chunks:
                all_chunks.append(
                    {
                        "text" : chunk,
                        "page_number" : page["page_number"]
                    }
                )
    except Exception:
        logger.exception("Document chunking failed.")
        raise

    logger.info("Text chunks created successfully! Total chunks: %d",
    len(all_chunks))
    
    chunk_texts = []

    for chunk in all_chunks:
        chunk_texts.append(chunk["text"])
    try:
        embeddings = embedder.create_embeddings(chunk_texts)
    except Exception:
        logger.exception("Embedding process failed.")
        raise

    logger.info("Text embeddings stage completed successfully!")

    try:
        store.store_data(doc_id, all_chunks, embeddings)
    except Exception as e:
        logger.exception("Document Storage Failed.")
        raise RuntimeError("Error occured while storing the data.") from e

    processing_time = datetime.now()

    metadata = DocumentMetadata(
        doc_id=doc_id,
        filename=filename,
        upload_time=upload_time,
        processing_time=processing_time,
        processing_status=ProcessingStatus.COMPLETED,
        chunks_created=len(all_chunks),
        embeddings_created=len(embeddings) 
    )

    paths = get_document_paths(doc_id)

    try:
        with open(paths.metadata, "w", encoding="utf-8") as file:
            json.dump(
                metadata.model_dump(mode="json"),
                file,
                indent=4
            )
    except Exception:
        logger.exception("Failed to save metadata.")
        raise

    logger.info("Document Indexing Completed Successfully! Doc: %s", doc_id)

    return metadata



