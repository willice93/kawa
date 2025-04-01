import yaml

def charger_dialogues(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def chercher_reponse(question_utilisateur, dialogues):
    question_basse = question_utilisateur.lower()
    for d in dialogues:
        if d["intent"] == "inconnu":
            continue
        mots_clefs = d["question"].lower().split()
        if any(mot in question_basse for mot in mots_clefs) or d["intent"] in question_basse:
            return d["response"]
    return next((d["response"] for d in dialogues if d["intent"] == "inconnu"), "Je n'ai pas de réponse.")

def lancer_agent():
    print("\nBienvenue dans KAWA-CITOYEN")
    print("Posez une question simple (ex: 'Comment voter ?', 'Carte d'identité', etc.)\n")

    dialogues = charger_dialogues("dialogues/citoyen_dialogues.yaml")

    while True:
        question = input(">> ").strip()
        if question.lower() in ["exit", "quit", "stop"]:
            print("\nMerci d’avoir utilisé KAWA-CITOYEN. À bientôt !")
            break
        reponse = chercher_reponse(question, dialogues)
        print(f"\n{reponse}\n")

if __name__ == "__main__":
    lancer_agent()
