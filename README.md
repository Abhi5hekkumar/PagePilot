# PagePilot: AI-Powered PDF Chat Assistant

Upload a PDF and ask questions about it in plain English. PagePilot finds the relevant passages in your document and uses them to generate an answer, instead of relying only on the language model's general knowledge.

Built with **LangChain**, **ChromaDB**, **Mistral AI** and **Streamlit**.

---

## Overview

PagePilot is a Retrieval-Augmented Generation (RAG) application. When a PDF is uploaded, it is split into chunks, converted into vector embeddings and stored in a Chroma vector database. When you ask a question, the most relevant chunks are retrieved and passed to the language model, which writes an answer based on that context.

The project covers the full RAG pipeline: document loading, chunking, embeddings, vector storage, retrieval, prompting and response generation, with a simple web interface on top.

---

## Features

- Upload a PDF and ask questions in natural language
- Answers generated from the retrieved parts of your document
- Semantic search using Mistral embeddings
- Automatic splitting of documents into overlapping chunks
- Max Marginal Relevance (MMR) retrieval, which returns relevant and varied passages
- Chroma vector store created automatically for each uploaded document
- Clean, simple Streamlit interface

---

## Architecture

```text
Upload PDF
    |
    v
PDF loader (PyPDFLoader)
    |
    v
Chunking (RecursiveCharacterTextSplitter)
    |
    v
Embeddings (Mistral)
    |
    v
Vector store (ChromaDB)
    |
    v
MMR retriever  <---  User question
    |
    v
Prompt template (question + retrieved context)
    |
    v
Mistral chat model
    |
    v
Answer
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| LLM and embeddings | Mistral AI |
| Orchestration | LangChain |
| Vector database | ChromaDB |
| Interface | Streamlit |
| PDF loading | PyPDFLoader |
| Chunking | RecursiveCharacterTextSplitter |

---

## Project Structure

```text
PagePilot/
├── ui.py                  # Streamlit app (run this)
├── create_database.py     # Builds the vector database from a PDF
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .gitignore
├── LICENSE
├── README.md
└── screenshots/           # Images used in this README
```

---

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A Mistral AI API key (from the Mistral console)

### 1. Clone the repository

```bash
git clone https://github.com/Abhi5hekkumar/PagePilot.git
cd PagePilot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy `.env.example` to `.env` and add your key:

```env
MISTRAL_API_KEY=your_api_key_here
```

Never commit your real `.env` file.

### 5. Run the app

```bash
streamlit run ui.py
```

Then open http://localhost:8501 in your browser.

---

## How It Works

1. **Upload:** the user uploads a PDF in the Streamlit interface.
2. **Load:** the PDF text is extracted with PyPDFLoader.
3. **Chunk:** the text is split into overlapping chunks with RecursiveCharacterTextSplitter.
4. **Embed:** each chunk is converted into a vector with Mistral embeddings.
5. **Store:** the vectors are saved in ChromaDB.
6. **Retrieve:** for each question, an MMR search selects the most relevant and diverse chunks.
7. **Generate:** the question and the retrieved context are sent to the Mistral chat model, which writes the answer.

---

## Screenshots

![PagePilot interface](screenshots/demo.png)

---

## Limitations

- Works with PDFs that contain selectable text. Scanned PDFs and images of pages are not supported yet (this needs OCR).
- Handles one document at a time.
- Answer quality depends on how well the retrieval step finds the right passages.
- Requires a Mistral API key and an internet connection.

---

## Roadmap

- Support for multiple PDFs and cross-document questions
- Other formats: Word documents, text files and e-books
- Questions from images of pages, using OCR
- Source citations with page numbers
- Conversation memory and streaming responses
- Persistent vector database across sessions
- Hybrid search (keyword + vector)
- Docker and cloud deployment

---

## License

Released under the [MIT License](LICENSE).

---

## Author

**Abhishek Kumar**

- GitHub: [Abhi5hekkumar](https://github.com/Abhi5hekkumar)
- LinkedIn: [Abhishek Kumar](https://www.linkedin.com/in/abhishek-kumar-94888b276)
- Email: kumarabhishek8749@gmail.com
