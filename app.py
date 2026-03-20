# ---------------------------------------------------------------
#
# Application Flask pour l'interface utilisateur de classification de textes d'assurance.
#
# - Cette appli Flask requête l'API FastAPI qui expose le modèle d'IA de classification.
#
# Se lance avec la commande : Python app.py
#
# (Accès: http://127.0.0.1:5000)
#
# ---------------------------------------------------------------


import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv


# Environnement variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
API_PASSWORD = os.getenv("API_PASSWORD")
USERNAME = os.getenv("USERNAME")

 

# ---------------- Flask App --------------
app = Flask(__name__)




# ---------------- Routes ----------------


FASTAPI_URL = "http://127.0.0.1:8000/"

# Lors d'un déploiement sur Render on utilisera cette URL:
# FASTAPI_URL = "https://binary-classification.onrender.com/"



payload = {
        "password": API_PASSWORD, #"admin",
        "duration": 3600
    }

def get_token():
    response = requests.post(
        FASTAPI_URL + "token",
        json = payload
    )
    data = response.json()
    print("data:", data)
    return data["token"]


@app.route("/", methods=["GET", "POST"])
def index():
    
    result = None

    if request.method == "POST":

        token = get_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }

        text = request.form["text"]
        print("Text:", text)

        response = requests.post(
            FASTAPI_URL + "predict",
            params = {"text" : text},
            headers = headers
        )
        
        print("Response Status Code:", response.status_code)
        if response.status_code == 200:
            result = response.json()
        
        print("Result:", result)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # prend le port fourni par Render
    app.run(host="0.0.0.0", port=port)

