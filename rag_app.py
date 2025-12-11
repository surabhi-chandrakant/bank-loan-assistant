import os
import pickle
import faiss
import numpy as np
from groq import Groq
from sentence_transformers import SentenceTransformer


# -----------------------------
# Lazy loading for Streamlit Cloud safety
# -----------------------------

_model = None
_index = None
_chunks = None


def load_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def load_faiss_and_chunks():
    global _index, _chunks

    if _index is None:
        _index = faiss.read_index("vectorstore/faiss.index")

    if _chunks is None:
        with open("vectorstore/chunks.pkl", "rb") as f:
            _chunks = pickle.load(f)

    return _index, _chunks


# -----------------------------
# Main RAG function
# -----------------------------
def ask_rag(question, top_k=5):
    # Load Groq client inside function (fix for Streamlit Cloud)
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return "Error: GROQ_API_KEY not found. Please add it in Streamlit Cloud Secrets.", []

    client = Groq(api_key=groq_key)

    # Load model, index, chunks lazily
    model = load_embedding_model()
    index, chunks = load_faiss_and_chunks()

    # Encode query
    q_embed = model.encode([question]).astype("float32")

    # Normalize for cosine-like distance
    try:
        faiss.normalize_L2(q_embed)
    except:
        pass

    # Search FAISS index
    distances, idx = index.search(q_embed, top_k)

    # IMPORTANT:
    # FAISS returns *lower distance = more similar*
    # Your previous code incorrectly required distance > 0.3 (backwards)
    # Now using distance < 1.2 as a reasonable similarity threshold.
    valid_results = [(i, d) for i, d in zip(idx[0], distances[0]) if d < 1.2]

    if not valid_results:
        return (
            "I could not find relevant information in Bank of Maharashtra documents. "
            "Please try rephrasing or ask about home loans, personal loans, education loans, or MSME loans.",
            []
        )

    retrieved = [chunks[i] for i, _ in valid_results]

    # Build RAG prompt
    context = "\n\n---\n\n".join(retrieved)
    prompt = f"""
You are a helpful Bank of Maharashtra Loan Assistant.

Use ONLY the context below to answer the question. Be precise and clear.

CONTEXT:
{context}

QUESTION:
{question}

If the information is not available in the context, say:
"I could not find this information in Bank of Maharashtra documents."
"""

    # Call Groq LLM safely
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return f"LLM request failed: {e}", []

    return answer, retrieved
