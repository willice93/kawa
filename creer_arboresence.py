import os

def creer_arborescence_depuis_texte(fichier_txt):
    with open(fichier_txt, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    if not lignes:
        print(" Le fichier est vide.")
        return

    # Extraire la racine (première ligne, sans backslash final)
    racine = lignes[0].strip().rstrip("\\/")
    pile_chemins = [racine]

    for ligne in lignes[1:]:  # on saute la première ligne déjà utilisée
        ligne = ligne.rstrip("\n")
        if not ligne.strip():
            continue

        # Nettoyage et indentation
        nom = ligne.replace("├── ", "").replace("└── ", "").replace("│", "").strip()
        profondeur = (len(ligne) - len(ligne.lstrip())) // 4

         # Ignorer les noms invalides
        if nom.strip(".") == "" or nom in ["...", "…"]:
            continue

        pile_chemins = pile_chemins[:profondeur+1]
        pile_chemins.append(nom)

        chemin_complet = os.path.join(*pile_chemins)

        if nom.endswith("\\") or not "." in nom:
            os.makedirs(chemin_complet.rstrip("\\"), exist_ok=True)
        else:
            os.makedirs(os.path.dirname(chemin_complet), exist_ok=True)
            with open(chemin_complet, "w", encoding="utf-8") as f:
                f.write("")

    print(f" Arborescence créée à partir de la racine : {racine}")

# Utilisation
if __name__ == "__main__":
    creer_arborescence_depuis_texte("structure.txt")
