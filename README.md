# AI Document Question Answering System (RAG)

This project is a simple AI system that answers questions based only on given PDF documents.

---

## What this system does

- Reads multiple PDF files  
- Converts text into embeddings  
- Stores data in vector database  
- Retrieves relevant content for a question  
- Generates answer using AI  
- Shows source of answer  

---

## Tech Stack

- Python  
- Streamlit  
- LlamaIndex  
- Qdrant (Vector Database)  
- HuggingFace Embeddings  
- Google Gemini  
- PyMuPDF  

---

## How it works

1. Load PDF documents  
2. Extract text  
3. Split into chunks  
4. Convert into embeddings  
5. Store in Qdrant  
6. User asks question  
7. Retrieve relevant chunks  
8. Generate answer  

---

## Chunking Strategy

- Chunk size: 512  
- Overlap: 50  

---

## Embedding Model

sentence-transformers/all-MiniLM-L6-v2  

---

## Setup Instructions

### Install dependencies


pip install -r requirements.txt


### Add .env file


GOOGLE_API_KEY=your_key
QDRANT_URL=your_url
QDRANT_API_KEY=your_key


### Build index


python index.py


### Run app


streamlit run app.py


---

## Example Queries

- What is force?  
- What are forms of energy?  
- What is environment?  
- What are states of matter?  
- What are human body systems?  

---

## Failure Case

- What is quantum computing?  

Expected output:

I don't know based on the provided documents.

---

## Notes

- Answers are generated only from given documents  
- If answer is not found, system handles it properly  
