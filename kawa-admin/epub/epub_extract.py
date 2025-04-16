from ebooklib import epub
from bs4 import BeautifulSoup
import os
import re
import yaml

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator="\n")

def epub_to_kawa(epub_path, output_dir="from_struct/"):
    book = epub.read_epub(epub_path)
    
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "Sans titre"
    author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else "Inconnu"
    lang = book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else "xx"

    text_content = []

    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            cleaned = clean_html(item.get_content().decode("utf-8"))
            text_content.append(cleaned)

    full_text = "\n\n".join(text_content)
    safe_title = re.sub(r'\W+', '_', title.lower())[:50]
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, f"{safe_title}.md"), "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.dump({
            "title": title,
            "author": author,
            "language": lang,
            "source": "epub",
        }, allow_unicode=True))
        f.write("---\n\n")
        f.write(full_text)

    print(f"[✓] Exporté vers : {output_dir}{safe_title}.md")

# Exemple d’utilisation :
# epub_to_kawa("ton_fichier.epub")
