# PagePilot

**Your documents, understood.**

PagePilot is an AI-powered document intelligence application that helps users explore documents, ask questions, generate summaries, and understand content across languages.

## Features

- **Document Q&A:** Ask questions about uploaded documents.
- **Smart summaries:** Generate concise overviews and structured summaries.
- **Multilingual responses:** Request answers and summaries in supported languages.
- **Document support:** Work with PDFs, Word documents, text, Markdown, EPUB books, and supported images.
- **Source-aware answers:** Inspect relevant passages used to answer questions.
- **Flexible AI providers:** Use Ollama for local inference or a supported cloud provider.

## Technology Stack

- Python
- Streamlit
- LangChain
- Chroma vector database
- Sentence Transformers
- Ollama and optional Groq integration
- Tesseract OCR for supported scanned documents and images

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd pagepilot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

## AI Configuration

PagePilot supports local AI through Ollama and can use a supported cloud AI provider when configured.

- **Ollama:** Install Ollama and download a compatible model.
- **Cloud AI:** Configure the required API key through environment variables or your deployment platform's secrets settings.

Never commit API keys, passwords, or private documents to GitHub.

## Deployment

PagePilot is designed for deployment on Streamlit Community Cloud or another compatible hosting platform.

Deployment requires a public GitHub repository, a valid application entry point, compatible dependencies, and appropriate AI-provider configuration.

Free hosting and AI services may have resource limits, rate limits, or usage restrictions. Local Ollama models running on a developer's computer are not automatically accessible to a publicly hosted application.

## Security and Privacy

- Do not commit `.env` files or API credentials.
- Avoid uploading confidential or sensitive documents to services without reviewing their privacy policies.
- Configure appropriate limits before making the application publicly accessible.

## Project Status

PagePilot is an evolving project. Features and deployment compatibility should be tested before relying on the application for important documents or production workloads.

## License

See the `LICENSE` file for the applicable license terms.
