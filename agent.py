import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_version=st.secrets["AZURE_OPENAI_API_VERSION"],
)

def ask(question, retrieved_chunks, chat_history):
    history_text = ""
    for msg in chat_history[:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    context = ""
    for i, chunk in enumerate(retrieved_chunks, 1):
        context += f"\n--- Chunk {i} [Source: {chunk['source']}, Section: {chunk['section']}] ---\n"
        context += chunk["text"] + "\n"

    prompt = f"""You are a helpful assistant that answers questions strictly
from the document chunks retrieved below.

Rules:
- If multiple documents exist and the question is unclear about which job,
  ask the user to clarify which role they mean.
- Search carefully through ALL retrieved chunks to find relevant information.
- If the answer is truly not in the retrieved chunks, say
  "I could not find that in the documents."
- Always mention which company/role your answer is about.
- Cite the source document when possible.

Retrieved document chunks:
{context}

Previous conversation:
{history_text}

Current question: {question}
"""
    response = client.chat.completions.create(
        model=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content