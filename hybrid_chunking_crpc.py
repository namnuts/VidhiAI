import os
import re
import json

# === CONFIG ===
INPUT_FILE = "LAW_TXT_CLEANED/crpcIndia.txt"
OUTPUT_FILE = "LAW_CHUNKS/crpc_chapter_chunks.json"
os.makedirs("LAW_CHUNKS", exist_ok=True)

def chunk_by_chapters(text):
    # Normalize CHAPTER headings
    text = re.sub(r'\s{2,}', '\n', text)  # convert multiple spaces to newlines
    text = re.sub(r'(CHAPTER\s+[IVXLCDM\-A]+)', r'\n###CHAPTER###\1', text, flags=re.IGNORECASE)

    chunks = []
    blocks = text.split("###CHAPTER###")

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines or not lines[0].strip().upper().startswith("CHAPTER"):
            continue

        chapter_number = lines[0].strip()

        # Get title from second line if it exists and is not a section
        chapter_title = ""
        if len(lines) > 1 and not re.match(r'^\d{1,3}[A-Z]?\.', lines[1]):
            chapter_title = lines[1].strip()

        full_title = f"{chapter_number}: {chapter_title}".strip(": ")

        # Rest is body
        chapter_text = "\n".join(lines[2:]).strip()

        if len(chapter_text) > 50:
            chunks.append({
                "chapter": full_title,
                "text": chapter_text
            })

    return chunks

# === Run Script
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

chapters = chunk_by_chapters(text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chapters, f, indent=2, ensure_ascii=False)

print(f"[✅] Chunked {len(chapters)} chapters from CrPC.")
print(f"[💾] Saved to: {OUTPUT_FILE}")
