import os
import re
import spacy
import scipy as sp
import numpy as np
import pandas as pd
import pickle
import pdfplumber
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from flask import Flask, render_template, request, redirect


# ---------------- Flask App --------------
app = Flask(__name__)


# ---------------- Config ----------------
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXT = {"png", "jpg", "jpeg", "webp"}
CLASSES = ['desert', 'forest', 'meadow', 'mountain']


# ---------------- Model ----------------
def Load_Vectorizer(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def Load_ScipyMatrix(filename):
    return sp.sparse.load_npz(filename)

MODEL_PATH = "VECTORS/"
model = Load_Vectorizer(MODEL_PATH + "vectorizer_ia_texts.pkl")




# ---------------- Routes ----------------
@app.route("/", methods=["GET"])
def index():
    """Affiche la page d’upload.

    Returns:
        Réponse HTML rendant le template "upload.html".
    """
    return render_template("upload.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Traite l’upload, exécute la prédiction et affiche le résultat.

    Attendu: une requête `multipart/form-data` avec le champ `file`.
    Étapes:
      1) Validation de présence et d’extension du fichier.
      2) Lecture du contenu en mémoire et ouverture en PIL.
      3) Prétraitement -> tenseur (1, H, W, 3).
      4) Prédiction Keras -> probas, top-1 (label, confiance).
      5) Encodage de l’image en Data URL et rendu du template résultat.

    Redirects:
        - Redirige vers "/" si le fichier est manquant ou invalide.

    Returns:
        Réponse HTML rendant "result.html" avec:
        - `image_data_url` : image soumise encodée (base64),
        - `predicted_label` : classe prédite (str),
        - `confidence` : score softmax (float),
        - `classes` : liste des classes (pour les boutons).
    """

    if "file" not in request.files:
        return redirect("/")
    
    file = request.files["file"]
    if file.filename == "" or not allowed_file(secure_filename(file.filename)):
        return redirect("/")

    raw = file.read()
    pil_img = Image.open(io.BytesIO(raw))
    img_array = preprocess_from_pil(pil_img)

    probs = model.predict(img_array, verbose=0)[0]
    cls_idx = int(np.argmax(probs))
    label = CLASSES[cls_idx]
    conf = float(probs[cls_idx])

    image_data_url = to_data_url(pil_img, fmt="JPEG")

    return render_template("result.html", image_data_url=image_data_url, predicted_label=label, confidence=conf, classes=CLASSES)

@app.route("/feedback", methods=["GET"])
def feedback_ok():
    """Affiche la page de confirmation de feedback (placeholder).

    Returns:
        Réponse HTML rendant le template "feedback_ok.html".
    """
    return render_template("feedback_ok.html")

if __name__ == "__main__":
    app.run(debug=True)

