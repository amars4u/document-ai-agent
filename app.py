import streamlit as st
from loader import load_and_chunk_documents
from vector_store import build_index, query, index_exists, index_count
from agent import ask

st.set_page_config(page_title="Document AI Agent", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; padding: 8px; margin-bottom: 8px; }
    h1 { color: #1a1a2e; font-family: 'Segoe UI', sans-serif; }
    .subtitle { color: #666; font-size: 16px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 📄 Document AI Agent")
st.markdown('<p class="subtitle">Ask questions and get instant answers from your documents (RAG-powered).</p>',
            unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.markdown("### 🗂️ Document Index")
    count = index_count()
    if count > 0:
        st.success(f"✅ Index ready ({count} chunks)")
    else:
        st.warning("⚠️ No index found. Click below to build.")

    if st.button("🔄 Build / Rebuild Index"):
        with st.spinner("Chunking documents and building embeddings..."):
            chunks = load_and_chunk_documents()
            if not chunks:
                st.error("No .docx files found in docs/")
            else:
                num = build_index(chunks)
                st.success(f"Indexed {num} chunks from docs/")
                st.rerun()

if not index_exists():
    st.info("👈 Use the sidebar to build the document index first.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.chat_message(msg["role"], avatar=icon).write(msg["content"])

    question = st.chat_input("💬 Ask a question about your documents...")
    if question:
        st.chat_message("user", avatar="🧑").write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("🔍 Searching documents..."):
            retrieved_chunks = query(question, top_k=5)

        with st.spinner("🤖 Thinking..."):
            answer = ask(question, retrieved_chunks, st.session_state.messages)

        st.chat_message("assistant", avatar="🤖").write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})