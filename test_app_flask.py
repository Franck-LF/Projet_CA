# ---------------------------------------------------------------
#
# Test unitaires pour l'application Flask de moteur de recherche.
#
# ---------------------------------------------------------------


import os
import io
import sys
import pytest
import pickle
import numpy as np
import pandas as pd
import scipy as sp
from pathlib import Path
from dotenv import load_dotenv

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))




# ---------------- Model ----------------
# def Load_Pickle(filename):
#     with open(filename, 'rb') as file:
#         return pickle.load(file)

# load_dotenv()

PATH_CSV = "CSV/"


# ------------------------------------------
#
#           Mes tests
#
# ------------------------------------------
# S'assurer que le fichier avec le dataframe avec les informations sur les documents existe bien
def test_df_data_documents_file():
    print("\n****** Test df_data documents")
    try:
        df_data_path = PATH_CSV + "df_data.csv"
        assert Path(df_data_path).exists()
    except:
        assert False, f"Le fichier {df_data_path} est introuvable."


# S'assurer que l'on peut charger le dataframe avec les informations sur les documents
def test_load_df_data_documents():
    print("\n****** Test Load df_data documents")
    try:
        df_data_path = PATH_CSV + "df_data.csv"
        _ = pd.read_csv(df_data_path, index_col = [0])
        assert True
    except:
        assert False, f"Impossible de charger le dataframe des documents depuis {df_data_path}."


# # S'assurer que le fichier de vectorizer existe bien
# def test_vectorizer_file():
#     print("\n****** Test Vectorizer File")
#     try:
#         vectorizer_path = PATH + "vectorizer_ia_texts.pkl"
#         assert Path(vectorizer_path).exists()
#     except:
#         assert False, f"Le fichier {vectorizer_path} est introuvable."

# # S'assurer que l'on peut charger le vectorizer
# def test_load_vectorizer():
#     print("\n****** Test Load Vectorizer")
#     try:
#         vectorizer_path = PATH + "vectorizer_ia_texts.pkl"
#         _ = Load_Pickle(vectorizer_path)
#         assert True
#     except:
#         assert False, f"Impossible de charger le vectorizer depuis {vectorizer_path}."

# # # S'assurer que la forme de sortie du vectorizer est cohérente avec 
# # # la forme d'entrée du classifieur (Logistic regression)
# def test_vectorizer_output_dimension():
#     vectorizer_path = PATH + "vectorizer_ia_texts.pkl"
#     vectorizer = Load_Pickle(vectorizer_path)
#     model_path = PATH + "reglog_ia_texts.pkl"
#     model = Load_Pickle(model_path)
#     X_transformed = vectorizer.transform(["Simple texte pour faire mon test"])
#     print("TF-IDF output:", X_transformed.shape)
#     print("Classifier input:", model.coef_.shape[1])
#     assert X_transformed.shape[1] == model.coef_.shape[1], \
#             f"ATTENTION !!!\n {X_transformed.shape[1]} != {model.coef_.shape[1]}"



# if __name__ == "__main__":
#     print("START MAIN")
#     test_model_file()
#     test_load_model()
#     test_vectorizer_file()
#     test_load_vectorizer()
