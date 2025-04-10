import os
import re

# === CONFIG ===
INPUT_FILE = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\LAW_TXT_CLEANED\consumerProtectionIndia.txt"
OUTPUT_FILE = "LAW_CHUNKS/constitution_chunks.txt"
os.makedirs("LAW_CHUNKS", exist_ok=True)

def split_by_articles(text):
    # Add a split marker before every legal article number like 14. or 21A.
    marked = re.sub(r'(?<!\d)(\d{1,3}[A-Z]?\.\s)', r'###ARTICLE###\1', text)

    # Now split the text at our custom marker
    raw_chunks = marked.split('###ARTICLE###')

    # Keep only valid chunks starting with numbers like 14. or 21A.
    cleaned_chunks = []
    for chunk in raw_chunks:
        chunk = chunk.strip()
        if re.match(r'^\d{1,3}[A-Z]?\.', chunk):  # Must start with a number + dot
            cleaned_chunks.append(chunk)

    return cleaned_chunks


# === Load Constitution Text
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# === Chunk It
chunks = split_by_articles(raw_text)

# === Save Chunks to File
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, 1):
        f.write(f"### Article {i} ###\n{chunk}\n\n")

print(f"[✅] Chunked {len(chunks)} articles from: {INPUT_FILE}")
print(f"[💾] Saved to: {OUTPUT_FILE}")
