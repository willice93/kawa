import os
import re

INPUT_DIR = "from_struct"
OUTPUT_DIR = "chunks"
CHUNK_SIZE = 500  # caractères

def extract_yaml_and_body(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        yaml_block = parts[1].strip()
        body = parts[2].strip() if len(parts) > 2 else ""
        return yaml_block, body
    return "", text

def chunk_text(text, size):
    return [text[i:i+size].strip() for i in range(0, len(text), size) if text[i:i+size].strip()]

def process_file(md_path, output_dir):
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    yaml_block, body = extract_yaml_and_body(content)
    chunks = chunk_text(body, CHUNK_SIZE)

    for idx, chunk in enumerate(chunks):
        chunk_filename = f"{base_name}_chunk_{idx+1}.txt"
        chunk_path = os.path.join(output_dir, chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as cf:
            cf.write(chunk)

    print(f"OK {base_name}.md -> {len(chunks)} chunk(s) generes.")

def process_all_md_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".md")]

    for file in files:
        md_path = os.path.join(INPUT_DIR, file)
        process_file(md_path, OUTPUT_DIR)

if __name__ == "__main__":
    process_all_md_files()
