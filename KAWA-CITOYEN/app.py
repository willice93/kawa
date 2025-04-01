from flask import Flask, request, jsonify, render_template # type: ignore
import yaml

app = Flask(__name__)

# Chargement du fichier de dialogues YAML
with open("dialogues/citoyen_dialogues.yaml", "r", encoding="utf-8") as f:
    dialogues = yaml.safe_load(f)

def chercher_reponse(texte):
    texte = texte.lower()
    for d in dialogues:
        if d["intent"] == "inconnu":
            continue
        mots = d["question"].lower().split()
        if any(mot in texte for mot in mots) or d["intent"] in texte:
            return d["response"]
    # Si aucun match précis trouvé, renvoyer fallback
    for d in dialogues:
        if d["intent"] == "inconnu":
            return d["response"]
    return "Je n’ai pas encore de réponse à cette question."

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    user_input = data.get("question", "")
    reponse = chercher_reponse(user_input)
    return jsonify({"response": reponse})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    from flask import render_template # type: ignore



