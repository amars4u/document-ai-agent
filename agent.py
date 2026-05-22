import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_version=st.secrets["AZURE_OPENAI_API_VERSION"],
)

def ask(question, documents, chat_history):
    history_text = ""
    for msg in chat_history[:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are a helpful assistant that answers questions strictly 
from the job description documents provided below.

Rules:
- If multiple documents exist and the question is unclear about which job, 
  ask the user to clarify which role they mean.
- Search carefully through ALL sections (Qualifications, Responsibilities, 
  Job description, Benefits) to find relevant information.
- If the answer is truly not in the documents, say 
  "I could not find that in the documents."
- Always mention which company/role your answer is about.

Documents:
{documents}

Previous conversation:
{history_text}

Current question: {question}
"""
    response = client.chat.completions.create(
        model=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.contentscm-history-item:c%3A%5CUsers%5Camarsingh%5Csource%5Crepos%5CMyProjects%5CAIUpskill%5Cdocument-ai-agent?%7B%22repositoryId%22%3A%22scm0%22%2C%22historyItemId%22%3A%22b4570c605fa26b8952eda104dd17a40f3cc8c84b%22%2C%22historyItemParentId%22%3A%22009ee99c78916c8f937bc035fa5b6a9e85172d30%22%2C%22historyItemDisplayId%22%3A%22b4570c6%22%7D