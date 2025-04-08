import os

# Nom du répertoire principal
base_dir = "kawa-admin"

# Dossiers à créer
subdirs = [
    "raw_input",
    "from_collect",
    "from_struct",
    "chunks",
    "embeddings",
    "index",
    "dialogues",
    "agents",
    "tests"
]

# README pour chaque dossier
readme_content = {
    "raw_input": "Contient les données brutes collectées (PDF, HTML, DOCX, etc.)",
    "from_collect": "Fichiers nettoyés en .txt générés par KAWA-COLLECT",
    "from_struct": "Fichiers structurés en Markdown avec YAML en-tête via KAWA-STRUCT",
    "chunks": "Segments de texte découpés par KAWA-CHUNK",
    "embeddings": "Vecteurs générés pour chaque chunk par KAWA-EMBED",
    "index": "Index de recherche utilisé pour le moteur RAG local",
    "dialogues": "Scénarios conversationnels pour guider les interactions",
    "agents": "Scripts Python exécutant chaque module KAWA",
    "tests": "Résultats des tests et fichiers de vérification"
}

# Création de l'arborescence
def create_project_structure():
    os.makedirs(base_dir, exist_ok=True)
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        os.makedirs(path, exist_ok=True)
        readme_path = os.path.join(path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {subdir}\n\n{readme_content.get(subdir, '')}\n")

    # Fichier d'intention GUWA-GUIDE
    guwa_path = os.path.join(base_dir, "guwa_guide.yaml")
    if not os.path.exists(guwa_path):
        with open(guwa_path, "w", encoding="utf-8") as f:
            f.write("# Fichier GUWA-GUIDE : intention sémantique, balises, exclusions, finalité\n")

    # Fichier .gitignore
    gitignore_path = os.path.join(base_dir, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write("*.pyc\n__pycache__/\n.env\n.DS_Store\n")

    print(f"Structure KAWA-ADMIN initialisée dans : {base_dir}/")

# Exécution principale
if __name__ == "__main__":
    create_project_structure()
