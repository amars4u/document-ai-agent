# Document AI Agent

A Streamlit chatbot that answers questions from `.docx` documents using Azure OpenAI.

Drop Word documents into the `docs/` folder and ask questions in a conversational chat interface. The AI answers strictly from your documents and maintains chat history across turns.

## How It Works

1. **loader.py** reads all `.docx` files from `docs/`, extracting text with section headings preserved
2. **agent.py** sends the full document text, conversation history, and your question to Azure OpenAI
3. **app.py** provides the Streamlit chat UI with message history and a clear-chat button

## Setup

### Prerequisites

- Python 3.12+
- An Azure OpenAI deployment (e.g., `gpt-4.1-mini`)

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
AZURE_OPENAI_DEPLOYMENT = "your-deployment-name"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
```

### Run

```bash
streamlit run app.py
```

## Usage

1. Place `.docx` files in the `docs/` folder
2. Start the app and ask questions in the chat input
3. The AI will answer based only on the document contents
4. Use the clear chat button to reset the conversation

## Project Structure

```
app.py                  # Streamlit chat interface
agent.py                # Azure OpenAI integration
loader.py               # Word document text extraction
docs/                   # Drop .docx files here
.streamlit/secrets.toml # Azure OpenAI credentials (not tracked in git)
requirements.txt        # Python dependencies
```
