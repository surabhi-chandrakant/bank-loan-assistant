# 🏦 Bank of Maharashtra – Loan Product Assistant (RAG System)

This repository contains my submission for the **Generative AI Developer Technical Assessment** at **EncureIT Systems Pvt Ltd**.

The goal of this project is to build a **Retrieval-Augmented Generation (RAG)** pipeline that answers user queries related to the **Bank of Maharashtra (BOM) loan products**.  
It includes:

- Automated **scraping** of BOM’s loan-related pages  
- **Cleaned & consolidated** loan text dataset  
- **FAISS vector store**  
- **SentenceTransformer embeddings**  
- **Groq LLM (llama-3.3-70b-versatile)**  
- **Streamlit UI** for interacting with the assistant  

# Live Demo app : https://bank-loan-assistant-rag.streamlit.app/

---

# 📂 Project Structure

```
bank-loan-assistant/
│
├── data/
│   ├── raw_loans.txt
│   ├── clean_loans.txt
│
├── vectorstore/
│   ├── faiss.index
│   ├── chunks.pkl
│
├── scraper.py
├── clean_data.py
├── build_vector_store.py
├── rag_app.py
├── streamlit_app.py
│
├── requirements.txt
├── README.md
└── .env (ignored)
```

---
##  Clone the Repository
git clone https://github.com/surabhi-chandrakant/bank-loan-assistant.git
cd bank-loan-assistant

##  Create a Virtual Environment (Recommended)
Windows
python -m venv venv
venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate


# ⚙️ Project Setup

## 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 2️⃣ Add Groq API Key  
Create a `.env` file in project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

or set it temporarily:

```bash
$env:GROQ_API_KEY="your_groq_api_key_here"
```

---

## 3️⃣ Run the Scraper
```bash
python scraper.py
```

---

## 4️⃣ Clean Data
```bash
python clean_data.py
```

---

## 5️⃣ Build Vector Store
```bash
python build_vector_store.py
```

---

## 6️⃣ Run Streamlit UI
```bash
streamlit run streamlit_app.py
```

---

# 🧠 Architectural Decisions

## 1. Scraping Strategy
- Used `requests` + `BeautifulSoup`  
- Extracted headings, content blocks, paragraphs, list items  
- Removed scripts, navigation, ads  
- Covered all major loan pages  

---

## 2. Data Processing
- Normalized whitespace  
- Removed duplicates  
- Cleaned noisy HTML-derived text  

---

## 3. Chunking Strategy
- Section-aware chunking (~450–700 chars)  
- Chosen to maintain semantic meaning  
- Higher accuracy in FAISS retrieval  

---

## 4. Vector Search (FAISS)
- FAISS CPU index for cosine similarity  
- Lightweight & extremely fast  
- Uses embedding normalization + similarity filtering  

---

## 5. Embedding Model
- `all-MiniLM-L6-v2`  
- Fast, accurate, CPU-friendly  

---

## 6. LLM Choice
- **Groq `llama-3.3-70b-versatile`**  
- High reasoning quality  
- Very fast inference  
- Free tier available  

---

## 7. AI Tools Used
| Tool | Purpose |
|------|---------|
| Groq API | High-speed LLM inference |
| SentenceTransformers | Embedding generation |
| FAISS | Vector retrieval |
| Streamlit | Interactive UI |
| BeautifulSoup | Web scraping |
| Dotenv | Secure API key loading |

---

# 🛑 Challenges & Solutions

### 1. Dynamic HTML structure  
→ Extracted semantic containers + headings  

### 2. Duplicate content  
→ Sentence-level deduplication  

### 3. Missing schemes  
→ Added direct scheme URLs  

### 4. Groq model deprecation  
→ Switched to `llama-3.3-70b-versatile`  

---

# 🚀 Potential Improvements

- Auto-crawler for entire BOM loan domain  
- Add BM25 hybrid retrieval  
- Metadata tagging of all chunks  
- Multi-language support  
- Add evaluation metrics  

---

# 📊 RAG Architecture Diagram

```
                        ┌───────────────────────────────────────────────┐
                        │     Bank of Maharashtra Loan Assistant        │
                        │               (RAG System)                    │
                        └───────────────────────────────────────────────┘
                                       ▲
                                       │ User Question
                                       │
                          ┌─────────────────────────┐
                          │     Streamlit UI        │
                          └─────────────────────────┘
                                       │
                                       ▼
                          ┌─────────────────────────┐
                          │   RAG Pipeline (Python) │
                          └─────────────────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
        ┌──────────────────────────┐            ┌──────────────────────────┐
        │ SentenceTransformer      │            │   FAISS Vector Search    │
        │ Query Embedding         │            │ Retrieve Top-K Chunks    │
        └──────────────────────────┘            └──────────────────────────┘
                      │                                 │
                      └──────────────┬──────────────────┘
                                     ▼
                         ┌──────────────────────────────┐
                         │ Retrieved Context Chunks      │
                         └──────────────────────────────┘
                                     │
                                     ▼
                      ┌────────────────────────────────────────┐
                      │ Groq LLM (llama-3.3-70b-versatile)     │
                      └────────────────────────────────────────┘
                                     ▼
                         ┌──────────────────────────────┐
                         │ Final Answer + Source Chunks │
                         └──────────────────────────────┘
```

---

# 🎉 Conclusion

This project demonstrates the complete workflow of a modern **RAG-based intelligent assistant**, including scraping, cleaning, vector search, embedding models, prompt engineering, and UI deployment.

It fulfills all assignment requirements from EncureIT Systems Pvt Ltd.

---

