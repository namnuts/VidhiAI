import re
import json

INPUT_FILE = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\LAW_TXT_CLEANED\dowry_prohibition.txt"
OUTPUT_FILE = "LAW_CHUNKS/dowry_chunks.json"

# Read the full text
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize whitespace
text = re.sub(r'\s+', ' ', text)

# Extract sections using regex like "1. Short title..." and its text
pattern = re.compile(r'(?P<number>\d+[A-Z]?\.?)\s(?P<title>[A-Z].*?)(?=\d+[A-Z]?\.|$)', re.DOTALL)

matches = list(pattern.finditer(text))
chunks = []

for i, match in enumerate(matches):
    section = match.group("number").strip(".")
    title = match.group("title").strip()

    # Determine end of this chunk
    start = match.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

    body = text[start:end].strip()

    chunks.append({
        "section": section,
        "title": title,
        "text": body
    })

# Save to JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"[✅] Extracted {len(chunks)} sections from Dowry Act.")
print(f"[💾] Saved to: {OUTPUT_FILE}")
