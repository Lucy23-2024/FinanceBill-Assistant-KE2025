# FinanceBill-Assistant-KE2025
A bilingual (English/Kiswahili) RAG assistant for the Kenya 2025 Finance Bill

# Finance Bill RAG Assistant

**A Retrieval-Augmented Generation (RAG) assistant that answers questions from a Finance Bill PDF (English & Swahili).**

---

## Table of contents

* [What is this project?](#what-is-this-project)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setup — step by step (beginner-friendly)](#setup--step-by-step-beginner-friendly)
* [Project structure](#project-structure)
* [How to run (notebook)](#how-to-run-notebook)
* [How to run (Streamlit app)](#how-to-run-streamlit-app)
* [How it works (simple explanation)](#how-it-works-simple-explanation)
* [Key settings to tune (and why)](#key-settings-to-tune-and-why)
* [Debugging tips](#debugging-tips)
* [Prompts used in this project](#prompts-used-in-this-project)
* [Examples & expected behavior](#examples--expected-behavior)
* [Troubleshooting](#troubleshooting)
* [Next steps / Enhancements](#next-steps--enhancements)
* [License & contact](#license--contact)

---

## What is this project?

This repository demonstrates a **beginner-friendly** Retrieval-Augmented Generation (RAG) workflow that:

* loads a Finance Bill PDF,
* splits it into searchable chunks,
* creates embeddings and stores them in a vector database,
* retrieves relevant chunks for a user question,
* answers the question using an LLM and custom prompts.

It’s aimed at learners who are new to LangChain, vector search, and practical RAG setups.

---

## Features

* Load PDFs (Finance Bill) and extract text.
* Split long documents into smaller chunks for better retrieval.
* Create embeddings and persist a vector store (Chroma by default).
* Custom Query + Answer prompts (keeps language consistent — English/Swahili).
* A Jupyter notebook for exploration and a Streamlit app for end-user interaction.

---

## Prerequisites

* **Python 3.12** (use `python --version` to check)
* `git` (optional, for cloning)
* Basic command-line knowledge (open a terminal)
* Optional: account/API key for your chosen LLM (OpenAI) or a local LLM (Ollama)

---

## Setup — step by step (beginner-friendly)

1. **Clone the repo** (or make a local folder and copy files):

```bash
# replace <your-repo-url> with your repo link, or skip if working locally
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Create & activate a virtual environment** (recommended):

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

3. **Install dependencies**

* If your repo includes `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

* Or install directly (matches the notebook):

```bash
pip install langchain langchain-core langchain-community langchain-ollama langchain-text-splitters chromadb pypdf streamlit
```

4. **Place the Finance Bill PDF**

* Put your PDF in a `data/` folder, e.g. `data/finance_bill_2025.pdf`.
* Update any file path variables in `finance_rag.ipynb` or `streamlit_app.py` if needed.

5. **Set LLM credentials (if using a hosted model like OpenAI)**

```bash
# example for OpenAI
export OPENAI_API_KEY="sk-..."
# On Windows PowerShell
setx OPENAI_API_KEY "sk-..."
```

* If you use Ollama or another local server, configure environment variables.

---

## Project structure

```
finance_rag/                 # root (example)
├─ finance_rag.ipynb         # main notebook (development & experiments)
├─ prompts.py                # query & answer PromptTemplate objects
├─ streamlit_app.py          # Streamlit app to run the RAG interactively
├─ data/                     # put PDFs here
│  └─ finance_bill_2025.pdf
├─ README.md                 # this file
└─ requirements.txt          # (optional) pinned dependencies
```

---

## How to run (notebook)

1. Launch Jupyter:

```bash
jupyter notebook
# or
jupyter lab
```

2. Open `finance_rag.ipynb`.
3. Run cells **top to bottom**. Key steps include:

   * Installing dependencies (if you didn’t already).
   * Loading the PDF with `PyPDFLoader`.
   * Splitting text with `RecursiveCharacterTextSplitter`.
   * Creating embeddings & persisting vector store (Chroma default).
   * Creating a retriever and QA chain.

> Tip: run the `loader.load()` and inspect `data[0].page_content` before splitting to verify text extraction worked.

---

## How to run (Streamlit app)

1. Ensure your virtual environment is active and dependencies installed.
2. Run:

```bash
streamlit run streamlit_app.py
```

3. Open the local URL printed in the terminal (usually `http://localhost:8501`).
4. In the app you can type a question (English or Swahili) and the app will display the RAG answer. Make sure the vector store (or the PDF path) is configured as expected in `streamlit_app.py`.

---

## How it works (simple explanation)

1. **Loader** — reads the PDF and extracts text.
2. **Splitter** — chops the long text into small chunks (e.g., 800–1000 chars) so the retriever can match precisely.
3. **Embeddings** — each chunk is converted into a vector using an embedding model.
4. **Vector store** — vectors are stored in a database (Chroma) for similarity search.
5. **Retriever** — when a user asks a question, the retriever returns the `k` most similar chunks.
6. **QA Chain** — an LLM consumes the retrieved context and the prompt template to produce the final answer.

---

## Key settings to tune (and why)

* **Chunk size / overlap**: for legal docs, try `chunk_size=800-1200` and `chunk_overlap=100`. Smaller chunks increase precision; larger chunks keep more context.
* **Retriever `k`**: how many chunks to return. Start with 4–8 (try `k=6`). Larger `k` shows more sections but increases token usage.
* **Embedding model**: different models produce different nearest neighbors. Keep the model consistent across indexing and querying.

Example tweak:

```python
retriever = db.as_retriever(search_kwargs={"k": 6})
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
```

---


## Prompts used in this project

The project separates the prompts into `prompts.py` (query optimization + answer prompt). The idea:

* **QUERY\_PROMPT**: rewrites or optimizes the user question to improve retrieval.
* **ANSWER\_PROMPT**: instructs the LLM to answer *only* from the provided context and to reply in the same language as the question.

This separation helps the system find the right chunks and then produce a concise, grounded answer.

---

## Examples & expected behavior

**Example:**

```python
# ask_rag is a helper that performs retrieval + answer
ask_rag("What Taxes does the document address?")
```

* You may see short answers (e.g., `Income Tax, VAT`) or a longer list depending on how many chunks were retrieved. If you want more complete results, increase `k` and/or reduce chunk size.

**Why two people get different answers**: differences usually come from the retrieval step (chunking, `k`, embeddings). To make results consistent, standardize indexing settings and embedding model.

---

## Troubleshooting (common issues)

* **Model returns "I don't know"**: the retriever didn't find relevant chunks; increase `k` or re-index with smaller chunk size.
* **PDF text extraction is empty or garbled**: try another loader (OCR) or clean the PDF.
* **Different users get different results**: ensure the vector DB is the same (same embeddings & persisted store) and retriever settings are identical.

---

