# Multi-Document RAG PDF Q&A System

A document-based Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents, index them independently, and ask questions specifically from a selected document.

The project combines a **FastAPI backend**, **FAISS vector search**, **sentence-transformer embeddings**, **CrossEncoder reranking**, **Groq LLM inference**, and a **React frontend**.

The system is designed around a multi-document architecture where every uploaded document receives its own unique identifier and its own vector index.

---

## Features

### Document Management

- Upload PDF documents
- Generate a unique `doc_id` for every document
- Store each document independently
- View all uploaded documents
- View individual document metadata
- Delete documents
- Track document processing information

### Document-Specific RAG

- Ask questions from a selected document
- Retrieve relevant chunks using vector similarity
- Rerank retrieved chunks using a CrossEncoder
- Generate answers using an LLM
- Restrict answers to the selected document
- Include page-number citations in generated answers
- Avoid generating information that is not present in the document

### Frontend

The project includes a React-based interface with:

- Document sidebar
- PDF upload interface
- Document selection
- Document deletion
- Chat interface
- Animated UI components
- Loading states
- Empty states
- Error handling

---

## Architecture

The system follows a document-specific RAG pipeline:

```text
                    ┌─────────────────────┐
                    │    React Frontend   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI API      │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
             ▼                                   ▼
      Document Upload                     Document Q&A
             │                                   │
             ▼                                   ▼
      PDF Text Extraction              Query Embedding
             │                                   │
             ▼                                   ▼
          Chunking                       FAISS Retrieval
             │                                   │
             ▼                                   ▼
        Embeddings                       CrossEncoder
             │                              Reranking
             ▼                                   │
       FAISS Index                              ▼
             │                              LLM Generation
             ▼                                   │
    Per-Document Storage                         ▼
                                          Answer + Citations
```

---

## Multi-Document Architecture

Unlike a single-document RAG system, this project does **not** use one global FAISS index.

Every uploaded document receives its own `doc_id`.

Example:

```text
data/
└── processed/
    ├── 7f3a.../
    │   ├── index.faiss
    │   ├── chunks.pkl
    │   └── metadata.json
    │
    └── a91c.../
        ├── index.faiss
        ├── chunks.pkl
        └── metadata.json
```

This allows retrieval to remain isolated to the selected document.

For example:

```text
User selects Document A
        ↓
POST /documents/{document_A_id}/ask
        ↓
Retrieve from Document A's FAISS index
        ↓
Generate answer from Document A
```

Document B is never searched for that request.

---

## Project Structure

```text
Rag_bot/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── DocumentCard.jsx
│   │   │   ├── DocumentList.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   ├── Loading.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── UploadZone.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── ...
│
├── src/
│   ├── api/
│   │   └── ...
│   │
│   ├── core/
│   │   └── ...
│   │
│   ├── models/
│   │   └── ...
│   │
│   ├── rag/
│   │   ├── embedder.py
│   │   ├── generator.py
│   │   └── retriever.py
│   │
│   ├── services/
│   │   └── document_service.py
│   │
│   ├── storage/
│   │   ├── paths.py
│   │   └── store.py
│   │
│   ├── utils/
│   │   └── ...
│   │
│   ├── llm.py
│   ├── main.py
│   └── reranker.py
│
├── tests/
│   └── ...
│
├── data/
│   ├── raw/
│   └── processed/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## RAG Pipeline

### 1. Document Upload

The user uploads a PDF through the frontend.

```http
POST /documents
```

The backend validates the file and starts document processing.

### 2. Document Identification

A unique UUID is generated for every document.

Example:

```text
doc_id:
8d7f3c3e-7f5d-4e7a-b6c1-...
```

### 3. Text Extraction

PDF text is extracted using `pypdf`.

### 4. Chunking

The extracted text is divided into smaller chunks.

Chunks retain metadata such as:

```python
{
    "text": "...",
    "page_number": 12
}
```

This allows the generated answer to reference the original PDF pages.

### 5. Embedding Generation

Each chunk is converted into a numerical vector using a sentence-transformer embedding model.

### 6. Vector Storage

The embeddings are stored in a document-specific FAISS index.

```text
processed/<doc_id>/index.faiss
```

The corresponding chunks are stored separately:

```text
processed/<doc_id>/chunks.pkl
```

### 7. Retrieval

When a user asks a question, the question is converted into an embedding.

FAISS searches the selected document's vector index and retrieves the most relevant chunks.

### 8. Reranking

The initially retrieved chunks are reranked using a CrossEncoder.

This improves the quality of the context passed to the language model.

### 9. LLM Generation

The reranked context is passed to the configured LLM through the Groq API.

The generation prompt instructs the model to:

- Answer only from the provided context
- Avoid inventing information
- Combine relevant chunks
- Mention page numbers
- Clearly indicate when information is unavailable

---

## API Endpoints

### Health

```http
GET /
```

Returns a basic welcome message.

```http
GET /health
```

Returns API health status.

### Documents

**Upload Document**

```http
POST /documents
```

Uploads and indexes a PDF.

**List Documents**

```http
GET /documents
```

Returns metadata for all indexed documents.

**Get Document**

```http
GET /documents/{doc_id}
```

Returns metadata for a specific document.

**Delete Document**

```http
DELETE /documents/{doc_id}
```

Deletes a document and its associated storage.

### Document Q&A

```http
POST /documents/{doc_id}/ask
```

Ask a question specifically from one document.

Example request:

```json
{
    "question": "What are the main ideas discussed in chapter 3?"
}
```

---

## Metadata

Each document maintains metadata such as:

- Filename
- Document ID
- Upload timestamp
- Processing status
- Number of chunks
- Number of embeddings
- Additional processing information

Example:

```json
{
    "filename": "example.pdf",
    "doc_id": "8d7f3c3e-7f5d-4e7a-b6c1-...",
    "processing_status": "completed",
    "number_of_chunks": 1372,
    "number_of_embeddings": 1372
}
```

---

## Technologies

**Backend**
- Python
- FastAPI
- Pydantic
- Uvicorn

**RAG / NLP**
- Sentence Transformers
- CrossEncoder
- FAISS
- NumPy
- pypdf

**LLM**
- Groq API

**Frontend**
- React
- Vite
- JSX
- Framer Motion
- Lucide React

**Testing**
- Pytest

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fatimafarooq24k/Rag_bot.git
cd Rag_bot
```

