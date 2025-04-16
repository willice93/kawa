from pathlib import Path
import yaml

yaml_dir = Path("kawa_struct")
yaml_files = list(yaml_dir.glob("*.yaml"))

def build_embedding_text(data):
    parts = []
    if "regle" in data:
        if "description" in data["regle"]:
            parts.append(f"Règle : {data['regle']['description']}")
        if "formule" in data["regle"] and isinstance(data['regle']['formule'], str):
            if "détectée" not in data['regle']['formule'].lower():
                parts.append(f"Formule : {data['regle']['formule']}")
    if "cas_pratique" in data:
        parts.append(f"Cas pratique : {data['cas_pratique']}")
    return "\n".join(parts)

for file in yaml_files:
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    embedding_text = build_embedding_text(data)
    if embedding_text.strip():
        data["embedding_text"] = embedding_text
        with open(file, "w", encoding="utf-8") as f_out:
            yaml.dump(data, f_out, allow_unicode=True, sort_keys=False)
        print(f"[✓] Embedding ajouté : {file.name}")
