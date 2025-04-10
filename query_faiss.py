import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === CONFIG ===
INDEX_PATH = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\legal_faiss.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
# ==============

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load same embedding model used during indexing
model = SentenceTransformer(EMBEDDING_MODEL)

# Load the original text chunks (same order as when indexed)
# You need to keep this consistent!
def load_chunks_from_txt(txt_dir="LAW_TXT_CLEANED"):
    chunks = []
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    for filename in sorted(os.listdir(txt_dir)):  # Use sorted to keep order
        if filename.endswith(".txt"):
            with open(os.path.join(txt_dir, filename), "r", encoding="utf-8") as f:
                text = f.read()
            split_chunks = splitter.split_text(text)
            chunks.extend(split_chunks)
    return chunks

# Load the chunks
import os
chunks = load_chunks_from_txt("LAW_TXT_CLEANED")

# Query the FAISS index
def search(query, top_k=TOP_K):
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, top_k)
    results = [chunks[i] for i in indices[0]]
    return results

# CLI Loop
if __name__ == "__main__":
    while True:
        q = input("\n⚖️  Enter your legal question (or type 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break

        results = search(q)
        print("\n🔍 Top Relevant Chunks:\n" + "-" * 40)
        for i, chunk in enumerate(results, 1):
            print(f"{i}. {chunk.strip()[:500]}...\n")  # limit print to 500 chars
