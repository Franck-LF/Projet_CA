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



# ---------------- Flask App --------------
app = Flask(__name__)




# ---------------- Routes ----------------


FASTAPI_URL = "http://127.0.0.1:8000/predict"


# récupérer token
token_response = requests.post(
    "http://127.0.0.1:8000/token",
    data={
        "username": "admin",
        "password": "admin"
    }
)

token = token_response.json()["detail"][0]["input"].split("&")[1].split("=")[1]


@app.route("/", methods=["GET", "POST"])
def index():
    
    result = None

    if request.method == "POST":
        text = request.form["text"]
        print("Text:", text)

        response = requests.post(
            FASTAPI_URL,
            params={"text": text},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print("Response Status Code:", response.status_code)
        if response.status_code == 200:
            result = response.json()
        
        print("Result:", result)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)


