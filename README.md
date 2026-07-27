Project title: RAG Bot

Description:

A Retrieval-Augmented Generation (RAG) chatbot that loads PDF documents, splits them into chunks, generates sentence embeddings, stores them in a FAISS HNSW index, retrieves the most relevant chunks for a query, and generates context-aware responses using a language model.

Features

* Load PDF documents
* Chunk text with overlap
* Generate sentence embeddings
* Store embeddings using FAISS HNSW
* Retrieve relevant chunks
* Generate answers using an LLM
* Unit tested with pytest

Project structure

src/
    loader.py
    chunker.py
    embedder.py
    store.py
    retriever.py
    generator.py
    main.py

tests/
data/

Installation

git clone ...
cd Rag_bot

python -m venv .venv

pip install -r requirements.txt

How to run

python src/main.py

Technologies

* Python
* Sentence Transformers
* FAISS (HNSW)
* NumPy
* PyPDF2
* pytest

RAG Pipeline

PDF
   ↓
Loader
   ↓
Chunker
   ↓
Embedder
   ↓
FAISS Store
   ↓
Retriever
   ↓
Generator
   ↓
Answer

Current status

Loader -> Completed
Chunker -> Completed
Embedder -> Completed
FAISS Storage -> Completed
Retriever -> In Progress
Generator -> In Progress



| Module       | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| loader.py    | Loads PDF documents and extracts text.                                     |
| chunker.py   | Splits text into overlapping chunks while preserving word boundaries.      |
| embedder.py  | Converts text chunks into sentence embeddings using Sentence Transformers. |
| store.py     | Stores and loads embeddings using a FAISS HNSW index.                      |
| retriever.py | Retrieves the most relevant chunks for a query.                            |
| generator.py | Produces the final answer using the retrieved context.                     |

## Approach

```
User uploads a PDF
        ↓
Text is extracted
        ↓
Text is chunked
        ↓
Embeddings are generated
        ↓
Embeddings are stored in FAISS
        ↓
User asks a question
        ↓
Relevant chunks are retrieved
        ↓
Context is sent to the LLM
        ↓
Final response is generated

