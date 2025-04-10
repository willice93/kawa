from pathlib import Path
import pandas as pd


# Construction d'un tableau avec liste des fichiers manquants par étape

# Récupération des fichiers réels
chunk_dir = Path("from_chunk")
explain_dir = Path("from_explanation")
example_dir = Path("from_exemples")
yaml_dir = Path("kawa_struct")

chunk_ids = {f.name.replace(".chunk.txt", "") for f in chunk_dir.glob("*.chunk.txt")}
explain_ids = {f.name.replace(".txt", "") for f in explain_dir.glob("*.txt")}
example_ids = {f.name.replace(".example.txt", "") for f in example_dir.glob("*.example.txt")}
yaml_ids = {f.name.replace(".yaml", "") for f in yaml_dir.glob("*.yaml")}

# Compilation des statuts
all_ids = sorted(chunk_ids | explain_ids | example_ids | yaml_ids)

incomplets = []
for id_base in all_ids:
    status = {
        "ID": id_base,
        "Chunk présent": id_base in chunk_ids,
        "Explication présente": id_base in explain_ids,
        "Exemple présent": id_base in example_ids,
        "YAML présent": id_base in yaml_ids
    }
    if not (status["Chunk présent"] and status["Explication présente"] and status["Exemple présent"] and status["YAML présent"]):
        incomplets.append(status)

df_incomplets = pd.DataFrame(incomplets)
print(df_incomplets)
df_incomplets.to_csv("fichiers_incomplets.csv", index=False)

