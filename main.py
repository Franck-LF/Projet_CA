# ---------------------------------------------------------------
#
# Projet classification documentaire
#
# API FastAPI exposant le modèle de classification de textes d'assurance.
#
# ---------------------------------------------------------------


import os
import jwt
import datetime
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from fastapi import FastAPI, Query, Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from tools import cleaning_process, remove_stopwords_punct
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv





# Environnement variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
API_PASSWORD = os.getenv("API_PASSWORD")

print("SECRET_KEY:", SECRET_KEY)
print("API_PASSWORD:", API_PASSWORD)



# ---------------- Model ----------------
def Load_Pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)



MODEL_PATH = "MODELS/"
vectorizer = Load_Pickle(MODEL_PATH + "vectorizer_ia_texts.pkl")
model = Load_Pickle(MODEL_PATH + "reglog_ia_texts.pkl")


app = FastAPI(title="API Classification Assurance")




# Configuration de la sécurité
security = HTTPBearer()

# Modèle pour l'authentification
class TokenRequest(BaseModel):
    password: str
    duration: Optional[int] = 3600  # in seconds


def create_jwt(duration: int) -> str:
    """
    Fonction qui permet de générer un token JWT
    
    - **param duration** : Durée de validité du token en secondes
    - **return** : Token JWT encodé
    """
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    return jwt.encode(
        {"exp": expiration},
        SECRET_KEY, # Server side
        algorithm="HS256" # Hashing algorithm
    )

@app.post("/token")
def generate_token(request: TokenRequest):
    """
        Route qui permet de générer un token pour un utilisateur qui saisit son mot de passe
    
     - **param request** :  Objet TokenRequest contenant le mot de passe et la durée
     - return : Token JWT
    """
    print("request.password:", request.password)
    if request.password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_jwt(request.duration)
    return {"token": token}

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Fonction qui permet de vérifier le token JWT

    - **param credentials** : Credentials fournis via le bearer token
    - **return** : None
    - **raises** : HTTPException si le token est invalide ou expiré
    """
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")




# @app.get("/")
# async def home(request: Request):
#     '''
#         Page d'accueil
#     '''
#     return {'Titre' : "API IA Assurance active"}


@app.get("/")
def root():
    return {"message": "API assurance active"}

@app.post("/predict")
async def predict(text: str,
            credentials: HTTPAuthorizationCredentials = Depends(security)
            ):
    """
        Route réalisant la prédiction à partir d'un texte saisi par l'utilisateur.
    
        Return: Un dictionnaire contenant le texte, la probabilité d'être un texte d'assurance, et une classification binaire.
    """
    # await verify_token(credentials)

    print("Received text for prediction:", text)

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
    # print("X_data:", X_data)
    prediction = model.predict(X_data)[0]
    # print("prediction:", prediction)

    # prediction_proba = model.predict_proba(X_data)[0]
    # print("prediction_proba:", prediction_proba)

    return {
        "text": text,
        "assurance_probability": float(prediction),
        "is_assurance": bool(prediction > 0.5)
    }