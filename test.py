
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
# Requete PREDICT

# FASTAPI_URL = "http://127.0.0.1:8000/"
# token = "token"

# response = requests.post(
#             FASTAPI_URL + "predict",
#             params={"text": "assurance tous risques"},
#             headers={"Authorization": f"Bearer {token}"}
#         )

# print("status_code:", response.status_code)

# if response.status_code == 200:
#     result = response.json()
#     print("result:", result)

# Requete TOKEN

# FASTAPI_URL = "http://127.0.0.1:8000/"
# # token = "token"
# # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQwNDU3Mjl9.QMzkhLMwdw4_d_0lZse9Wy3704WWMHggiDF6f0dqqwA"

# payload = {
#         "password": "admin",
#         "duration": 3600
#     }

# response = requests.post(
#             FASTAPI_URL + "token",
#             json=payload
#         )

# print("status_code:", response.status_code)

# if response.status_code == 200:
#     result = response.json()
#     print("result:", result)

from sklearn.feature_extraction.text import TfidfVectorizer

sentences = ["Un avion est en train de décoller.",
          "Un homme joue d'une grande flûte.",
          "Un homme étale du fromage râpé sur une pizza.",
          "Une personne jette un chat au plafond.",
          "Une personne est en train de plier un morceau de papier.",
          "Un italien prépare le repas avec du fromage",
          "Le chien joue dans le jardin au milieu des fleurs",
          "L'éléphant mange"
          ]

vectorizer = TfidfVectorizer()
tfidf_sentences = vectorizer.fit_transform(sentences)
print(type(tfidf_sentences), tfidf_sentences.shape)