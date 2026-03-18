# 📄 Projet de moteur de recherche documentaire et de classification de documents d'Assurance

Ce projet propose une solution complète de traitement et de classification de documents basée sur l’intelligence artificielle. Il est structuré en deux parties principales :

1. **Une API FastAPI intégrant un modèle de machine learning**
2. **Une application Flask avec une interface web simple pour interagir avec le modèle**

---

# 🚀 1. API FastAPI & Modèle de Machine Learning

## 🎯 Objectif

Analyser différents types de documents et déterminer si leur contenu est lié au domaine des **assurances** ou non.

---

## 📥 Extraction des données

Le projet prend en charge plusieurs formats de fichiers :

* PDF → `pdfplumber`
* Word → `python-docx`
* Excel → `openpyxl`
* PowerPoint → `python-pptx`

---

## 🔄 Conversion en PDF

Afin d’uniformiser le traitement, les fichiers sont convertis en PDF :

* `docx2pdf`
* `pptxtopdf`
* `win32com`

---

## 🧹 Nettoyage des données

Les textes extraits sont nettoyés via :

* Expressions régulières (**RegEx**)
* Traitement linguistique avec **SpaCy**

Objectifs :

* Suppression des caractères inutiles
* Normalisation du texte
* Préparation pour le modèle

---

## 🧠 Feature Engineering

* Encodage des textes avec **TF-IDF** (`scikit-learn`)
* Transformation des textes en vecteurs numériques exploitables

---

## ✂️ Préparation des données

* Séparation des données :

  * **Assurance**
  * **Non assurance**
* **Chunking** des textes (découpage en segments)
* Split :

  * Données d'entraînement
  * Données de test

---

## 🤖 Modélisation

* Modèle utilisé : **Régression Logistique** (`scikit-learn`)
* Objectif : classification binaire

---

## 📊 Suivi des performances

* Tracking des expérimentations avec **MLflow**
* Sauvegarde des métriques et résultats

---

## 💾 Sauvegarde des artefacts

* Vectorizer TF-IDF
* Modèle de régression logistique

---

## 🔌 API FastAPI

Une API est exposée pour permettre l’utilisation du modèle :

### Endpoint principal :

```http
POST /predict
```

### Exemple de requête :

```json
{
  "text": "Ce contrat couvre les risques liés à l'habitation."
}
```

### Réponse :

```json
{
  "prediction": "assurance"
}
```

---

# 🌐 2. Application Web Flask

## 🎯 Objectif

Fournir une interface utilisateur simple pour interagir avec le modèle.

---

## 🖥️ Fonctionnement

1. L’utilisateur saisit :

   * un mot
   * ou une phrase

2. L’application Flask :

   * envoie la requête à l’API FastAPI

3. L’API :

   * analyse le texte
   * retourne une prédiction

4. L’application affiche :

   * **"Assurance"** ou **"Non assurance"**

---

## 🔄 Architecture globale

```
Utilisateur → Interface Flask → API FastAPI → Modèle ML → Résultat → Interface Flask
```

---

# 🛠️ Installation

## 1. Cloner le projet

```bash
git clone <repo_url>
cd <repo_name>
```

---

## 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer les services

### API FastAPI

```bash
uvicorn main:app --reload
```

---

### Application Flask

```bash
python app.py
```

---

# 📦 Technologies utilisées

* Python
* FastAPI
* Flask
* Scikit-learn
* SpaCy
* MLflow
* pdfplumber
* python-docx
* openpyxl
* python-pptx

---

# 📌 Améliorations possibles

* Ajout d’un modèle plus avancé (BERT, transformers)
* Amélioration de l’interface utilisateur
* Ajout de gestion multi-langue
* Déploiement cloud optimisé

---

# 👨‍💻 Auteur

Projet réalisé dans le cadre d’un apprentissage en data science et développement web.

---
