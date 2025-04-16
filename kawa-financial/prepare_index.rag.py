from sentence_transformers import SentenceTransformer
import faiss
import yaml
import os
import numpy as np
import json

# Répertoires et fichiers
yaml_dir = "kawa_struct"
index_file = "faiss_index.bin"
id_map_file = "faiss_id_map.json"

# Modèle léger pour CPU
model = SentenceTransformer("all-MiniLM-L6-v2")

# Lecture des YAML avec champ "embedding_text"
documents = []
ids = []

for file in os.listdir(yaml_dir):
    if file.endswith(".yaml"):
        with open(os.path.join(yaml_dir, file), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if "embedding_text" in data:
                documents.append(data["embedding_text"])
                ids.append(data["id"])

# Génération des embeddings
embeddings = model.encode(documents, show_progress_bar=True)

# Création de l’index FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Sauvegarde de l’index + correspondance ID
faiss.write_index(index, index_file)
with open(id_map_file, "w", encoding="utf-8") as f:
    json.dump(ids, f, ensure_ascii=False, indent=2)

print(f"[✓] Index FAISS généré : {index_file}")
print(f"[✓] Mapping ID : {id_map_file}")
print(f"[✓] Total documents indexés : {len(ids)}")
