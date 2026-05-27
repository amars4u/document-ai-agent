# Document AI Agent

A Streamlit chatbot that answers questions from `.docx` documents using Retrieval-Augmented Generation (RAG) with Azure OpenAI.

Drop Word documents into the `docs/` folder, build the vector index, and ask questions in a conversational chat interface. The AI retrieves the most relevant document chunks and answers strictly from your documents.

## How It Works

1. **loader.py** reads all `.docx` files from `docs/`, extracting text with section headings preserved and splitting into chunks (~1000 characters with 200-character overlap)
2. **vector_store.py** embeds chunks using Azure OpenAI embeddings, stores them in a local JSON index, and retrieves the top 5 most relevant chunks via cosine similarity
3. **agent.py** sends the retrieved chunks, conversation history, and your question to Azure OpenAI
4. **app.py** provides the Streamlit chat UI with a sidebar to build/rebuild the index

```
docs/ → chunk → embed (Azure OpenAI) → vector_index.json
question → embed → cosine similarity → top 5 chunks → Azure OpenAI → answer
```

## Setup

### Prerequisites

- Python 3.12+
- An Azure OpenAI deployment for chat (e.g., `gpt-4.1-mini`)
- An Azure OpenAI deployment for embeddings (e.g., `text-embedding-ada-002`)

### Install

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Configure

Create `.streamlit/secrets.toml` with your Azure OpenAI credentials:

```toml
AZURE_OPENAI_API_KEY = "your-azure-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT = "your-chat-deployment-name"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "your-embedding-deployment-name"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
```

### Run

```bash
streamlit run app.py
```

## Usage

1. Place `.docx` files in the `docs/` folder
2. Start the app and click **Build / Rebuild Index** in the sidebar
3. Ask questions in the chat input
4. The AI retrieves the most relevant chunks and answers from them
5. Use the clear chat button to reset the conversation

## Project Structure

```
app.py                  # Streamlit chat interface
agent.py                # Azure OpenAI chat integration
loader.py               # Word document text extraction and chunking
vector_store.py         # Embedding, indexing, and similarity search
docs/                   # Drop .docx files here
.streamlit/secrets.toml # Azure OpenAI credentials (not tracked in git)
vector_index.json       # Local vector index (not tracked in git)
requirements.txt        # Python dependencies
```
