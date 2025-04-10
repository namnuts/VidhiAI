import os
import re

# === CONFIG ===
INPUT_FILE = "LAW_TXT_CLEANED/ipcIndia.txt"
OUTPUT_FILE = "LAW_CHUNKS/ipc_chunks.txt"
os.makedirs("LAW_CHUNKS", exist_ok=True)

# === Function to Split by Legal Separator (Dashed Lines) ===
def split_by_separator(text):
    # Split using dashed line separator (at least 20 dashes)
    chunks = re.split(r'-{20,}', text)
    cleaned_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]
    return cleaned_chunks

# === Load text
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# === Chunk it
chunks = split_by_separator(raw_text)

# === Save to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, 1):
        f.write(f"### Chunk {i} ###\n{chunk}\n\n")

print(f"[✅] Chunked {len(chunks)} sections from: {INPUT_FILE}")
print(f"[💾] Saved cleaned chunks to: {OUTPUT_FILE}")
