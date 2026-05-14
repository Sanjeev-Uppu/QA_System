# AI Document Question Answering System (RAG)

This project is an AI-based question answering system that reads PDF documents and answers questions based only on their content. It uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant information and generate accurate responses. If the answer is not present in the documents, it clearly states that.

--------------------------------------------------

## Tech Stack

Python 3.12  
Streamlit  
LlamaIndex  
Qdrant (Vector Database - Cloud)  
sentence-transformers/all-MiniLM-L6-v2  
Google Gemini API  
PyMuPDF  
python-dotenv  

--------------------------------------------------

## Architecture Overview

This project follows a RAG pipeline:

1. Document Ingestion  
   PDF files are loaded and text is extracted using PyMuPDF  

2. Chunking  
   Text is split into smaller chunks  

3. Embedding  
   Each chunk is converted into vectors using MiniLM  

4. Storage  
   Vectors are stored in Qdrant  

5. Retrieval  
   Query is converted to embedding and matched  

6. Generation  
   Retrieved chunks are sent to LLM  

Flow:

User → Query → Embedding → Qdrant → Retrieve Chunks → Context → LLM → Answer  

--------------------------------------------------

## Chunking Strategy

Chunk size: 512  
Overlap: 50  

Reason:  
Maintains context  
Improves retrieval  
Prevents sentence breaking  

--------------------------------------------------

## Embedding Model and Vector Database

Embedding Model:  
sentence-transformers/all-MiniLM-L6-v2  

Reason:  
Fast  
Lightweight  
Good semantic understanding  

Vector Database:  
Qdrant Cloud  

Reason:  
Fast search  
Metadata support  
No local setup  

--------------------------------------------------

## Setup Instructions

Step 1: Clone repo

git clone https://github.com/Sanjeev-Uppu/QA_System.git  
cd QA_System-main  

Step 2: Install dependencies

pip install -r requirements.txt  

Step 3: Create .env file

GOOGLE_API_KEY=your_key  
QDRANT_URL=your_url  
QDRANT_API_KEY=your_key  

Step 4: Add PDFs

Place files inside:

data/pdfs/  

Step 5: Build index

python index.py  

Step 6: Run app

streamlit run app.py  

--------------------------------------------------

## Environment Variables

GOOGLE_API_KEY → Gemini API key  
QDRANT_URL → Qdrant endpoint  
QDRANT_API_KEY → Qdrant key  

Note:  
Do not upload .env file  

--------------------------------------------------

## Example Queries

What is force?  
What are forms of energy?  
What is environment?  
What are states of matter?  
What are human body systems?  

Failure Case:  
What is quantum computing?  

Expected:  
I don't know based on the provided documents  

--------------------------------------------------

## Known Limitations

Depends on API quota  
Accuracy depends on chunking  
Limited to provided documents  
Retrieval may miss context sometimes  

--------------------------------------------------

## Demo Video

https://drive.google.com/file/d/1usE7lYlUcAJ33F6dQEKxgm1IODUVTv9k/view?usp=sharing  

--------------------------------------------------

## Final Note

This project demonstrates a complete RAG pipeline using document ingestion, vector storage, semantic search, and LLM-based answer generation. It is designed to show how AI systems can answer questions from custom data.

```
