from dotenv import load_dotenv
import os

load_dotenv()

DATA_FOLDER = "data"

INDEX_PATH = "data/processed/index.faiss"
CHUNKS_PATH = "data/processed/chunks.pkl"

HNSW_M = 32
HNSW_EF_CONSTRUCTION = 200
# Retriever Configuration

TOP_K = 12

# Reranker Configuration 
RERANK_TOP_K = 6

# Generator Configurations

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None or GROQ_API_KEY == "":
    raise ValueError("No API key found.")

MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.3
MAX_TOKENS = 512
