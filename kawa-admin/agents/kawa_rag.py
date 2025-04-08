# Moteur RAG minimal pour questionner tes PDF locaux
# Compatible avec tes documents officiels (raw_input/)

import os
import glob
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Modèle d'embeddings leger (local CPU)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# etape 1 : Lire et chunker simplement tes PDF
def extract_chunks_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    # Chunks simples par paragraphes
    chunks = [para.strip() for para in text.split("\n") if para.strip()]
    return chunks

# etape 2 : Construire embeddings et index FAISS
def build_index(chunks):
    embeddings = embedder.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings

# etape 3 : Recherche RAG simplifiee
def query_rag(question, chunks, index, embeddings, top_k=3):
    q_embedding = embedder.encode([question])
    distances, indices = index.search(q_embedding, top_k)
    results = [chunks[idx] for idx in indices[0]]
    return results

# Usage immediat
if __name__ == "__main__":
    pdf_files = glob.glob("raw_input/*.pdf")
    all_chunks = []
    for pdf in pdf_files:
        chunks = extract_chunks_from_pdf(pdf)
        all_chunks.extend(chunks)

    print(f"Nombre total de chunks extraits : {len(all_chunks)}")
    
    # Creation index
    index, embeddings = build_index(all_chunks)

    # Questionne tes PDF immediatement
    while True:
        question = input("Pose ta question (ou 'stop') : ")
        if question.lower() == "stop":
            break
        results = query_rag(question, all_chunks, index, embeddings)
        print("\n--- Resultats RAG :")
        for res in results:
            print("-", res)
        print("\n")
