from flask import Flask, request, jsonify, render_template
import os
import json
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# === CONFIG ===
CHUNKS_DIR = "chunks"
EMBEDDINGS_FILE = "embeddings/embeddings.npy"
MAPPING_FILE = "embeddings/embedding_mapping.txt"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

# === Charger modèle SentenceTransformer (pour encoder la question)
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

app = Flask(__name__)

# === Charger vecteurs + noms de fichiers + contenus
def load_vectors_and_texts():
    vectors = np.load(EMBEDDINGS_FILE)
    with open(MAPPING_FILE, encoding="utf-8") as f:
        filenames = [line.strip() for line in f]

    texts = []
    for fname in filenames:
        path = os.path.join(CHUNKS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            texts.append(f.read())
    return vectors, filenames, texts

# === RAG avec similarité cosine sur embeddings
def retrieve(question, vectors, filenames, texts, top_k=3):
    question_vec = MODEL.encode([question])
    sims = cosine_similarity(question_vec, vectors).flatten()
    top_idx = sims.argsort()[-top_k:][::-1]
    return [(filenames[i], texts[i]) for i in top_idx]

# === Appel Ollama
def ask_mistral(question, context):
    prompt = f"""
Tu es un chercheur en cybersecurité spécialisé en OSINT.
Voici des extraits de documents à utiliser pour répondre :

{context}

Question : {question}
Réponds précisément et uniquement à partir du contenu fourni.
"""
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

# === Routes Flask
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "question manquante"}), 400

    vectors, filenames, texts = load_vectors_and_texts()
    top_chunks = retrieve(question, vectors, filenames, texts)
    context = "\n---\n".join([c[1] for c in top_chunks])
    response = ask_mistral(question, context)

    return jsonify({
        "question": question,
        "response": response,
        "chunks": [c[0] for c in top_chunks]
    })

if __name__ == "__main__":
    app.run(debug=True)
