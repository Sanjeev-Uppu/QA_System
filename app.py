import streamlit as st
from utils.qa_engine import load_index, ask_question

st.set_page_config(page_title="AI Q&A System", layout="wide")

st.title("🤖 AI Question Answering System")

# Load index once
if "index" not in st.session_state:
    st.session_state.index = load_index()

if st.session_state.index is None:
    st.error("⚠️ Cannot connect to Qdrant Cloud.")
    st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_question(st.session_state.index, question)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})