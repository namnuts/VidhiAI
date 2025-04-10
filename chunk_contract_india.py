import re
import json

INPUT_PATH = "LAW_TXT_CLEANED/contractactIndian.txt"
OUTPUT_PATH = "LAW_CHUNKS/contract_chunks.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Normalize extra spaces
text = re.sub(r'\s+', ' ', raw_text)

# Split by CHAPTERS (if any)
chapter_matches = re.split(r'(CHAPTER\s+[IVXLCDM]+\s*.*?) (?=\d{1,3}[A-Z]?\.\s)', text, flags=re.IGNORECASE)

chunks = []

if chapter_matches:
    # If chapters are found
    for i in range(1, len(chapter_matches), 2):
        chapter_title = chapter_matches[i].strip()
        chapter_text = chapter_matches[i + 1].strip()

        # Match section numbers like 3., 19A., 100.
        sections = re.split(r'(?=\d{1,3}[A-Z]?\.\s)', chapter_text)

        for section in sections:
            match = re.match(r'^(\d{1,3}[A-Z]?)\.\s*(.+?)(?=\s\d{1,3}[A-Z]?\.\s|\Z)', section, re.DOTALL)
            if match:
                section_num = match.group(1)
                section_text = match.group(2).strip()
                chunks.append({
                    "chapter": chapter_title,
                    "section": section_num,
                    "text": f"{section_num}. {section_text}"
                })

else:
    # Fallback if no chapters found — still extract sections
    sections = re.findall(r'(\d{1,3}[A-Z]?)\.\s(.+?)(?=\s\d{1,3}[A-Z]?\.\s|\Z)', text)
    for section_num, section_text in sections:
        chunks.append({
            "chapter": "General",
            "section": section_num,
            "text": f"{section_num}. {section_text.strip()}"
        })

# Save as JSON
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"[✅] Extracted {len(chunks)} Contract Act chunks.")
print(f"[💾] Saved to: {OUTPUT_PATH}")

