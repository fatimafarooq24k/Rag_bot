from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.utils.logging import setup_logging

import logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("PDF Q/A Bot API Initialized.")

app = FastAPI(
    title="PDF Q/A Bot",
    description="Upload PDF and ask questions from it using RAG.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]

)

app.include_router(router)