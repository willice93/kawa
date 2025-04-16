import faiss
import json
import yaml
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# === Configuration ===
INDEX_PATH = "faiss_index.bin"
ID_MAP_PATH = "faiss_id_map.json"
YAML_DIR = "kawa_struct"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

# === Chargement du modèle et de l’index ===
print("[] Chargement du modèle d'embedding...")
model = SentenceTransformer(MODEL_NAME)

print("[] Chargement de l’index FAISS...")
index = faiss.read_index(INDEX_PATH)

with open(ID_MAP_PATH, "r", encoding="utf-8") as f:
    id_list = json.load(f)

# === Fonction de recherche ===
def interroger_rag(question, top_k=TOP_K):
    vecteur = model.encode([question])
    distances, indices = index.search(np.array(vecteur).astype("float32"), top_k)

    résultats = []
    for idx, score in zip(indices[0], distances[0]):
        doc_id = id_list[idx]
        yaml_path = os.path.join(YAML_DIR, f"{doc_id}.yaml")
        if os.path.exists(yaml_path):
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                résultats.append({
                    "id": doc_id,
                    "score": float(score),
                    "titre": data.get("titre", "Sans titre"),
                    "embedding_text": data.get("embedding_text", "")[:300] + "..."
                })
    return résultats

# === Exécution CLI ===
if __name__ == "__main__":
    print("🔎 Entrez votre question (ou Ctrl+C pour quitter) :")
    try:
        while True:
            question = input("\n Question > ").strip()
            if question:
                résultats = interroger_rag(question)
                print("\n📚 Résultats les plus proches :")
                for r in résultats:
                    print(f"\n ID : {r['id']}\nTitre : {r['titre']}\nScore FAISS : {r['score']:.2f}\n---\n{r['embedding_text']}")
    except KeyboardInterrupt:
        print("\n[] Fin de session.")
