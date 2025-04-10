import os
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === CONFIG ===
TXT_DIR = "LAW_TXT_CLEANED"          # Folder containing cleaned .txt files
INDEX_PATH = "legal_faiss.index"     # Output FAISS index file
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Embedding model
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
# ==============

# Load embedding model
print("[🧠] Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

# Prepare chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " "]
)

# Read and split all text files
texts = []

print(f"[📂] Reading and chunking from: {TXT_DIR}\n")
for filename in os.listdir(TXT_DIR):
    if filename.endswith(".txt"):
        file_path = os.path.join(TXT_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        chunks = splitter.split_text(raw_text)
        texts.extend(chunks)

print(f"[✅] Total Chunks to Index: {len(texts)}")

# Embed and index
print("[📦] Embedding chunks and building FAISS index...\n")
embeddings = []
batch_size = 32

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i + batch_size]
    vectors = model.encode(batch)
    embeddings.extend(vectors)

embeddings = np.array(embeddings).astype("float32")
dimension = embeddings.shape[1]

faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)

# Save FAISS index
faiss.write_index(faiss_index, INDEX_PATH)
print(f"\n[✅] FAISS index saved to: {INDEX_PATH}")
