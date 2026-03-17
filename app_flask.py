# ---------------------------------------------------------------
#
# Application Flask pour l'interface utilisateur du moteur de recherche
#
# Cette application Flask charge :
# - le dataframe avec les informations sur les documents d'assurance
# - les matrices TF-IDF des titres et des textes
# - le vectorizer TF-IDF
#
# Elle expose une interface web pour faire des requêtes de recherche de documents
# Elle utilise la similarité cosinus pour trouver les documents les plus similaires à la requête
# Elle Se lance avec la commande : Python app.py
#
# ---------------------------------------------------------------



import os
from flask import Flask, render_template, request
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from tools import cleaning_process, remove_stopwords_punct
import pickle
import flask_monitoringdashboard as dashboard


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# ---------------- Model ----------------
# def Load_Pickle(filename):
#     with open(filename, 'rb') as file:
#         return pickle.load(file)

def Load_Vectorizer(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# MODEL_PATH = "MODELS/"
# vectorizer = Load_Pickle(MODEL_PATH + "vectorizer_ia_texts.pkl")

# Load the dataframe with documents information
df_data = pd.read_csv("CSV/df_data.csv", index_col = [0])

# load the TF-IDF vectorizer
tfidf_vectorizer_titles = Load_Vectorizer("VECTORS/tfidf_vectorizer_titles.pkl")

# Load the TFIDF matrix of the titles
filename = f"VECTORS/tfidf_matrix_titles.npz"
tfidf_matrix_titles = sp.sparse.load_npz(filename)

# Load the TFIDF matrix of the documents
filename = f"VECTORS/tfidf_matrix_texts.npz"
tfidf_matrix_texts = sp.sparse.load_npz(filename)


# ---------------- Flask App --------------
app = Flask(__name__)




# ---------------- Routes ----------------

@app.route("/", methods=["GET", "POST"])
def index2():
    
    results = None

    if request.method == "POST":
        query = request.form["query"]
        print("query:", query)

        if query.strip():
            print("Text:", query)

            df = pd.DataFrame.from_dict({
            'Texts': [query]
            })
            print(df)
            df['Texts_Cleaned']  = df['Texts'].apply(cleaning_process)
            df['Texts_Token']  = df['Texts_Cleaned'].apply(remove_stopwords_punct)
            print(df)
            query_lemm = [' '.join(df.Texts_Token.values[0])]

            print("query_lemm: ", query_lemm)
            tfidf_query = tfidf_vectorizer_titles.transform(query_lemm)
            similarities = cosine_similarity(tfidf_query, tfidf_matrix_titles).flatten()
            print("Similarities:", similarities)
            index_scores = similarities.argsort()[::-1]
            print("Index Scores:", index_scores)

            results = []
            for i in index_scores:
                title = df_data.Titles.to_list()[i].strip()
                results.append(title)
                if len(results) >= 10:
                    break
            
            print("Results:", results)
        else:
            print("No query provided.")

    else:
        print("No request.method")

    return render_template("index2.html", results=results)


print("BASE_DIR:", BASE_DIR)

# dashboard.config.init_from(file=BASE_DIR + '\\config.cfg')

# Pour relier le dashboard à cette app Flask
dashboard.bind(app)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

