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
@pytest.mark.parametrize("filename", ["tfidf_vectorizer_titles.pkl", "tfidf_vectorizer_texts.pkl"])
def test_vectorizer_titles_file(filename):
    print("\n****** Test Vectorizer File")
    try:
        vectorizer_path = PATH_VEC + filename
        assert Path(vectorizer_path).exists()
    except:
        assert False, f"Le fichier {vectorizer_path} est introuvable."


# S'assurer que l'on peut charger le vectorizer à partir du fichier
@pytest.mark.parametrize("filename", ["tfidf_vectorizer_titles.pkl", "tfidf_vectorizer_texts.pkl"])
def test_load_vectorizer_titles(filename):
    print("\n****** Test Load Vectorizer")
    try:
        vectorizer_path = PATH_VEC + filename
        _ = Load_Vectorizer(vectorizer_path)
        assert True
    except:
        assert False, f"Impossible de charger le vectorizer depuis {vectorizer_path}."


# S'assurer que le fichier avec la matrice TF-IDF des documents existe bien
def test_tfidf_matrix():
    print("\n****** Test TF-IDF Matrix")
    try:
        tfidf_matrix_path = PATH_VEC + "tfidf_matrix_titles.npz"
        assert Path(tfidf_matrix_path).exists()
    except:
        assert False, f"Le fichier {tfidf_matrix_path} est introuvable."

# S'assurer que l'on peut charger la matrice TF-IDF des documents
def test_load_tfidf_matrixs():
    print("\n****** Test Load TF-IDF Matrix")
    try:
        tfidf_matrix_path = PATH_VEC + "tfidf_matrix_titles.npz"
        _ = sp.sparse.load_npz(tfidf_matrix_path)
        assert True
    except:
        assert False, f"Impossible de charger la matrice TF-IDF des documents depuis {tfidf_matrix_path}."


# S'assurer que la dimension de sortie du vectorizer est cohérente avec 
# la dimension de la matrice TF-IDF déjà calculée à partir de notre base documentaire
def test_vectorizer_output_dimension():
    vectorizer_path = PATH_VEC + "tfidf_vectorizer_titles.pkl"
    vectorizer = Load_Vectorizer(vectorizer_path)
    tfidf_matrix_path = PATH_VEC + "tfidf_matrix_titles.npz"
    tfidf_matrix = sp.sparse.load_npz(tfidf_matrix_path)
    X_transformed = vectorizer.transform(["Simple texte pour faire mon test"])
    print("TF-IDF Matrix Shape:", X_transformed.shape)
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
    assert X_transformed.shape[1] == tfidf_matrix.shape[1], \
            f"ATTENTION !!!\n {X_transformed.shape[1]} != {tfidf_matrix.shape[1]}"



if __name__ == "__main__":
    print("START MAIN")
    # test_vectorizer_titles_file()
#     test_load_vectorizer()
    test_vectorizer_output_dimension()


