<img width="1918" height="1012" alt="Screenshot 2026-07-11 130350" src="https://github.com/user-attachments/assets/d4741673-6133-4f83-846b-97a1e3d16841" />
<img width="1918" height="1017" alt="Screenshot 2026-07-11 130305" src="https://github.com/user-attachments/assets/c6f36d9c-2389-44bf-ad06-bc85209e5dc2" />
<img width="1918" height="1018" alt="Screenshot 2026-07-11 130218" src="https://github.com/user-attachments/assets/ec8aecff-26e0-4d96-859c-a33d17c33077" />
<img width="1918" height="1007" alt="Screenshot 2026-07-11 125916" src="https://github.com/user-attachments/assets/598afd92-76ad-455c-9bd4-e265a56bd110" />
<img width="1918" height="1021" alt="Screenshot 2026-07-11 125815" src="https://github.com/user-attachments/assets/b671ed1d-d15f-46ac-a182-a373a1c981f7" />
<img width="1918" height="1018" alt="Screenshot 2026-07-11 125636" src="https://github.com/user-attachments/assets/e2e028f9-62f7-4b39-a489-145c1f19d1cb" />

# 🛡️ AI Code Review & Security Analysis Agent

Welcome to the **AI Code Review & Security Analysis Agent** developer portal! This project is being built to automatically analyze source code for quality issues, security vulnerabilities, and best practice violations.

Currently, this repository contains the **Milestone 1 & 2** implementation, featuring a multi-agent architecture powered by LangGraph.

## ✨ Milestone 1 Features
1. **Interactive UI Module**: A beautifully styled Streamlit frontend allowing users to seamlessly upload `.py` / `.java` files or paste code directly.
2. **Pre-Analysis Syntax Validation**: Uses Python's `ast` and the `javalang` library to catch basic structural errors *before* invoking the AI agents.
3. **Secure Coding Knowledge Base**: Initialized a RAG (Retrieval-Augmented Generation) pipeline using a local **ChromaDB** vector database. It ingests standard coding practices and the OWASP Top 10 vulnerabilities via **FastEmbed** embeddings.

## ✨ Milestone 2 Features
1. **Multi-Agent Orchestration**: Implemented **LangGraph** to manage workflow execution, running multiple analysis agents in parallel to drastically reduce wait times.
2. **Code Analysis Agent**: Analyzes code for quality issues such as code smells, high complexity, and design anti-patterns, generating structured feedback.
3. **Security Vulnerability Agent**: Powered by RAG, this agent specifically hunts for OWASP vulnerabilities (e.g., SQL Injection, XSS, Hardcoded Secrets) and provides secure coding recommendations.
4. **Unified Findings Report**: Automatically merges and sorts all findings by severity (High 🔴, Medium 🟡, Low 🔵) in the Streamlit UI.

## 🚀 Tech Stack
- **Frontend**: Streamlit
- **Agent Orchestration**: LangGraph
- **LLM**: Groq (`llama-3.3-70b-versatile` & `llama-3.1-8b-instant`)
- **Vector Database**: ChromaDB
- **Embeddings**: FastEmbed (`BAAI/bge-small-en-v1.5`)
- **Validation Parsing**: built-in `ast` (Python), `javalang` (Java)

## 🛠️ How to Run Locally

### Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sidduvinayaka31/ai-code-review-agent.git
   cd ai-code-review-agent
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

5. **Initialize the Vector Database**
   This script chunks the sample markdown data and stores the embeddings in local ChromaDB.
   ```bash
   python rag/knowledge_base.py
   ```

6. **Run the Application**
   ```bash
   streamlit run app.py
   ```
