import json
import os

import numpy as np
from openai import AzureOpenAI
import streamlit as st

INDEX_PATH = "vector_index.json"


def _get_client():
    return AzureOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_version=st.secrets["AZURE_OPENAI_API_VERSION"],
    )


def _embed(texts):
    client = _get_client()
    response = client.embeddings.create(
        model=st.secrets["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
        input=texts,
    )
    return [item.embedding for item in response.data]


def build_index(chunks):
    texts = [c["text"] for c in chunks]

    all_embeddings = []
    batch_size = 16
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        all_embeddings.extend(_embed(batch))

    index_data = {
        "chunks": chunks,
        "embeddings": all_embeddings,
    }
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_data, f)

    return len(chunks)


def query(question, top_k=5):
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    q_embedding = np.array(_embed([question])[0])
    embeddings = np.array(index_data["embeddings"])

    similarities = embeddings @ q_embedding / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(q_embedding)
    )

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        chunk = index_data["chunks"][idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "section": chunk["section"],
            "score": float(similarities[idx]),
        })
    return results


def index_exists():
    if not os.path.exists(INDEX_PATH):
        return False
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data.get("chunks", [])) > 0
    except Exception:
        return False


def index_count():
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data.get("chunks", []))
    except Exception:
        return 0