---

## Backend Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit your actual `.env` file.

---

## Run the Backend

Start FastAPI:

```bash
uvicorn src.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Example Workflow

```text
1. Start FastAPI
        ↓
2. Start React frontend
        ↓
3. Upload PDF
        ↓
4. Backend generates doc_id
        ↓
5. PDF is extracted
        ↓
6. Text is chunked
        ↓
7. Embeddings are generated
        ↓
8. Document-specific FAISS index is created
        ↓
9. Metadata is stored
        ↓
10. User selects document
        ↓
11. User asks a question
        ↓
12. Relevant chunks are retrieved
        ↓
13. Chunks are reranked
        ↓
14. LLM generates answer
        ↓
15. Answer is returned with page citations
```

---

## Current Development Status

### Completed

- [x] PDF document loading
- [x] Text extraction
- [x] Text chunking
- [x] Embedding generation
- [x] FAISS vector storage
- [x] HNSW-based similarity search
- [x] CrossEncoder reranking
- [x] LLM response generation
- [x] Document UUID architecture
- [x] Per-document storage
- [x] Document metadata
- [x] Document listing
- [x] Document retrieval
- [x] Document deletion endpoint
- [x] FastAPI API structure
- [x] React frontend structure
- [x] Document management UI
- [x] Chat interface

### In Progress

- [ ] Complete frontend-backend integration
- [ ] Complete document-specific Q&A integration
- [ ] Propagate `doc_id` through retrieval and generation
- [ ] Final API testing
- [ ] Frontend error handling and polish

### Planned

- [ ] Streaming LLM responses
- [ ] Conversation history
- [ ] Authentication
- [ ] Persistent database for document metadata
- [ ] Background document processing
- [ ] Progress tracking during indexing
- [ ] Support for additional document formats
- [ ] Hybrid keyword + vector retrieval
- [ ] Improved citation handling
- [ ] Docker containerization
- [ ] CI/CD
- [ ] Cloud deployment

---

## Project Goal

The goal of this project is to build a practical, modular, and scalable Retrieval-Augmented Generation system rather than a simple PDF chatbot.

The architecture separates:

- Document processing
- Embedding generation
- Vector retrieval
- Reranking
- LLM generation
- Storage
- API services
- Frontend presentation

This separation makes the system easier to test, maintain, extend, and eventually deploy.

---

## Why Multi-Document RAG?

A traditional PDF chatbot often works with a single global document or vector index.

This project uses an isolated index for every document.

This provides:

- Better document isolation
- More predictable retrieval
- Easier document deletion
- Easier document management
- Independent indexing
- Reduced risk of retrieving information from the wrong document
- A cleaner foundation for future scaling

---

## Author

**Fatima Farooq**

BS Artificial Intelligence

This project is being developed as a hands-on implementation of Retrieval-Augmented Generation, vector search, LLM-based question answering, backend API development, and full-stack AI application development.