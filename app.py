import streamlit as st
from utils.qa_engine import load_index, ask_question

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Q&A System", layout="wide")

st.title("🤖 AI Question Answering System")

# ---------- LOAD INDEX ----------
if "index" not in st.session_state:
    st.session_state.index = load_index()

if st.session_state.index is None:
    st.error("⚠️ Cannot connect to Qdrant Cloud.")
    st.stop()

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY OLD MESSAGES ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # 🔥 Show sources
        if "sources" in msg and msg["sources"]:
            st.markdown("**Sources:**")
            for s in msg["sources"]:
                st.write(f"📘 {s}")

        # 🔥 Show chunks (collapsible)
        if "chunks" in msg and msg["chunks"]:
            with st.expander("🔍 View Retrieved Chunks"):
                for i, chunk in enumerate(msg["chunks"][:3]):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk[:400])
                    st.markdown("---")

# ---------- USER INPUT ----------
question = st.chat_input("Ask your question...")

if question:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = ask_question(st.session_state.index, question)

            # 🔥 Handle both dict and string safely
            if isinstance(response, dict):
                answer_text = response.get("answer", "")
                sources = response.get("sources", [])
                chunks = response.get("chunks", [])
            else:
                answer_text = response
                sources = []
                chunks = []

            # ---------- DISPLAY ANSWER ----------
            st.markdown("### Answer")
            st.write(answer_text)

            # ---------- DISPLAY SOURCES ----------
            if sources:
                st.markdown("### Sources")
                for s in sources:
                    st.write(f"📘 {s}")

            # ---------- DISPLAY CHUNKS ----------
            if chunks:
                with st.expander("🔍 View Retrieved Chunks"):
                    for i, chunk in enumerate(chunks[:3]):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.write(chunk[:400])
                        st.markdown("---")

    # 🔥 Save full structured response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer_text,
        "sources": sources,
        "chunks": chunks
    })