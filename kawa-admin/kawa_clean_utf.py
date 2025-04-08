import os

FORBIDDEN_CHARS = {
    '\u2192': '->',   # → flèche
    '\u201C': '"',    # “ guillemet courbe
    '\u201D': '"',    # ” guillemet courbe
    '\u2018': "'",    # ‘ apostrophe courbe
    '\u2019': "'",    # ’ apostrophe courbe
    '\u2705': '',     # ✅
    '\U0001f4c2': '', # 📂
    '\U0001f4cc': '', # 📌
    '\U0001f680': '', # 🚀
    '\U0001f4a1': '', # 💡
}

def clean_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        for char, replacement in FORBIDDEN_CHARS.items():
            line = line.replace(char, replacement)
        cleaned.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

def clean_all_py_files(root="."):
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                clean_file(full_path)
                print(f"✔ Fichier nettoyé : {full_path}")

if __name__ == "__main__":
    print("🔧 Nettoyage des caractères non-ASCII décoratifs dans les scripts Python...")
    clean_all_py_files("kawa-admin")
