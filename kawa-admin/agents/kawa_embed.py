import os
import json
import numpy as np
from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf

INPUT_DIR = "chunks"
OUTPUT_DIR = "embeddings"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "embeddings.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = TFAutoModel.from_pretrained(MODEL_NAME)

def mean_pooling(last_hidden_state, attention_mask):
    mask = tf.cast(tf.expand_dims(attention_mask, -1), tf.float32)
    masked = last_hidden_state * mask
    summed = tf.reduce_sum(masked, axis=1)
    counts = tf.reduce_sum(mask, axis=1)
    return summed / counts

def generate_embedding(text):
    encoded = tokenizer(text, truncation=True, padding=True, return_tensors="tf", max_length=512)
    output = model(encoded["input_ids"], attention_mask=encoded["attention_mask"]).last_hidden_state
    pooled = mean_pooling(output, encoded["attention_mask"])
    normalized = tf.linalg.l2_normalize(pooled, axis=1)
    return normalized.numpy().tolist()[0]

def process_all_chunks():
    embeddings = []
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(INPUT_DIR, fname), encoding="utf-8") as f:
                text = f.read()
            emb = generate_embedding(text)
            embeddings.append({"chunk": fname, "embedding": emb})
            print(f"Embedding généré pour {fname}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(embeddings, out, ensure_ascii=False, indent=2)
    print(f"Embeddings enregistrés dans {OUTPUT_FILE}")

if __name__ == "__main__":
    process_all_chunks()
