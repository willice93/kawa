import os
import re
import yaml
from pathlib import Path

EXPLANATION_DIR = "from_explanation"
EXAMPLE_DIR = "from_exemples"
OUTPUT_DIR = "kawa_struct"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

def detecter_formule(contenu):
    match = re.search(r"(\d{1,5})\s*(euros|€).*?(\d{1,2})\s*%", contenu)
    if match:
        montant = int(match.group(1))
        taux = int(match.group(3)) / 100
        abattement = round(montant * taux)
        revenu_net = montant - abattement
        formule = f"revenu_brut * (1 - {taux})"
        exemple = {
            "revenu_brut": montant,
            "abattement": abattement,
            "revenu_net": revenu_net
        }
        return formule, exemple
    return None, None

def fusionner_fichiers(id_base):
    base = id_base.replace(".txt", "")
    fichier_exp = f"{base}.txt"
    fichier_exemple = f"{base}.example.txt"
    path_exp = os.path.join(EXPLANATION_DIR, fichier_exp)
    path_ex = os.path.join(EXAMPLE_DIR, fichier_exemple)

    if not os.path.exists(path_exp) or not os.path.exists(path_ex):
        print(f"[!] Fichiers manquants pour : {id_base}")
        return

    with open(path_exp, "r", encoding="utf-8") as f1, open(path_ex, "r", encoding="utf-8") as f2:
        explication = f1.read()
        exemple_txt = f2.read()

    formule, exemple_calc = detecter_formule(exemple_txt)

    yaml_struct = {
        "id": base,
        "titre": explication.split('\n')[0].strip(),
        "source": "Brochure IR 2024",
        "regle": {
            "description": explication.strip(),
            "formule": formule or "Non détectée"
        },
        "calcul": {
            "formule": formule,
            "exemple": exemple_calc
        } if formule else None,
        "cas_pratique": exemple_txt.strip()
    }

    output_path = os.path.join(OUTPUT_DIR, base + ".yaml")
    with open(output_path, "w", encoding="utf-8") as f_out:
        yaml.dump(yaml_struct, f_out, allow_unicode=True, sort_keys=False)
        print(f"[✓] YAML généré : {output_path}")

def batch_fusion():
    fichiers = [f for f in os.listdir(EXPLANATION_DIR) if f.endswith(".txt")]
    for fichier in fichiers:
        fusionner_fichiers(fichier)

if __name__ == "__main__":
    batch_fusion()
