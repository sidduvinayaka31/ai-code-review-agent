<img width="1918" height="1012" alt="Screenshot 2026-07-11 130350" src="https://github.com/user-attachments/assets/d4741673-6133-4f83-846b-97a1e3d16841" />
<img width="1918" height="1017" alt="Screenshot 2026-07-11 130305" src="https://github.com/user-attachments/assets/c6f36d9c-2389-44bf-ad06-bc85209e5dc2" />
<img width="1918" height="1018" alt="Screenshot 2026-07-11 130218" src="https://github.com/user-attachments/assets/ec8aecff-26e0-4d96-859c-a33d17c33077" />
<img width="1918" height="1007" alt="Screenshot 2026-07-11 125916" src="https://github.com/user-attachments/assets/598afd92-76ad-455c-9bd4-e265a56bd110" />
<img width="1918" height="1021" alt="Screenshot 2026-07-11 125815" src="https://github.com/user-attachments/assets/b671ed1d-d15f-46ac-a182-a373a1c981f7" />
<img width="1918" height="1018" alt="Screenshot 2026-07-11 125636" src="https://github.com/user-attachments/assets/e2e028f9-62f7-4b39-a489-145c1f19d1cb" />
# 🛡️ AI Code Review & Security Analysis Agent

Welcome to the **AI Code Review & Security Analysis Agent** developer portal! This project is being built to automatically analyze source code for quality issues, security vulnerabilities, and best practice violations.

Currently, this repository contains the **Milestone 1** implementation, which lays the foundation for our multi-agent architecture.

## ✨ Milestone 1 Features
1. **Interactive UI Module**: A beautifully styled Streamlit frontend allowing users to seamlessly upload `.py` / `.java` files or paste code directly.
2. **Pre-Analysis Syntax Validation**: Uses Python's `ast` and the `javalang` library to catch basic structural errors *before* invoking the AI agents.
3. **Secure Coding Knowledge Base**: Initialized a RAG (Retrieval-Augmented Generation) pipeline using a local **ChromaDB** vector database. It ingests standard coding practices and the OWASP Top 10 vulnerabilities via **Google Gemini Embeddings**, which will later ground our conversational assistant.

## 📸 Screenshots
*(Tip: Once you upload this to GitHub, edit this file and drag-and-drop a screenshot of your running app right here so your mentor can see it!)*

## 🚀 Tech Stack
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **LLM & Embeddings**: Google Gemini (`langchain-google-genai`)
- **Validation Parsing**: built-in `ast` (Python), `javalang` (Java)

## 🛠️ How to Run Locally

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/ai-code-review-agent.git
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
   Rename the `.env.example` file to `.env` and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
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
