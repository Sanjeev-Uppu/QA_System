# utils/qa_engine.py

import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from utils.embeddings import get_embedding_model
import google.generativeai as genai

# ---------- Load environment ----------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found")

# ---------- Configure Gemini ----------
genai.configure(api_key=API_KEY)

# Use supported model
MODEL_NAME = "gemini-1.5-flash"


# ---------- Build index ----------
def build_index_from_pdf(pdf_path):
    documents = SimpleDirectoryReader(
        input_files=[pdf_path]
    ).load_data()

    return VectorStoreIndex.from_documents(
        documents,
        embed_model=get_embedding_model()
    )


# ---------- PDF Q&A ----------
def ask_question(index, question):
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(question)

    if not nodes:
        return "I don't know based on the provided document."

    context = "\n\n".join(n.text[:1000] for n in nodes)

    prompt = f"""
Answer ONLY using the context below.
If the answer is not present, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{question}
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------- General chat ----------
def ask_general_question(question):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"