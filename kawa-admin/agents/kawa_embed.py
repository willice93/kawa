import os
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_DIR = "chunks"
EMBEDDINGS_DIR = "embeddings"
MAPPING_FILE = os.path.join(EMBEDDINGS_DIR, "embedding_mapping.txt")
MODEL_NAME = "all-MiniLM-L6-v2"  # léger et rapide, adapté à la clé KAWA

def load_chunks():
    chunks = []
    filenames = []
    for filename in sorted(os.listdir(CHUNKS_DIR)):
        if filename.endswith(".txt"):
            path = os.path.join(CHUNKS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    chunks.append(text)
                    filenames.append(filename)
    return chunks, filenames

def embed_chunks(chunks):
    model = SentenceTransformer(MODEL_NAME)
    return model.encode(chunks, show_progress_bar=True)

def save_embeddings(vectors, filenames):
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    np.save(os.path.join(EMBEDDINGS_DIR, "embeddings.npy"), vectors)
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        for name in filenames:
            f.write(f"{name}\n")
    print(f" {len(filenames)} embeddings enregistrés dans : {EMBEDDINGS_DIR}/")

if __name__ == "__main__":
    chunks, filenames = load_chunks()
    if not chunks:
        print(" Aucun chunk trouvé dans le dossier 'chunks/'")
    else:
        vectors = embed_chunks(chunks)
        save_embeddings(vectors, filenames)
