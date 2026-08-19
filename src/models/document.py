from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"



class DocumentMetadata(BaseModel):
    doc_id: UUID
    filename: str
    upload_time: datetime
    processing_time: datetime
    processing_status: ProcessingStatus
    chunks_created: int
    embeddings_created: int
