import os
import time
import fitz  # PyMuPDF
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SimpleNodeParser
from qdrant_client import QdrantClient

from utils.embeddings import get_embedding_model
from groq import Groq

# -------- LOAD ENV --------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
 

 

# -------- QDRANT CLIENT --------
def get_qdrant_client():
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=120,
        prefer_grpc=False
    )

# -------- PDF EXTRACTION --------
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_documents(folder):
    documents = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)

            text = extract_text_from_pdf(path)

            if not text.strip():
                print(f"⚠️ Empty file skipped: {file}")
                continue

            documents.append(
                Document(
                    text=text,
                    metadata={
                        "chapter": file.replace(".pdf", "")
                    }
                )
            )

            print(f"✅ Loaded: {file} | chars={len(text)}")

    return documents

# -------- GEMINI RETRY --------
# -------- GROQ RETRY --------
def generate_with_retry(prompt):

    models = [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192"
    ]

    for model in models:
        for _ in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                return response.choices[0].message.content

            except Exception as e:
                print(f"⚠️ {model} failed: {e}")
                time.sleep(2)

    return None
# -------- BUILD INDEX --------
def build_index():
    print("📄 Loading PDFs...")

    documents = load_documents("data/pdfs")

    parser = SimpleNodeParser.from_defaults(
        chunk_size=512,
        chunk_overlap=50
    )

    nodes = parser.get_nodes_from_documents(documents)
    print(f"🧩 Nodes: {len(nodes)}")

    qdrant_client = get_qdrant_client()

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="rag_collection"
    )

    storage = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex(
        nodes,
        storage_context=storage,
        embed_model=get_embedding_model()
    )

    print("✅ Index built!")

# -------- LOAD INDEX --------
def load_index():
    try:
        qdrant_client = get_qdrant_client()

        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name="rag_collection"
        )

        return VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=get_embedding_model()
        )

    except Exception as e:
        print("❌ Qdrant connection failed:", e)
        return None

# -------- ASK QUESTION --------
def ask_question(index, question):

    if index is None:
        return {
            "answer": "❌ Qdrant not connected.",
            "sources": [],
            "chunks": []
        }

    retriever = index.as_retriever(similarity_top_k=5) #retriver = search engine
    nodes = retriever.retrieve(question)

    # ❌ No context → fallback
    if not nodes: 
        ext = ask_from_external_knowledge(question)
        return {
            "answer": ext,
            "sources": ["External Knowledge"],
            "chunks": []
        }

    context = "\n\n".join(n.text for n in nodes)

    # ❌ Weak context → fallback
    if len(context.strip()) < 50:
        ext = ask_from_external_knowledge(question)
        return {
            "answer": ext,
            "sources": ["External Knowledge"],
            "chunks": []
        }

    sources = list(set(
        n.metadata.get("chapter")
        for n in nodes
        if n.metadata.get("chapter")
    ))

    prompt = f"""
You are a strict AI assistant.

Answer ONLY using the context below in a proper manner according 
to how question is asked in a structured manner.
Do NOT use external knowledge.

If answer is not clearly present, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate_with_retry(prompt)

    # ❌ Model unsure → fallback
    if not answer or "i don't know" in answer.lower():
        ext = ask_from_external_knowledge(question)
        return {
            "answer": ext,
            "sources": ["External Knowledge"],
            "chunks": []
        }

    # ✅ FINAL RETURN (IMPORTANT)
    return {
        "answer": answer,
        "sources": sources,
        "chunks": [n.text for n in nodes]
    }

# -------- EXTERNAL KNOWLEDGE --------
def ask_from_external_knowledge(question):
    prompt = f"""
Answer the question clearly using general knowledge.

Question:
{question}

Answer:
"""

    answer = generate_with_retry(prompt)

    return answer if answer else "⚠️ API quota exceeded. Please try again later"