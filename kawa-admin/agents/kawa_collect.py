import os
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from docx import Document

RAW_DIR = "raw_input"
OUTPUT_DIR = "from_collect"

def clean_text(text):
    return ' '.join(text.replace('\n', ' ').split())

def process_txt(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return clean_text(f.read())

def process_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return clean_text(text)

def process_html(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
        return clean_text(soup.get_text())

def process_docx(filepath):
    doc = Document(filepath)
    text = "\n".join([p.text for p in doc.paragraphs])
    return clean_text(text)

def detect_and_process(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        return process_txt(filepath)
    elif ext == ".pdf":
        return process_pdf(filepath)
    elif ext == ".html":
        return process_html(filepath)
    elif ext == ".docx":
        return process_docx(filepath)
    else:
        print(f"Extension non prise en charge : {ext}")
        return None

def process_all_files():
    if not os.path.exists(RAW_DIR):
        print(f"Dossier introuvable : {RAW_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = os.listdir(RAW_DIR)

    for file in files:
        input_path = os.path.join(RAW_DIR, file)
        if os.path.isfile(input_path):
            print(f"... Traitement de : {file}")
            result = detect_and_process(input_path)
            if result:
                output_filename = os.path.splitext(file)[0] + ".txt"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f" Fichier traite  {output_filename}")
            else:
                print(f" Echec pour : {file}")

if __name__ == "__main__":
    process_all_files()
