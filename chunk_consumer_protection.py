import re
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load text from the main file (already extracted from PDF or plain .txt file)
with open("LAW_TXT_CLEANED\consumerProtectionIndia.txt", "r", encoding="utf-8") as file:
    full_text = file.read()

# Optional cleanup: remove headers/footers/extra white spaces
cleaned_text = re.sub(r'\s+', ' ', full_text)

# Step 1: Extract Sections using regex pattern like `1.` or `2.`
section_pattern = re.compile(r'(\d+\.\s.*?)(?=(\d+\.\s)|$)')  # Match sections like 1. or 2.
matches = section_pattern.findall(cleaned_text)

# Step 2: Create dictionary of sections
sections = []
for match in matches:
    title_and_content = match[0].strip()
    # Try separating title and content
    split_title = re.split(r'\s', title_and_content, maxsplit=1)
    if len(split_title) == 2:
        section_number = split_title[0]
        rest = split_title[1]
        title, _, content = rest.partition('.')
        sections.append({
            "title": f"Section {section_number}: {title.strip()}",
            "content": content.strip()
        })

# Step 3: Chunk the content using Langchain splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

chunked_data = []
for section in sections:
    chunks = splitter.split_text(section["content"])
    for idx, chunk in enumerate(chunks):
        chunked_data.append({
            "title": section["title"] + (f" (Part {idx + 1})" if len(chunks) > 1 else ""),
            "content": chunk
        })

# Step 4: Save to JSONL file
with open("consumer_protection_chunks.json", "w", encoding="utf-8") as json_file:
    for entry in chunked_data:
        json.dump(entry, json_file, ensure_ascii=False)
        json_file.write("\n")

print("✅ JSON chunks saved to consumer_protection_chunks.jsonl")
