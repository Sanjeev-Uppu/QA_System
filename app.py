import streamlit as st
import os
from dotenv import load_dotenv
from utils.qa_engine import (
    build_index_from_pdf,
    ask_question,
    ask_general_question
)

load_dotenv()

st.set_page_config(page_title="AI Q&A System", layout="wide")

st.title("🤖 AI Question Answering System")

# ---------------- Sidebar ----------------
st.sidebar.title("Settings")

mode = st.sidebar.radio(
    "Select Mode",
    ["🌍 General AI Q&A", "📄 PDF-based Q&A"]
)

if mode == "📄 PDF-based Q&A":
    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF",
        type="pdf"
    )

    if uploaded_file:
        os.makedirs("data/uploads", exist_ok=True)
        pdf_path = f"data/uploads/{uploaded_file.name}"

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Indexing PDF..."):
            st.session_state.index = build_index_from_pdf(pdf_path)

        st.sidebar.success("PDF indexed successfully!")

# ---------------- Chat State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Chat Input ----------------
question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            if mode == "🌍 General AI Q&A":
                answer = ask_general_question(question)

            else:
                if "index" not in st.session_state:
                    answer = "❌ Please upload a PDF first."
                else:
                    answer = ask_question(
                        st.session_state.index,
                        question
                    )

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )