# ---------------------------------------------------------------
#
# Projet classification documentaire
#
# API FastAPI exposant le modèle de classification de textes d'assurance.
#
# ---------------------------------------------------------------


import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from fastapi import FastAPI
import pickle
from tools import cleaning_process, remove_stopwords_punct


# ---------------- Model ----------------
def Load_Pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# def Load_ScipyMatrix(filename):
#     return sp.sparse.load_npz(filename)

MODEL_PATH = "VECTORS/"
vectorizer = Load_Pickle(MODEL_PATH + "vectorizer_ia_texts.pkl")
model = Load_Pickle(MODEL_PATH + "reglog_ia_texts.pkl")
print(type(model))

# charger embedder
# embedder = SentenceTransformer("dangvantuan/sentence-camembert-large")

app = FastAPI(title="API Classification Assurance")

@app.get("/")
def root():
    return {"message": "API assurance active"}

@app.post("/predict")
def predict(text: str):

    if len(text.strip()) == 0:
        return {
            "text": text,
            "assurance_probability": 0.0,
            "is_assurance": False
        }
    
    df = pd.DataFrame.from_dict({
        'Texts': [text]
    })

    df['Texts_Cleaned']  = df['Texts'].apply(cleaning_process)
    df['Texts_Token']  = df['Texts_Cleaned'].apply(remove_stopwords_punct)
    text_ = [' '.join(df.Texts_Token.values[0])]
    print("text_: ", text_)
    X_data = vectorizer.transform(text_)
    print("X_data:", X_data)
    prediction = model.predict(X_data)[0]
    print("prediction:", prediction)

    return {
        "text": text,
        "assurance_probability": float(prediction),
        "is_assurance": bool(prediction > 0.5)
    }