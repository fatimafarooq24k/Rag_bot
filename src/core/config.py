from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    data_folder: str = "data"

    raw_folder: str = "data/raw"
    processed_folder: str = "data/processed"

    hnsw_m: int = 132
    hnsw_ef_construction: int = 200
    hnsw_ef_search: int = 128

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    top_k: int = 12

    rerank_top_k: int = 6
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    groq_api_key: str

    model: str = "openai/gpt-oss-20b"
    temperature: float = 0.4
    max_tokens: int = 4096

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"    
    )

settings = Settings()