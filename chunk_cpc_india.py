import os
import re
import json

# === CONFIG ===
INPUT_FILE = "LAW_TXT_CLEANED/cpcIndia.txt"
OUTPUT_JSON = "LAW_CHUNKS/cpc_chunks.json"
os.makedirs("LAW_CHUNKS", exist_ok=True)

def chunk_cpc(text):
    # Normalize text for easier parsing
    text = re.sub(r'\s{2,}', '\n', text)
    text = text.replace("PART ", "\n###PART###PART ")  # Inject marker before PART
    
    parts = text.split("###PART###")
    chunks = []

    for part_block in parts:
        part_lines = part_block.strip().splitlines()
        if not part_lines:
            continue

        part_title = part_lines[0].strip()

        # Combine all lines after part title
        part_content = "\n".join(part_lines[1:])

        # Split sections inside the part
        section_blocks = re.split(r'(?=\n?\d{1,3}[A-Z]?\.\s)', part_content)

        for sec in section_blocks:
            sec = sec.strip()
            if len(sec) > 30:
                # Extract the section number (e.g., "9.")
                match = re.match(r'^(\d{1,3}[A-Z]?)\.', sec)
                section_no = match.group(1) if match else "?"

                chunks.append({
                    "part": part_title,
                    "section": section_no,
                    "text": sec
                })

    return chunks

# === Read the raw CPC file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# === Run the chunker
cpc_chunks = chunk_cpc(raw_text)

# === Save JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(cpc_chunks, f, indent=2, ensure_ascii=False)

print(f"[✅] Chunked {len(cpc_chunks)} CPC sections.")
print(f"[💾] Saved to: {OUTPUT_JSON}")
