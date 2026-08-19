from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import logging
import json
from uuid import UUID
import shutil

from src.rag.generator import generate_answer
from src.services.document_service import index_document
from src.models.document import DocumentMetadata
from src.core.config import settings
from src.storage.paths import get_document_paths

logger = logging.getLogger(__name__)
router = APIRouter()

class AnswerResponse(BaseModel):
    answer: str

class QuestionRequest(BaseModel):
    question: str = Field(
        min_length = 1,
        description = "Question to ask from pdf")

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        if not value.strip():
            raise ValueError("Please enter you question first.")
        return value.strip()

@router.get("/")
def home():
    return {"message" : "Welcome! I am PDF Q/A Bot."}

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get(
    "/documents",
    summary= "Uploaded Documents",
    description= "List of all the documents uploaded and indexed.",
    response_model = list[DocumentMetadata]
    )
def list_documents():

    processed_folder = Path(settings.processed_folder)
    if not processed_folder.exists():
        logger.warning("No Documents available to show")
        return []
    
    documents = []
    for document_folder in processed_folder.iterdir():

        if not document_folder.is_dir():
            continue

        metadata_path = document_folder / "metadata.json"
        if not metadata_path.is_file():
            logger.warning("Metadata not found for this document. Moving to next.")
            continue

        try:
            with open(metadata_path, "r", encoding="utf-8") as file:
                metadata = json.load(file)
                documents.append(DocumentMetadata(**metadata))

        except Exception:
            logger.exception("Failed to load the document: %s", metadata_path)
            continue

    return documents

@router.get(
        "/documents/{doc_id}",
        summary="Get document details",
        description="Return details of specefic document",
        response_model=DocumentMetadata
)
def get_document(doc_id: UUID):
    paths = get_document_paths(doc_id)

    if not paths.metadata.is_file():
        logger.warning("Metadata not found. Document %s", doc_id)
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    try:
        with open(paths.metadata, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        return DocumentMetadata(**metadata)
    except Exception:
        logger.exception("Failed to load the document: %s", doc_id)

        raise HTTPException(
        status_code=500,
        detail=f"Error occured while loading the infomation of document {doc_id}"
    )




@router.post(
        "/documents",
        summary = "Upload a pdf",
        description = "Upload the document so the RAG process and index it.",
        response_model=DocumentMetadata
)
def index_pdf(file_upload: UploadFile = File(...)):
    try:
        upload_folder = Path("data/raw")
        upload_folder.mkdir(exist_ok = True, parents=True)

        if not file_upload.filename or file_upload.filename.isspace():
            raise ValueError("File name invalid.")

        if not file_upload.filename.lower().endswith(".pdf"):
            raise ValueError("Please enter a pdf.")

        if file_upload.size > 100 * 1024 * 1024:
            raise ValueError("Please enter a pdf smaller than 100MB.")

        logger.info("Starting document indexing...")
        
        file_path = upload_folder / Path(file_upload.filename).name
        file_data = file_upload.file.read()

        if not file_data:
            raise ValueError("Please enter a pdf first.")

        with open(file_path, "wb") as buffer:
            buffer.write(file_data)

        metadata = index_document(str(file_path))

        logger.info(
            "Successfully indexed document %s",
            metadata.doc_id
        )

        return metadata
    
    except FileNotFoundError:
        logger.exception("Required file was not found during indexing.")

        raise HTTPException(
            status_code=500,
            detail="A required file was not found while processing the document."
        )

    except Exception:
        logger.exception("Unexpected error occurred while indexing document.")

        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing the document."
        )

    finally:
        file_upload.file.close()


@router.post(
        "/documents/{doc_id}/ask",
        summary="Ask a question",
        description="Answer the question from the indexed pdf.",
        response_model=AnswerResponse
        )
def ask_question(doc_id: UUID, request: QuestionRequest):


    try:
        logger.info("Question received from document %s.", doc_id)

        paths = get_document_paths(doc_id)

        if not paths.folder.is_dir():
            logger.exception("Requested Document not found.")
            raise HTTPException(
                status_code=500, 
                detail="Requested document not found."
            )

        answer = generate_answer(doc_id, request.question)

        logger.info("Question processed successfully!")

        return {
            "answer" : answer
        }
    
    except FileNotFoundError:
        logger.warning("No indexed document found while processing a question.")

        raise HTTPException(
            status_code=503,
            detail="No indexed document is available. Please upload the document first."
        )

    except Exception:
        logger.exception("Unexpected error occured while processing.")

        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred."
        )

@router.delete(
    "/documents/{doc_id}",
    summary="Dalete document",
    description="Delete the document that is not required."
)
def delete_document(doc_id: UUID):
    paths = get_document_paths(doc_id)

    if not paths.folder.is_dir():
        logger.warning("Folder not found. ID: %s", doc_id)

        raise HTTPException(
            status_code=404,
            detail="Requested document not found."
        )

    try:
        shutil.rmtree(paths.folder)
        logger.info("Document: %s deleted successfully!", doc_id)
        return {
            "message" : "Document deleted successfully!",
            "doc_id" : doc_id
        }

    except Exception:
        logger.exception("Download failed for document %s", doc_id)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete folder."
        )



