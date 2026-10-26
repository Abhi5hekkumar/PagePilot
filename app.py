
import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from documind.ingestion import load_documents, chunk_documents
from documind.llm import get_llm
from documind.rag import build_retriever, answer_question, summarize_documents

load_dotenv()

st.set_page_config(
    page_title="PagePilot — your document copilot",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --pp-ink:#172033; --pp-muted:#64748b; --pp-blue:#315efb; --pp-line:#e7ebf3; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#f7f9ff 0%,#ffffff 38%); color:var(--pp-ink); }
.block-container { max-width:1180px; padding-top:1.4rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:#f5f7fc; border-right:1px solid var(--pp-line); }
[data-testid="stSidebar"] .block-container { padding-top:1.6rem; }
.pp-brand { display:flex; align-items:center; gap:12px; margin:0 0 1.1rem; }
.pp-mark { width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#315efb,#7c4dff); color:white; font-size:23px; }
.pp-name { font-family:'Manrope',sans-serif; font-size:27px; font-weight:800; letter-spacing:-1.1px; color:#172033; line-height:1.1; }
.pp-tag { color:#64748b; font-size:12px; margin-top:4px; }
.pp-hero { padding:30px 32px; border:1px solid #e5eaff; border-radius:24px; background:radial-gradient(circle at 90% 10%,#e5eaff 0,transparent 34%),linear-gradient(135deg,#ffffff,#f5f7ff); margin-bottom:22px; }
.pp-kicker { color:#315efb; text-transform:uppercase; letter-spacing:1.8px; font-size:11px; font-weight:800; margin-bottom:9px; }
.pp-title { font-family:'Manrope',sans-serif; font-size:clamp(28px,4vw,43px); line-height:1.12; letter-spacing:-1.8px; font-weight:800; margin:0; color:#172033; }
.pp-sub { color:#64748b; font-size:15px; line-height:1.7; max-width:680px; margin-top:12px; }
.pp-chip { display:inline-block; border:1px solid #dbe4ff; background:#fff; color:#40527d; padding:7px 11px; border-radius:999px; font-size:12px; margin:16px 6px 0 0; }
.pp-card { box-sizing:border-box; border:1px solid #e5e7eb; border-radius:16px; background:#fff; padding:26px 25px; min-height:218px; height:100%; box-shadow:0 2px 8px rgba(15,23,42,.035); transition:border-color .18s ease, box-shadow .18s ease, transform .18s ease; }
.pp-card:hover { border-color:#cbd5e1; box-shadow:0 8px 24px rgba(15,23,42,.07); transform:translateY(-2px); }
.pp-card-icon { display:flex; align-items:center; justify-content:center; width:42px; height:42px; border-radius:12px; background:#f1f5f9; color:#334155; font-size:21px; margin-bottom:22px; }
.pp-card-title { font-family:'Manrope',sans-serif; font-weight:750; font-size:17px; line-height:1.35; margin-bottom:10px; color:#111827; letter-spacing:-.35px; }
.pp-card-copy { color:#64748b; font-size:14px; line-height:1.7; }
.pp-note { display:flex; gap:14px; align-items:flex-start; margin:26px 0 34px; padding:18px 20px; border:1px solid #dbeafe; border-radius:14px; background:#f8fbff; color:#334155; font-size:14px; line-height:1.65; }
.pp-note-mark { display:flex; flex-shrink:0; align-items:center; justify-content:center; width:30px; height:30px; border-radius:9px; background:#eaf2ff; color:#1d4ed8; font-weight:800; }
.pp-note strong { color:#1e293b; }
div[data-testid="stFileUploader"] { border:1.5px dashed #c8d3f5; background:#fbfcff; padding:12px; border-radius:16px; }
.stButton button[kind="primary"] { background:linear-gradient(90deg,#315efb,#6548f5); border:0; border-radius:11px; font-weight:700; }
.stButton button { border-radius:10px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--pp-line); }
.stTabs [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:12px 16px; }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--pp-line); border-radius:14px; padding:14px; }
hr { border-color:var(--pp-line); }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# Read credentials from Streamlit Cloud Secrets or local environment.
try:
    cloud_key = st.secrets.get("GROQ_API_KEY", "")
    secret_model = st.secrets.get("GROQ_MODEL", "")
except Exception:
    cloud_key = ""
    secret_model = ""

cloud_key = cloud_key or os.getenv("GROQ_API_KEY", "")
secret_model = secret_model or os.getenv("GROQ_MODEL", "")

with st.sidebar:
    st.markdown(
        '<div class="pp-brand"><div class="pp-mark">✦</div>'
        '<div><div class="pp-name">PagePilot</div>'
        '<div class="pp-tag">Your documents, understood.</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("**AI engine**")

    provider_options = [
        "Groq cloud (free tier)",
        "Ollama on this computer",
    ]
    provider_label = st.radio(
        "Choose how answers are generated",
        provider_options,
        index=0,
        label_visibility="collapsed",
    )
    provider = "groq" if provider_label.startswith("Groq") else "ollama"

    if provider == "groq":
        if cloud_key:
            groq_key = cloud_key
            st.success("Groq API key loaded from app Secrets.")
        else:
            groq_key = st.text_input(
                "Groq API key",
                value="",
                type="password",
                help="Enter your key from console.groq.com. It is used for this session only.",
            )

        st.caption(
            "Free-tier usage limits apply. For a deployed app, configure "
            "GROQ_API_KEY in Streamlit Cloud Secrets."
        )

        default_model = secret_model or "openai/gpt-oss-20b"
        model = st.text_input(
            "Groq model",
            value=default_model,
            help="Default: openai/gpt-oss-20b",
        )
    else:
        groq_key = None
        model = st.text_input(
            "Ollama model",
            value=os.getenv("OLLAMA_MODEL", "llama3.2"),
        )
        st.caption(
            "Ollama must be running on the same computer as this app. "
            "This option generally will not work on a hosted public app."
        )

    st.markdown("---")
    output_language = st.selectbox(
        "Answer language",
        ["English", "Hindi", "Spanish", "French", "German",
         "Portuguese", "Bengali", "Tamil", "Telugu", "Marathi", "Urdu"],
    )
    answer_style = st.selectbox(
        "Answer style",
        ["Crisp", "Detailed", "Beginner-friendly"],
    )
    st.markdown("---")
    st.caption(
        "🔒 Avoid uploading confidential or sensitive documents to a public demo."
    )


st.markdown(
    '<div class="pp-hero"><div class="pp-kicker">Meet your document copilot</div>'
    '<h1 class="pp-title">Less searching.<br>More understanding.</h1>'
    '<div class="pp-sub">Ask questions, turn long reads into clear summaries, '
    'and translate what matters — all from your documents, books, PDFs, and screenshots.</div>'
    '<span class="pp-chip">✦ Document Q&A</span>'
    '<span class="pp-chip">↗ Smart summaries</span>'
    '<span class="pp-chip">文 Multilingual</span>'
    '<span class="pp-chip">▧ OCR-ready</span></div>',
    unsafe_allow_html=True,
)

if "workspace" not in st.session_state:
    st.session_state.workspace = None
if "workspace_key" not in st.session_state:
    st.session_state.workspace_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("### Add your documents")
st.caption(
    "Start with a PDF or a few pages. PagePilot supports common text documents, "
    "ebooks, images, and scanned PDFs."
)
uploads = st.file_uploader(
    "Drop files here or browse",
    type=["pdf", "docx", "txt", "md", "epub", "png", "jpg", "jpeg", "webp", "tif", "tiff"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    help="Supported: PDF, DOCX, TXT, Markdown, EPUB, PNG, JPG, WEBP, TIFF. "
         "OCR is required for scanned pages and images.",
)

if uploads:
    upload_key = tuple(
        (f.name, f.size, hashlib.sha256(f.getvalue()).hexdigest())
        for f in uploads
    )

    if st.session_state.workspace_key != upload_key:
        try:
            with st.spinner("Reading and indexing your files… first run may take a minute."):
                documents = []
                for uploaded in uploads:
                    documents.extend(load_documents(uploaded))

                if not documents:
                    st.error("No readable text was found in these files.")
                    st.stop()

                chunks = chunk_documents(documents)
                llm = get_llm(provider, model, groq_key or None)
                retriever, vectorstore = build_retriever(chunks)

                st.session_state.workspace = {
                    "documents": documents,
                    "chunks": chunks,
                    "retriever": retriever,
                    "vectorstore": vectorstore,
                    "llm": llm,
                    "provider": provider,
                    "model": model,
                    "file_names": [f.name for f in uploads],
                }
                st.session_state.workspace_key = upload_key
                st.session_state.messages = []

            st.success(
                f"Workspace ready · {len(uploads)} file(s) · "
                f"{len(documents)} page/section(s) · {len(chunks)} searchable chunks"
            )
        except Exception as exc:
            message = str(exc)
            if "API key" in message or "GROQ_API_KEY" in message:
                st.error(
                    "Add GROQ_API_KEY in Streamlit Cloud Secrets or enter your "
                    "Groq API key in the sidebar."
                )
            else:
                st.error(f"Could not prepare the documents: {message}")
            st.stop()


if st.session_state.workspace:
    workspace = st.session_state.workspace

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">⌕</div>'
            '<div class="pp-card-title">Ask anything</div>'
            '<div class="pp-card-copy">Get grounded answers with page references.</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">✧</div>'
            '<div class="pp-card-title">Summarize faster</div>'
            '<div class="pp-card-copy">Turn long reads into useful takeaways.</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">文</div>'
            '<div class="pp-card-title">Read your way</div>'
            '<div class="pp-card-copy">Choose a language that works for you.</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    tab_chat, tab_summary, tab_translate = st.tabs(
        ["💬 Ask PagePilot", "✧ Summaries", "文 Translate"]
    )

    with tab_chat:
        for role, content, sources in st.session_state.messages:
            with st.chat_message(role):
                st.markdown(content)
                if role == "assistant" and sources:
                    with st.expander("View sources"):
                        for source in sources:
                            st.markdown(
                                f"- **{source['file']}**, page/section {source['page']}\n\n"
                                f"> {source['excerpt']}"
                            )

        question = st.chat_input("Ask a question about your documents…")
        if question:
            st.session_state.messages.append(("user", question, []))
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Finding relevant passages…"):
                        answer, sources = answer_question(
                            workspace["retriever"],
                            workspace["llm"],
                            question,
                            output_language,
                            answer_style,
                            st.session_state.messages[:-1],
                        )
                    st.markdown(answer)

                    if sources:
                        with st.expander("View sources"):
                            for source in sources:
                                st.markdown(
                                    f"- **{source['file']}**, page/section {source['page']}\n\n"
                                    f"> {source['excerpt']}"
                                )

                    st.session_state.messages.append(("assistant", answer, sources))
                except Exception as exc:
                    st.error(f"Answer generation failed. Check your AI engine. Details: {exc}")

    with tab_summary:
        scope = st.radio(
            "Summarize",
            ["All uploaded files", "One selected file"],
            horizontal=True,
        )
        selected_file = (
            st.selectbox("Choose a file", workspace["file_names"])
            if scope == "One selected file"
            else None
        )
        summary_type = st.selectbox(
            "Summary format",
            ["Short overview", "Chapter/section-wise summary",
             "Key ideas and takeaways", "Study notes"],
        )

        if st.button("Create summary", type="primary"):
            try:
                docs = (
                    workspace["documents"]
                    if not selected_file
                    else [
                        doc for doc in workspace["documents"]
                        if doc.metadata.get("source") == selected_file
                    ]
                )
                with st.spinner("Building a structured summary…"):
                    result = summarize_documents(
                        docs, workspace["llm"], output_language, summary_type
                    )
                st.markdown(result)
                st.download_button(
                    "Download summary (.md)",
                    result,
                    file_name="pagepilot_summary.md",
                )
            except Exception as exc:
                st.error(f"Summary generation failed: {exc}")

    with tab_translate:
        st.caption(
            "Translate extracted text in sections. Output length and fidelity "
            "depend on the model and document size."
        )
        target = st.selectbox(
            "Translate into",
            ["Hindi", "English", "Spanish", "French", "German",
             "Portuguese", "Bengali", "Tamil", "Telugu", "Marathi", "Urdu"],
        )
        selected_file = st.selectbox(
            "Document to translate", workspace["file_names"]
        )

        if st.button("Translate document", type="primary"):
            try:
                docs = [
                    doc for doc in workspace["documents"]
                    if doc.metadata.get("source") == selected_file
                ]
                with st.spinner("Translating sections…"):
                    translated = summarize_documents(
                        docs,
                        workspace["llm"],
                        target,
                        "Translate the provided text faithfully. Preserve headings, "
                        "names, facts, and meaning. Do not summarize or omit content.",
                    )
                st.markdown(translated)
                st.download_button(
                    "Download translation (.md)",
                    translated,
                    file_name="pagepilot_translation.md",
                )
            except Exception as exc:
                st.error(f"Translation failed: {exc}")

else:
    st.markdown("### Built for the way you read")
    st.caption(
        "One workspace for exploring, understanding, and translating your documents."
    )
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">▤</div>'
            '<div class="pp-card-title">From pages to answers</div>'
            '<div class="pp-card-copy">Explore PDFs, Word files, text, Markdown, '
            'EPUB books, and screenshots in one workspace.</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">⌁</div>'
            '<div class="pp-card-title">Evidence, not guesswork</div>'
            '<div class="pp-card-copy">Ask document-specific questions and inspect '
            'the source passages behind an answer.</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="pp-card"><div class="pp-card-icon">文</div>'
            '<div class="pp-card-title">Your language, your pace</div>'
            '<div class="pp-card-copy">Generate summaries and answers in English, '
            'Hindi, and other supported languages.</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="pp-note"><div class="pp-note-mark">i</div><div>'
        '<strong>Choose how PagePilot runs.</strong><br>'
        'For cloud AI, select <strong>Groq cloud</strong>. For local AI, select '
        '<strong>Ollama</strong> and keep Ollama running on this computer. '
        'Free-tier limits may apply.</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "PagePilot · Free, open-source project demo · "
    "AI usage is subject to the selected provider’s free-tier limits."
)
