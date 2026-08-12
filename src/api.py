from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import logging

from src.generator import generate_answer
from src.index import index_document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title = "PDF Q/A Bot",
    description = "Upload pdf and ask questions from it using RAG.",
    version = "1.0.0"
)

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


class IndexDetails(BaseModel):
    status: str
    chunks_created: int
    embeddings_created: int

class IndexResponse(BaseModel):
    message: str
    details: IndexDetails



@app.get("/")
def home():
    return {"message" : "Welcome! I am PDF Q/A Bot."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
        "/index",
        summary = "Upload a pdf",
        description = "Upload the document so the RAG process and index it.",
        response_model=IndexResponse
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

        logger.info(
            "Starting document indexing %s",
            file_upload.filename
        )
        
        file_path = upload_folder / Path(file_upload.filename).name
        file_data = file_upload.file.read()

        if not file_data:
            raise ValueError("Please enter a pdf first.")

        with open(file_path, "wb") as buffer:
            buffer.write(file_data)

        status = index_document(str(file_path))

        logger.info(
            "Successfully indexed document %s",
            file_upload.filename
        )

        return {
            "message" : "Document Indexed Successfully!",
            "details" : status
            }
    
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


@app.post(
        "/ask",
        summary="Ask a question",
        description="Answer the question from the indexed pdf.",
        response_model=AnswerResponse
        )
def ask_question(request: QuestionRequest):


    try:
        logger.info("Question recieved.")

        answer = generate_answer(request.question)

        logger.info("Question process successfully!")

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


