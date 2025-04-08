import os
import datetime
import uuid

INPUT_DIR = "from_collect"
OUTPUT_DIR = "from_struct"

def sanitize_title(filename):
    return filename.replace("_", " ").replace("-", " ").title()

def generate_yaml_block(title, category="administratif", tags=None):
    if tags is None:
        tags = ["auto"]
    yaml_block = f"""---
id: {uuid.uuid4()}
title: "{title}"
date: {datetime.date.today()}
category: {category}
tags: {tags}
---

"""
    return yaml_block

def process_file(txt_path, output_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_name = os.path.basename(txt_path)
    title = sanitize_title(os.path.splitext(base_name)[0])
    yaml_header = generate_yaml_block(title)

    full_md = yaml_header + content

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_md)

    print(f"OK {base_name} -> structure dans {os.path.basename(output_path)}")

def process_all_txt_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

    for file in files:
        txt_path = os.path.join(INPUT_DIR, file)
        output_filename = os.path.splitext(file)[0] + ".md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        process_file(txt_path, output_path)

if __name__ == "__main__":
    process_all_txt_files()
