# KAWA-MANIFEST.md

## 🌱 Origine

KAWA (Knowledge Agent With Autonomy) est un système modulaire d’intelligences locales, conçues pour fonctionner sans Internet, sur des supports sobres comme des clés USB.  
Il répond à une vision claire : **reprendre la maîtrise des outils de savoir**, et les rendre accessibles, reproductibles, éthiques et résilients.

---

## 🧭 Intention

KAWA n’est ni une plateforme, ni une app.  
C’est une **structure vivante**, une **forme réplicable**, au service de l’autonomie.  
Chaque agent KAWA répond à un usage concret (santé, citoyenneté, alphabétisation, métier, mémoire…),  
et peut être utilisé **sans connexion**, dans tous les contextes : foyers, abris, écoles, zones isolées, communautés rurales ou urbaines.

---

## 🔷 Strates fondamentales

KAWA est organisé en **trois strates** :

1. **L’Étage clair**  
   > Origine du projet. Strate de vision pure. Aucun compromis fonctionnel n’y est toléré.

2. **Transmission consciente – Clé d’éveil**  
   > Mise en forme du sens. Rédaction, balises sémantiques, scénarisation pédagogique.

3. **Domaine opératoire**  
   > Mise en œuvre technique. Code, structure, agents, interfaces, scripts, RAG, LLMs.

---

## 🛠️ Architecture technique

Chaque agent KAWA est conçu pour être **autonome, sobre et reproductible**.  
Il peut contenir :

- Un moteur local (Flask + Python portable)
- Des fichiers de dialogue (`.yaml`) et de contenu (`.md`)
- Une interface web (`index.html`)
- Un navigateur portable (optionnel)
- Des fonctions TTS ou audio préenregistrées (optionnel)
- Un moteur RAG local (optionnel)
- Un modèle de langage (LLM quantisé ou distillé) intégré si nécessaire  
  > (ex. : DeepSeek 1.3B Q4, Mistral 7B Q4, Phi 2…)

📦 Tous les composants sont modifiables, remplaçables, combinables.  
La structure est faite pour accueillir **toute évolution future**, sans centralisation imposée.

Le système tient dans **moins de 4 Go (hors LLM)**, et fonctionne sans installation sur la machine hôte.

---

## 🛰️ Phase de lancement – Infrastructure d’amorçage

Une **infrastructure temporaire centrale** est prévue pour le lancement :

- Téléchargement des clés pré-packagées
- Stockage des LLMs, voix, images et documents
- Remontées anonymisées pour amélioration (optionnelles)
- Espace pour la communauté naissante (partage, entraide, dépôts)

Cette phase est assumée comme **transitoire**.  
KAWA est pensé pour aller vers une diffusion distribuée :  
> duplication locale, clés physiques, réseaux mesh, propagation humaine.

---

## 🔐 Licence

Ce module est publié sous la **double licence** suivante :

- **GNU AGPL v3** (Affero General Public License)  
  → Fournit la base juridique libre, forte, reconnue internationalement.  
  → Texte complet dans `LICENSE_AGPL.txt`

- **Clause complémentaire KAWA-COPYFAIR v1.0**  
  → Garantit la liberté totale d’usage non commercial  
  → Exige une autorisation pour tout usage commercial par des entreprises privées  
  → Empêche l’appropriation ou la fermeture du code

Le projet est placé sous la responsabilité éthique de l’**association SUR LE TAS**,  
qui en détient les droits moraux et légaux, afin d'assurer sa pérennité et son ouverture pour les générations futures.

---

📜 Pour plus d'informations :  
- `KAWA-LICENCE.txt` → version complète en français  
- `KAWA-LICENSE-EN.txt` → version complète en anglais  
- `LICENSE_AGPL.txt` → texte original de la licence AGPL v3

---

## ✍️ Auteur et porteur

Projet initié, conceptualisé et structuré par **Roog**,  
et juridiquement protégé par l’association à but non lucratif :

**Association SUR LE TAS**  
60 AV STALINGRAD  
93200 Saint-Denis – France

---

## 🔁 Transmission

Ce manifeste est un **socle vivant**.  
Il peut être recopié, adapté, prolongé, tant que les principes fondamentaux sont respectés :

- Accès libre au savoir  
- Souveraineté numérique  
- Respect des utilisateurs  
- Reproductibilité intégrale  
- Clarté du sens

---

## 🕰️ Antériorité et preuve

Ce document constitue une **preuve d’antériorité structurée**,  
signée, versionnée, et rendue publique dans le dépôt officiel `kawa/`.

Il marque le passage de l’idée à la forme,  
et garantit que l’origine du projet est **consciente, structurée, librement transmise.**

---

**Signé le 1er avril 2025**  
par **Roog**  
pour l’**association SUR LE TAS**
