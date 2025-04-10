import os
from PyPDF2 import PdfReader

# Input and Output paths
pdf_folder = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\legalPDF"

output_folder = "LAW_TXT"

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDFs
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        txt_path = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
        
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            print(f"[✔] Saved: {txt_path}")
        
        except Exception as e:
            print(f"[✘] Failed to process {filename}: {e}")
