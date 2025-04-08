from flask import Flask, request, jsonify, render_template
import os
import json
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === CONFIG ===
CHUNKS_DIR = "chunks"
EMBEDDINGS_PATH = "embeddings/embeddings.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

app = Flask(__name__)

# === Charger corpus texte + noms ===
def load_corpus_and_filenames():
    with open(EMBEDDINGS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    filenames = [item["chunk"] for item in data]
    texts = []
    for file in filenames:
        path = os.path.join(CHUNKS_DIR, file)
        with open(path, encoding="utf-8") as h:
            texts.append(h.read())
    return texts, filenames

# === RAG
def retrieve(question, texts, filenames, top_k=3):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts + [question])
    question_vec = vectors[-1]
    chunk_vectors = vectors[:-1]
    sims = cosine_similarity(question_vec, chunk_vectors).flatten()
    top_idx = sims.argsort()[-top_k:][::-1]
    return [(filenames[i], texts[i]) for i in top_idx]

# === LLM
def ask_mistral(question, context):
    prompt = f"""
Tu es un assistant administratif.
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

# === API Endpoint
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/ask", methods=["POST"])

def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "question manquante"}), 400

    texts, filenames = load_corpus_and_filenames()
    top_chunks = retrieve(question, texts, filenames)
    context = "\n---\n".join([c[1] for c in top_chunks])
    response = ask_mistral(question, context)

    return jsonify({
        "question": question,
        "response": response,
        "chunks": [c[0] for c in top_chunks]
    })

if __name__ == "__main__":
    app.run(debug=True)
