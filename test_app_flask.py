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




def Load_Vectorizer(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    

# load_dotenv()

PATH_CSV = "CSV/"
PATH_VEC = "VECTORS/"


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


# S'assurer que les fichiers de vectorizer existent bien
# def test_vectorizer_titles_file():
#     print("\n****** Test Vectorizer File")
#     try:
#         vectorizer_path = PATH_VEC + "tfidf_vectorizer_titles.pkl"
#         assert Path(vectorizer_path).exists()
#     except:
#         assert False, f"Le fichier {vectorizer_path} est introuvable."


# S'assurer que l'on peut charger le vectorizer à partir du fichier
# def test_load_vectorizer_titles():
#     print("\n****** Test Load Vectorizer")
#     try:
#         vectorizer_path = PATH_VEC + "tfidf_vectorizer_titles.pkl"
#         _ = Load_Vectorizer(vectorizer_path)
#         assert True
#     except:
#         assert False, f"Impossible de charger le vectorizer depuis {vectorizer_path}."



# filename = f"VECTORS/tfidf_matrix_titles.npz"
# tfidf_matrix_titles = sp.sparse.load_npz(filename)

# S'assurer que le fichier avec la matrice TF-IDF des documents existe bien
def test_tfidf_matrix():
    print("\n****** Test TF-IDF Matrix")
    try:
        df_data_path = PATH_VEC + "tfidf_matrix_titles.npz"
        assert Path(df_data_path).exists()
    except:
        assert False, f"Le fichier {df_data_path} est introuvable."



if __name__ == "__main__":
    print("START MAIN")
    # test_vectorizer_titles_file()
#     test_load_vectorizer()
