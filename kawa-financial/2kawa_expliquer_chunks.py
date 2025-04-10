# kawa_expliquer_chunks.py
# Étape 1 de la nouvelle chaîne :
# Lit chaque chunk, génère une explication claire, sauvegarde dans /from_explanation/

import os
import subprocess
from pathlib import Path

CHUNK_DIR = "from_chunk"
EXPLAIN_DIR = "from_explanation"
MODEL = "mistral"  # ou deepseek, codellama, etc.

Path(EXPLAIN_DIR).mkdir(exist_ok=True)

def construire_prompt(texte, page_source):
    return f"""
Lis attentivement le texte suivant.
Résume-le sous la forme d’une règle de calcul claire, sans code ni tableau.

Ta réponse doit inclure :
- À qui s’applique la règle
- Dans quelles conditions
- Quels sont les montants ou plafonds
- Quelle est la formule de calcul applicable
- Et ce qu’il faut vérifier pour être sûr d’y avoir droit

Voici le texte à analyser :
<<<
{texte}
>>>
""".strip()

def interroger_llm(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=240
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"[ERREUR] {e}"

def traiter_chunks():
    fichiers = [f for f in os.listdir(CHUNK_DIR) if f.endswith(".chunk.txt")]
    total = 0

    for fichier in fichiers:
        path_in = os.path.join(CHUNK_DIR, fichier)
        with open(path_in, "r", encoding="utf-8") as f:
            contenu = f.read()
            texte = contenu.split("\n\n", 1)[1] if "\n\n" in contenu else contenu

        page = contenu.split("page")[1].split("\n")[0].strip() if "page" in contenu else "?"
        prompt = construire_prompt(texte, page)
        print(f"[>] Traitement de {fichier}...")

        reponse = interroger_llm(prompt)

        if reponse.strip():
            path_out = os.path.join(EXPLAIN_DIR, fichier.replace(".chunk.txt", ".txt"))
            with open(path_out, "w", encoding="utf-8") as f_out:
                f_out.write(reponse.strip())
            print(f"[✓] Réponse sauvegardée : {path_out}")
            total += 1
        else:
            print(f"[!] Réponse vide pour {fichier}")

    print(f"\n[✔] {total} explications générées dans {EXPLAIN_DIR}")

if __name__ == "__main__":
    traiter_chunks()