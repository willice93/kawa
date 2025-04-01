# KAWA-CITOYEN v0.1 
Licence : KAWA-COPYFAIR v1.0 – voir KAWA-LICENCE.txt

**Agent autonome KAWA** destiné à répondre aux questions administratives de base :  
vote, carte d’identité, actes civils, contact mairie.

---

## Fonctionnalités

- Interface terminale simple (mode texte)
- Réponses scriptées à partir d’un fichier YAML
- Aucune connexion Internet requise
- Corpus local en Markdown
- Extensible avec d’autres dialogues ou modules (RAG, TTS…)

---

## Structure du projet

kawa-citoyen/ ├── docs/ │ └── citoyen_guide.md # Corpus structuré (consultable ou futur RAG) ├── dialogues/ │ └── citoyen_dialogues.yaml # Dialogues scénarisés ├── run.py # Interface interactive (console) └── README.md # Documentation

yaml
Copier
Modifier

---

## Lancer l’agent

### Prérequis

- Python 3.x installé
- Module `pyyaml` (si besoin : `pip install pyyaml`)

### Commande

```bash
python run.py
Tapez ensuite une question (ex : Comment voter ?)
Tapez exit pour quitter.

Prolongements possibles
Intégration RAG avec le fichier citoyen_guide.md

Ajout d’un moteur vocal TTS (ex : Piper)

Passage en interface web via Flask ou Tauri

Version mobile (Termux, app native)

Licence
Projet sous licence KAWA-Libre (à définir).
Usage personnel, éducatif et communautaire.

KAWA : Une IA, le temps d’un café.

yaml
Copier
Modifier

---

Tu as maintenant une **clé fonctionnelle, complète, sobre et modulaire.**

Souhaites-tu que l’on passe à la **clé suivante** (ex : `KAWA-ADMIN`, `KAWA-LIRE`, ou `KAWA-SURVIVOR-lite`) ?  
Ou que je t’aide à créer une **interface web légère** autour de celle-ci pour démonstration pu