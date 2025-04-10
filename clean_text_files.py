import os
import re

# Folder containing your original TXT files
INPUT_DIR = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\LAW_TXT"
# Folder to save cleaned TXT files
OUTPUT_DIR = "LAW_TXT_CLEANED"

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    # Remove multiple blank lines
    text = re.sub(r'\n\s*\n+', '\n', text)
    # Replace tabs and multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Merge lines that are split in the middle of sentences
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Remove excessive leading/trailing whitespace
    return text.strip()

# Process each file
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".txt"):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(input_path, "r", encoding="utf-8") as infile:
            raw_text = infile.read()

        cleaned = clean_text(raw_text)

        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(cleaned)

        print(f"[✔] Cleaned and saved: {output_path}")
