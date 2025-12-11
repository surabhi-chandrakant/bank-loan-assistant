from sentence_transformers import SentenceTransformer
import faiss, pickle

with open("data/clean_loans.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Enhanced: chunk by sentences instead of fixed size
sentences = text.split(". ")
chunks = []
temp = ""

for s in sentences:
    if len(temp) + len(s) < 450:
        temp += s + ". "
    else:
        chunks.append(temp)
        temp = s + ". "

chunks.append(temp)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index, "vectorstore/faiss.index")

with open("vectorstore/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ Vector store created successfully!")
