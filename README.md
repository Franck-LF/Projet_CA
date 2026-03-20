# Ce dépôt GitHub contient 2 projets

Projet 1 : Moteur de Recherche pour Documents d'Assurance<br>
Projet 2 : Classification de documents d'Assurance

---

# Projet 1 : Moteur de Recherche pour Documents d’Assurance

Projet développé au sein du Crédit Agricole (CR22), propose un moteur de recherche permettant d'explorer efficacement un corpus de documents du **service ABP** (Assurance des Biens et des Personnes), basé sur des techniques de traitement du langage naturel (NLP) et de calcul de similarité sémantique.

---

# Objectif

Permettre aux utilisateurs du service ABP de retrouver rapidement les documents les plus pertinents à partir d’un mot-clé ou d’une phrase, en s’appuyant sur :

* une **analyse textuelle avancée**,
* des méthodes de **vectorisation classique et moderne**,
* une **recherche par similarité sémantique**.

---

# Fonctionnalités principales

## 1. Analyse et Extraction des textes bruts

Outils pour l'extraction des textes bruts :

* PDF → `pdfplumber`
* Word → `python-docx`
* Excel → `openpyxl`
* PowerPoint → `python-pptx`

---

## 2. Conversion des documents en PDF

* `docx2pdf` → conversion des Word en PDF
* `pptxtopdf` → conversion des PowerPoint en PDF
* `win32com` → convertion des Excel en PDF

---

## 3. Nettoyage des textes

Les textes extraits sont nettoyés via :

* Expressions régulières (**RegEx**)
* Traitement linguistique avec **SpaCy**

Objectifs :

* Nettoyage du texte (suppression des caractères inutiles, normalisation),
* Traitement linguistique avec **SpaCy**,
* Préparation des données pour les étapes de vectorisation.

---

## 4. Vectorisation des textes

Deux approches complémentaires sont utilisées :

### Vectorisation TF-IDF (Scikit-learn)
### Embeddings sémantiques à l'aide du modèle **Sentence-Camembert-Large**

---

## 5. Recherche de similarité

Lorsqu’un utilisateur saisit une requête :

1. Le texte est prétraité
2. Il est vectorisé (TF-IDF + embeddings)
3. Une **similarité cosinus** est calculée entre :

   * la requête utilisateur
   * les documents du corpus

---

## 4. Résultats

L’application retourne :

* une liste des documents les plus pertinents
* classés par score de similarité

---

Deux version de ce moteur de recherche sont disponibles

# 5. Application Web (Streamlit)

Une interface simple permet d’interagir avec le moteur de recherche :

## Fonctionnement :

1. L’utilisateur saisit une requête (mot ou phrase)
2. L’application :

   * envoie la requête au moteur de recherche,
   * calcule les similarités.

3. Les résultats sont affichés :

   * liste de documents pertinents avec nom des auteurs et date de dernière modification,
   * lorsqu'un document de la liste est sélectionné un aperçu des documents s'affiche.

4. Options disponibles :
   * Un système de filtre de documents est disponible,
   * 2 modes de recherche : recherche dans les titres / recherche dans le contenu des documents,
   * Possibilité de diminuer / augmenter le nombre de résultats dans la liste,
   * Possibilité de télécharger les documents.

# 5 bis. Application Web (Flask)

Une interface Web minimale permet d’interagir avec le moteur de recherche :

## Fonctionnement :

1. L’utilisateur saisit une requête (mot ou phrase)
2. L’application :

   * envoie la requête au moteur de recherche,
   * calcule les similarités.

3. Les résultats sont affichés :

   * liste de documents pertinents

---

# Installation

## 1. Cloner le projet

```bash
git clone <https://github.com/Franck-LF/Projet_CA>
cd <nom_du_dossier>
```

---

## 2. Installer un environnement avec les dépendances

```bash
python -m venv my_env
```

```bash
pip install -r requirements.txt
```

---

## 3. Lancer l'analyse des documents et le calculs des vectorisations

```bash
python traitement_nocturne.py
```

---

## 4. Lancer l’application Streamlit

```bash
streamlit run app_streamlit.py
```

Puis accéder à l’application via :

```
http://localhost:8501/
```

## 4 bis. Lancer l’application Flask

```bash
python app_flask.py
```

Puis accéder à l’application via :

```
http://127.0.0.1:5000/
```

---

# Projet 2 : Classification de documents d'Assurance

Ce projet propose une solution de traitement et de classification de documents basée sur l’intelligence artificielle. Il est structuré en deux parties principales :

1. **Une API FastAPI intégrant un modèle de machine learning**
2. **Une application Flask avec une interface web simple pour interagir avec le modèle**

---

# 1. API FastAPI & Modèle de Machine Learning

## Objectif

Analyser différents types de documents et déterminer si leur contenu est lié au domaine des **assurances** ou non.

---

## Analyse des documents

Le traitement des documents et des textes des documents est identique que pour le projet 1.

---

## Séparation des données pour l'entraînement

* Labellisation des données :
  * **Assurance**
  * **Non assurance**
* **Chunking** des textes (découpage en segments)
* Split :
  * Données d'entraînement
  * Données de test

---

## Entraînement d'un modèle d'IA

* Modèle utilisé : **Régression Logistique** (`scikit-learn`)
* Objectif : classification binaire

---

## Suivi des performances

* Tracking des expérimentations avec **MLflow**
* Sauvegarde des métriques et résultats

---

## Sauvegarde

* Vectorizer TF-IDF
* Modèle de régression logistique

---

## API FastAPI

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
  "prediction": "assurance",
  "text": "text",
  "assurance_probability": 0.86746815,
  "no_assurance_probability": 0.13253185,
  "is_assurance": "True"
}
```

---

# 2. Application Web Flask

## Objectif

Fournir une interface utilisateur simple pour interagir avec le modèle.

---

## Fonctionnement

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

# Installation

## 1. Cloner le projet

```bash
git clone <https://github.com/Franck-LF/Projet_CA>
cd <nom_du_dossier>
```

---

## 2. Installer un environnement avec les dépendances

```bash
python -m venv my_env
```

```bash
pip install -r requirements.txt
```

---

## 3. Lancer l'entraînement du modèle

```bash
python train_classifier.py
```

---

## 4. Lancer l'API FastAPI

```bash
uvicorn main:app --reload
```

Puis accéder à la documentation en ligne de l'API via :

```
http://127.0.0.1:8000/docs/
```

---

## 5. Lancer l'application Flask

```bash
python app.py
```

Puis accéder à l’application via :

```
http://127.0.0.1:5000/
```

---
