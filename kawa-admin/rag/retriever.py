import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDINGS_PATH = "embeddings/embeddings.json"
CHUNKS_DIR = "chunks"

def load_embeddings():
    with open(EMBEDDINGS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    vectors = np.array([item["embedding"] for item in data])
    filenames = [item["chunk"] for item in data]
    return vectors, filenames

def retrieve(question_vector, vectors, filenames, top_k=3):
    sims = cosine_similarity([question_vector], vectors)[0]
    top_idx = sims.argsort()[-top_k:][::-1]
    return [filenames[i] for i in top_idx]

def read_chunks(files):
    chunks = []
    for file in files:
        path = os.path.join(CHUNKS_DIR, file)
        with open(path, encoding="utf-8") as f:
            chunks.append(f.read())
    return chunks

if __name__ == "__main__":
    # Exemple de question (à remplacer par embedding réel)
    dummy_question_vector = np.random.rand(384).tolist()  # à remplacer
    vectors, filenames = load_embeddings()
    top_files = retrieve(dummy_question_vector, vectors, filenames)
    texts = read_chunks(top_files)

    print("\nDocuments les plus pertinents :")
    for name, text in zip(top_files, texts):
        print(f"\n--- {name} ---\n{text[:500]} [...]")
