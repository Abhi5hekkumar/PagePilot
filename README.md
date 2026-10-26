# PagePilot

**Your documents, understood.**

🚀 [**Launch PagePilot Live**](https://pagepilot-ai.streamlit.app/) · 💻 [**View Source Code**](https://github.com/Abhi5hekkumar/PagePilot)

PagePilot is an AI-powered document intelligence application that helps users explore documents, ask questions, generate summaries, and understand content across languages.

## Features

- **Document Q&A:** Ask questions about uploaded documents.
- **Smart Summaries:** Generate concise overviews and structured summaries.
- **Multilingual Responses:** Request answers and summaries in supported languages.
- **Multiple Document Formats:** Work with PDFs, Word documents, text files, Markdown, EPUB books, and supported images.
- **Source-Aware Answers:** Inspect relevant passages used to answer questions.
- **OCR Support:** Extract text from supported scanned documents and images.
- **Flexible AI Providers:** Use Ollama for local inference or a supported cloud AI provider.

## Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **Vector Database:** Chroma
- **Embeddings:** Sentence Transformers
- **AI Providers:** Ollama and optional Groq integration
- **OCR:** Tesseract OCR

## Live Demo

Try PagePilot here:

**[Launch PagePilot](https://pagepilot-ai.streamlit.app/)**

Explore the application by uploading a supported document and using the available tools to understand its content.

## Run Locally

### Prerequisites

- Python 3.10 or a compatible version supported by the project's dependencies
- Git
- An AI provider configured for the features you want to use
- Tesseract OCR, if required for your document-processing workflow

### 1. Clone the repository

```bash
git clone https://github.com/Abhi5hekkumar/PagePilot.git
cd PagePilot
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your AI provider

Follow the configuration requirements of your selected provider. If the project uses environment variables, create a local `.env` file based on `.env.example` and add the required settings.

Never add real API keys or secrets to GitHub.

### 5. Start the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use PagePilot.

## AI Configuration

PagePilot supports local AI through Ollama and may use a supported cloud AI provider when configured.

- **Ollama:** Install Ollama, download a compatible model, and ensure the application can access the local Ollama service.
- **Cloud AI:** Configure the required API key and environment variables using the provider's instructions.
- **Hosted Deployment:** Configure secrets through your hosting platform's settings rather than committing credentials to the repository.

Local Ollama models running on your computer are not automatically accessible to a publicly hosted application.

## Deployment

PagePilot can be deployed on Streamlit Community Cloud or another compatible hosting platform.

General deployment steps:

1. Push the project files to a GitHub repository.
2. Connect the repository to your hosting platform.
3. Select `app.py` as the application entry point.
4. Install the dependencies specified in `requirements.txt`.
5. Configure any required AI-provider credentials through the platform's secrets settings.
6. Deploy the application and test its document-processing and AI features.

Free hosting and AI services may have resource limits, rate limits, availability restrictions, or usage caps.

## Security and Privacy

- Never commit `.env` files, API keys, passwords, or other credentials.
- Avoid uploading confidential or sensitive documents to services without reviewing their privacy policies.
- Use trusted AI providers and understand how uploaded content may be processed.
- Apply appropriate access controls and usage limits before using the application with sensitive information.
- Test the application's security and privacy behaviour before production use.

## Project Status

PagePilot is an evolving project focused on making document understanding simpler and more accessible.

Feature availability depends on the implemented functionality, installed dependencies, AI-provider configuration, and hosting environment. Test the application before relying on it for important documents or production workloads.

## Contributing

Contributions, suggestions, and bug reports are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a branch for your changes.
3. Make and test your updates.
4. Submit a pull request describing your changes.

## License

See the [`LICENSE`](LICENSE) file in this repository for the applicable license terms.

---

**Built with Python, Streamlit, and AI to make document understanding easier.**
