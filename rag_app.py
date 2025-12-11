from groq import Groq
from sentence_transformers import SentenceTransformer
import faiss, pickle, os
import numpy as np

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vectorstore/faiss.index")

with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def ask_rag(question, top_k=5):
    # Encode and normalize query
    q_embed = model.encode([question])
    q_embed = q_embed.astype('float32')
    faiss.normalize_L2(q_embed)
    
    # Search for top_k most similar chunks
    distances, idx = index.search(q_embed, top_k)
    
    # Filter by similarity threshold (cosine similarity > 0.3)
    valid_results = [(i, d) for i, d in zip(idx[0], distances[0]) if d > 0.3]
    
    if not valid_results:
        return "I could not find relevant information in Bank of Maharashtra documents. Please try rephrasing your question or ask about home loans, personal loans, education loans, or MSME loans.", []
    
    retrieved = [chunks[i] for i, _ in valid_results]

    context = "\n\n---\n\n".join(retrieved)

    prompt = f"""You are a helpful Bank of Maharashtra Loan Assistant.

Use the information from the context below to answer the question. You can:
- Combine information from multiple sections
- Make reasonable inferences based on the context
- Provide helpful explanations

CONTEXT:
{context}

QUESTION:
{question}

Provide a clear, helpful answer based on the context above. If the specific information is not available but related information exists, mention what you found and suggest the user contact the bank for exact details.

If no relevant information is found at all, say: "I could not find this information in Bank of Maharashtra documents."
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )

    answer = response.choices[0].message.content

    return answer, retrieved