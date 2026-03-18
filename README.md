## Ce dépôt GitHub contient 2 projets :
Projet 1 : Moteur de Recherche pour Documents d'Assurance
Projet 2 : Classification de documents d'Assurance

---

# 🔎 Projet 1 : Moteur de Recherche pour Documents d’Assurance

Projet développé au sein du Crédit Agricole (CR22), propose un moteur de recherche interne permettant d’explorer efficacement un corpus de documents liés au domaine des **assurances** grâce à des techniques de traitement du langage naturel (NLP) et de similarité sémantique.

---

# 🎯 Objectif

Permettre aux utilisateurs de retrouver rapidement les documents les plus pertinents à partir d’un mot-clé ou d’une phrase, en s’appuyant sur :

* une **analyse textuelle avancée**
* des méthodes de **vectorisation classique et moderne**
* une **recherche par similarité sémantique**

---

# 🧠 Fonctionnalités principales

## 📄 1. Analyse et nettoyage des documents

Les documents sont prétraités afin d’améliorer la qualité des recherches :

* Nettoyage du texte (suppression des caractères inutiles, normalisation)
* Traitement linguistique avec **SpaCy**
* Préparation des données pour les étapes de vectorisation

---

## 🔢 2. Vectorisation des textes

Deux approches complémentaires sont utilisées :

### 🔹 TF-IDF (Scikit-learn)

* Transformation des documents en vecteurs basés sur la fréquence des termes
* Méthode rapide et efficace pour capturer les mots importants

### 🔹 Embeddings sémantiques

* Utilisation du modèle **Sentence-Camembert-Large**
* Capture du **sens global des phrases**
* Permet une recherche plus intelligente (au-delà des mots exacts)

---

## 🔍 3. Recherche de similarité

Lorsqu’un utilisateur saisit une requête :

1. Le texte est prétraité
2. Il est vectorisé (TF-IDF + embeddings)
3. Une **similarité cosinus** est calculée entre :

   * la requête utilisateur
   * les documents du corpus

---

## 📊 4. Résultats

L’application retourne :

* les documents les plus pertinents
* classés par score de similarité

---

# 🌐 5. Application Web (Flask)

Une interface simple permet d’interagir avec le moteur de recherche :

## Fonctionnement :

1. L’utilisateur saisit une requête (mot ou phrase)
2. L’application :

   * envoie la requête au moteur de recherche
   * calcule les similarités
3. Les résultats sont affichés :

   * liste de documents pertinents

---

# 🏗️ Architecture

```
Utilisateur → Interface Flask → Traitement NLP → Vectorisation → Similarité → Résultats
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

## ▶️ Lancer l’application

```bash
python app.py
```

Puis accéder à l’application via :

```
http://localhost:5000
```

---

# 📦 Technologies utilisées

* Python
* Flask
* SpaCy
* Scikit-learn (TF-IDF)
* Sentence Transformers (Camembert)
* NumPy / SciPy

---

# 🚀 Améliorations possibles

* Ajout d’un système de filtrage avancé (type de document, date…)
* Mise en place d’un index vectoriel (FAISS, Annoy)
* Interface utilisateur plus avancée
* Support multi-utilisateurs
* Déploiement cloud

---

# 📌 Cas d’usage

* Recherche rapide dans des documents internes d’assurance
* Aide à la décision pour les équipes métiers
* Centralisation de l’information documentaire

---

# 👨‍💻 Auteur

Projet réalisé dans le cadre du développement d’un outil interne de recherche documentaire basé sur l’intelligence artificielle.

---


# 📄 Projet 2 : Classification de documents d'Assurance

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
