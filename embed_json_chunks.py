import os
import json
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS

from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings


# === CONFIG ===
json_folder = "C:/Users/nagav/OneDrive/Desktop/lawStuff/LAW_CHUNKS"
output_folder = "C:/Users/nagav/OneDrive/Desktop/lawStuff/FAISS_DB"
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# === EMBEDDING SETUP ===
embedding_model = HuggingFaceEmbeddings(model_name=model_name)

# === LOAD & EXTRACT TEXT ===
documents = []

def extract_texts(data, filename):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                extract_texts(value, filename)
            elif isinstance(value, str) and len(value.strip()) > 15:
                documents.append(Document(page_content=value.strip(), metadata={"source": filename}))
    elif isinstance(data, list):
        for item in data:
            extract_texts(item, filename)

# Loop through all JSON files
for file in os.listdir(json_folder):
    if file.endswith(".json"):
        file_path = os.path.join(json_folder, file)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                extract_texts(data, file)
            except Exception as e:
                print(f"[❌] Failed to load {file}: {e}")

# === EMBED & SAVE ===
if documents:
    print(f"[📚] Total extracted chunks: {len(documents)}")
    vector_db = FAISS.from_documents(documents, embedding_model)
    vector_db.save_local(output_folder)
    print(f"[✅] Vector DB saved to: {output_folder}")
else:
    print("[⚠️] No valid text chunks found to embed.")
