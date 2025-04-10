import fitz  # PyMuPDF
import re
import os
from pathlib import Path
import hashlib





# === CONFIGURATION ===
SOURCE_PDF = "Brochure-IR-2024.pdf"
CHUNK_DIR = "from_chunk"
Path(CHUNK_DIR).mkdir(exist_ok=True)

# === Déclencheurs potentiels de "blocs règles de calcul" ===
PATTERNS_DEBUT = [
    r"(crédit|réduction|abattement).*imp[oô]t",
    r"vous pouvez déduire",
    r"plafond.*",
    r"formule.*",
    r"calcul.*",
    r"frais.*réels",
    r"bar[eè]me.*",
    r"montant.*déductible",
    r"case ?[\dA-Z]+",
]



def contient_regle(text):
    score = 0
    if re.search(r"\d+\s?%", text): score += 1
    if re.search(r"\d{3,5}\s?(€|euros)", text): score += 1
    for pat in PATTERNS_DEBUT:
        if re.search(pat, text, flags=re.IGNORECASE): score += 1
    return score >= 2

def nettoyer(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extraire_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    count = 0

    for i, page in enumerate(doc):
        blocs = page.get_text("blocks")
        for bloc in blocs:
            _, _, _, _, texte, *_ = bloc
            texte = nettoyer(texte)
            if len(texte) < 50: continue
            if contient_regle(texte):
                h = hashlib.md5(texte.encode()).hexdigest()[:8]
                nom_fichier = f"regle_p{i+1}_{h}.chunk.txt"
                path_out = os.path.join(CHUNK_DIR, nom_fichier)
                with open(path_out, "w", encoding="utf-8") as f:
                    f.write(f"# Source: page {i+1}\n\n")
                    f.write(texte)
                count += 1

    print(f"{count} chunks extraits vers {CHUNK_DIR}")

if __name__ == "__main__":
    extraire_chunks(SOURCE_PDF)
