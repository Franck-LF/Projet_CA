# --------------------------------------------
#
# Custom buttons:
# src: https://discuss.streamlit.io/t/button-css-for-streamlit/45888/9
#
# About onclick:
# src: https://blog.finxter.com/learning-streamlits-buttons-features/
#

import re
import os
import io

import scipy as sp
import pandas as pd
import streamlit as st
import spacy

from pathlib import Path
from datetime import datetime
import time

from PIL import Image
import base64
import pickle

from unidecode import unidecode
from streamlit_pdf_viewer import pdf_viewer

from sklearn.metrics.pairwise import cosine_similarity



@st.cache_data
def Load_Data(filename):
    return pd.read_csv(filename, index_col = [0])

@st.cache_data
def Load_Vectorizer(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

@st.cache_data
def Load_ScipyMatrix(filename):
    return sp.sparse.load_npz(filename)

@st.cache_resource
def Load_NLP(ff = ""):
    df_sw = pd.read_csv('CSV/stopwords-fr_CUSTOM.csv')
    nlp = spacy.load("E:\\YBP10\\ApachePub_Php8\\PPB\\bibliotheque-ABP\\fr_core_news_md-3.8.0\\fr_core_news_md\\fr_core_news_md-3.8.0\\")
    nlp.Defaults.stop_words.clear()
    nlp.Defaults.stop_words |= {word for word in df_sw.values.flatten().tolist()}
    return nlp


# -------------------------------------------------------------------
# Text processing
#

def lower(text):
    return text.lower()

def clean_text(text):
    text = text.replace('\n', ' ').replace('_', ' ')
    return re.sub(' +', ' ', text)

def clean_special_char(text):
    """ Remove underscores
        We should remove: $%&#[@!?*+]()
    """
    text = re.sub(r"…", '.', text)
    text = text.replace('.', ' ')
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace('?', ' ')
    text = text.replace('!', ' ')
    text = text.replace('%', ' ')
    return text

def clean_XXX(text):
    return re.sub(r"x{2,}", ' ', text)

def clean_folder_path(text):
    # ISSUE: does not work for: s:\dab-abp-car\equip\02 (because not ending by \):
    return re.sub(r"/^([a-zA-Z]:\\)([-\u4e00-\u9fa5\w\s.()~!@#$%^&()\[\]{}+=]+\\)*$/gm", ' ', text)
    # ISSUE: it removes also all texts starting with '\':
    return re.sub(r".+(?=\\)", ' ', text)

def clean_spaces_and_line_terminator(text):
    text = text.replace('\n', ' ')
    return re.sub(r" +", ' ', text).strip()

def clean_slashes(text):
    ''' replace slashes when surrounded by spaces '''
    text = text.replace(' / ', ' ')
    return text.replace(' \\ ', ' ')

def cleaning_process(text):
    text = lower(text)
    text = clean_folder_path(text)
    text = clean_special_char(text)
    text = clean_XXX(text)
    text = clean_slashes(text)
    return clean_spaces_and_line_terminator(text)

def remove_stopwords_punct(text):
    doc = nlp(text)
    return [token for token in doc if not (token.is_stop or token.is_punct)]

def rebuilder_EX(doc):
    text = ' '.join([token.text for token in doc])
    return re.sub(' +', ' ', text).strip()

def lemmatizer_EX(doc):
    text = ' '.join([token.lemma_ for token in doc])
    return re.sub(' +', ' ', text).strip()

def lemmatizer_CONCAT(doc):
    ''' Lemmatizer where we concat the lemmatized text to the original text '''

    def remove_duplicate_words(text):
        ''' Remove duplicate words '''
        return ' '.join(set(text.split(' ')))
    
    return remove_duplicate_words(lemmatizer_EX(doc) + ' ' + rebuilder_EX(doc))


def tfidf_search(query, top_k = 5, threshold = 0.03):
    """Recherche TF-IDF"""

    similarities = None

    # Search in titles
    if radio_content == "titre":
        # Process the new query
        query = map(cleaning_process, query)
        query = map(remove_stopwords_punct, query)
        query = map(lemmatizer_CONCAT, query)
        query = list(map(unidecode, query))
        tfidf_query = tfidf_vectorizer_titles.transform(query)
        similarities = cosine_similarity(tfidf_query, tfidf_matrix_titles).flatten()

    # Search in text content
    elif radio_content == "document":
        query = map(cleaning_process, query)
        query = map(remove_stopwords_punct, query)
        query = map(lemmatizer_EX, query)
        query = list(map(unidecode, query))
        tfidf_query = tfidf_vectorizer_texts.transform(query)
        similarities = cosine_similarity(tfidf_query, tfidf_matrix_texts).flatten()
    
    else:
        assert False
        assert radio_content == "titre + chemin"
        # query = map(cleaning_process, query)
        # query = map(remove_stopwords_punct, query)
        # query = map(lemmatizer_CONCAT, query)
        # query = list(map(unidecode, query))
        # tfidf_query = tfidf_vectorizer_titles_paths.transform(query)
        # similarities = cosine_similarity(tfidf_query, tfidf_matrix_titles_paths).flatten()

    index_scores = similarities.argsort()
    index_scores = index_scores[::-1]

    results = []
    for i in index_scores:
        results.append({"index" : i, "score" : similarities[i]})

    return results

def show_pdf(file_path):
    """Affiche un PDF dans l'application Streamlit à l'aide de streamlit-pdf_viewer
       src: https://pypi.org/project/streamlit-pdf-viewer/    
    """
    try:
        # Lecture du fichier PDF
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_viewer(file_path, show_page_separator = True)

    except Exception as e:
        st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        st.info("Assurez-vous que le fichier PDF existe dans le chemin spécifié.")

def show_pdf_2(file_path):
    """Affiche un PDF dans l'application Streamlit"""
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%" type="application/pdf" style="height: 70vh;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        st.info("Assurez-vous que le fichier PDF existe dans le chemin spécifié.")





# ------------------------------
#  CSS
#

# Function to load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS file
local_css("""E:/YBP10/ApachePub_Php8/PPB/bibliotheque-ABP/.streamlit/assets/style.css""")




# ------------------------------
#  Options
#

nlp = Load_NLP()
suf = ''
#suf = "_SAVE" # With All docs
df_data = Load_Data("CSV/df_data" + suf + ".csv")
tfidf_vectorizer_titles = Load_Vectorizer("VECTORS/tfidf_vectorizer_titles" + suf + ".pkl")
tfidf_vectorizer_texts = Load_Vectorizer("VECTORS/tfidf_vectorizer_texts" + suf + ".pkl")
# tfidf_vectorizer_titles_paths = Load_Vectorizer("VECTORS/tfidf_vectorizer_titles_paths" + suf + ".pkl")
tfidf_matrix_titles = Load_ScipyMatrix("VECTORS/tfidf_matrix_titles" + suf + ".npz")
tfidf_matrix_texts = Load_ScipyMatrix("VECTORS/tfidf_matrix_texts" + suf + ".npz")
# tfidf_matrix_titles_paths = Load_ScipyMatrix("VECTORS/tfidf_matrix_titles_paths" + suf + ".npz")

path_temp_pdf = "E:\\YBP10\\ApachePub_Php8\\PPB\\bibliotheque-ABP\\TEMP_PDF\\"
# path_temp_pdf = "../_TEMP_PDF/" # With all docs
radio_content = "titre"
display_Button = False
radio_encoding = "exacte"
nb_documents = 20
threshold = .003
radio_pdf = "1"

# To set dynamically
units = [r'ACAP', r'CAR', r'UGA', r'USP', r'Commun']
filter_check_boxes = []


# ----------- #
#    MAIN     #
# ----------- #

# Configuration de la page
st.set_page_config(
    page_title="Moteur de Recherche ABP",
    # page_icon="📜",
    page_icon="https://www.predica.com/wp-content/uploads/logo-ca-assurances.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

image = Image.open("E:/YBP10/ApachePub_Php8/PPB/bibliotheque-ABP/IMAGES/logo.png")
# st.image(image, width=128)

# --- Bannière CA ---
# st.markdown('<img src=logo.png>', unsafe_allow_html=True)
st.markdown("""
<div class="banner">
    <img src="https://www.predica.com/wp-content/uploads/logo-ca-assurances.svg" width=48 alt="Crédit Agricole Logo">
    Pôle ABP - Bibliothèque &nbsp&nbsp
</div>
""",
unsafe_allow_html = True)


# Cacher le menu burger et le footer par défaut de Streamlit
style_hide_streamlit = \
    """
    <style>
    MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    body { background-color: linen; }
    { color: red; text-align: center; margin-left: 40px; }
    </style>
    """

dict_type_icon = { 
    'pdf'  : '📕',
    'docx' : '📘',
    'doc'  : '📘',
    'pptx' : '📙',
    'xlsx' : '📗',
    'xlsm' : '📗',
    'xls'  : '📗',
}

st.markdown(style_hide_streamlit, unsafe_allow_html=True)

#user = os.getlogin()
#st.write("User: ", user)

#userhome = os.path.expanduser('~')
#st.write("Username: " + os.path.split(userhome)[-1])

#st.experimental_user
#st.write(os.environ)



# --------------------------------
# Sidebar to display options
#

with st.sidebar:
    st.image(image)
    st.markdown("""<h2>⚙️ Options</h2>""", unsafe_allow_html=True)

    radio_content = st.radio(
        "Rechercher dans le :", [
                                "titre", 
                                "document", 
                                # "titre + chemin"
                                ],
        help=(
            "Faire la recherche dans le titre uniquement ou bien dans le contenu du document."
        ),
        index = 0, horizontal = False)

    # radio_encoding = st.radio("Recherche", ["exacte", "sémantique"], index = 0, horizontal = False)

    # st.markdown("-----")
    # st.markdown("<span class='white-anchor' style='display:none'></span>", unsafe_allow_html=True)

    # display_Button = st.checkbox("Bouton afficher", value = display_Button)

    with st.container():
        st.markdown("<span class='white-anchor' style='display:none'></span>", unsafe_allow_html=True)
        st.write("Rechercher dans :")
        with st.container():
            filter_acap = st.checkbox(r"ACAP", True)
            filter_car = st.checkbox(r"CAR", True)
            filter_uga = st.checkbox(r"UGA", True)
            filter_usp = st.checkbox(r"USP", True)
            filter_communs = st.checkbox(r"Commun", True)

    nb_documents = st.slider("Nombre de documents", 0, 100, 20)
    # radio_pdf = st.radio("Aperçu : ", ['1', '2'], index = 0, horizontal = True)

    st.markdown("""<div>📕 PDF<br>📘 Word<br>📙 PowerPoint<br>📗 Excel</div>""", unsafe_allow_html = True)
    st.markdown("""<div/>""", unsafe_allow_html = True)


def on_click_preview(item):
    st.session_state.selected_doc = item


def get_filters():
    lst = []
    if filter_acap: lst.append(r'ACAP')
    if filter_car: lst.append(r'CAR')
    if filter_uga: lst.append(r'UGA')
    if filter_usp: lst.append(r'USP')
    if filter_communs: lst.append(r'Commun')
    return lst

# filters = get_filters()


# --------------------------------
#  Main
#

def main():

    search_button, query = '', ''

    # Initialisation de l'état de session
    if 'results' not in st.session_state:
        st.session_state.results = None

    if "selected_doc" not in st.session_state:
        st.session_state.selected_doc = None
    
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    # Section de recherche
    with st.container():
        # st.markdown('<div class="search-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            search_text = st.text_input("", placeholder="Entrez votre requête de recherche...", 
                                    label_visibility="collapsed")
        with col2:
            search_button = st.button("Rechercher", type="primary", use_container_width=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    results = []
    if search_button:
        # st.session_state.counter += 1
        # st.write("Counter: ", st.session_state.counter)

        if search_text.strip():
            top_k = nb_documents
            query = [search_text]
            results = tfidf_search(query, top_k = top_k, threshold = threshold)

            if len(results) == 0:
                st.session_state.results = None
                st.warning("Aucun résultat trouvé pour votre recherche.")
            else:
                st.session_state.results = results
        else:
            st.session_state.results = None
        st.session_state.selected_doc = None

    if st.session_state.results != None:
        col1, col2 = st.columns([2, 3], gap='small')

        with col1:

            filters = get_filters()
            counter = 0
            for item in st.session_state.results:
                id = item["index"]
                unit = df_data.Unit[id].strip()

                if not unit in filters:
                    continue

                score = int(100 * item["score"])
                if score < 2:
                    break
                extension = df_data.Extensions[id].strip().lower()
                author, date = "", ""
                counter += 1

                if pd.isna(df_data.Author[id]) or df_data.Author[id].strip() == '':
                    author = 'N/R'
                else:
                    author = df_data.Author[id].strip()

                if pd.isna(df_data.Date[id]) or df_data.Date[id].strip() == '':
                    date = 'N/R'
                else:
                    date = df_data.Date[id].strip()
                    if extension != 'pdf':
                        date = date[:10]

                st.markdown('<class id="button-after">Test</class>', unsafe_allow_html=True)
                st.button(f"{dict_type_icon[extension]}**{df_data.Titles.to_list()[id].strip()}**\n &nbsp;\
                        Auteur : {author} &nbsp;&nbsp;&nbsp;\
                        Date : {date} &nbsp;&nbsp;&nbsp;\
                        Score : {score} % &nbsp;&nbsp;&nbsp;\
                        Unité : {unit}",\
                        key = f"add_{item['index']}",
                        on_click = on_click_preview, args = [item])

                if counter == nb_documents:
                    break

        with col2:

            if st.session_state.selected_doc != None:

                id = st.session_state.selected_doc["index"]
                col3, col4 = st.columns([5, 1], gap='small')

                with col3:
                    st.info(f"**Document sélectionné** : {df_data.Titles[id].strip()}")
                    st.info(f"**Chemin** : {df_data.Path[id].strip()}")

                path = df_data.Path[id]

                with col4:
                    # We check if file exists
                    test_path = Path(f"{df_data.Path[id].strip()}{df_data.Titles[id].strip()}.{df_data.Extensions[id]}")

                    if test_path.exists():                        
                        with open(path + f"{df_data.Titles[id]}.{df_data.Extensions[id]}", "rb") as file:
                            btn = st.download_button(
                                label="📥 Télécharger",
                                data=file,
                                file_name=f"{df_data.Titles[id]}.{df_data.Extensions[id]}",
                                mime="application/pdf"
                            )
                    else:
                        st.info(f"**Fichier introuvable**")


                if df_data.Extensions[id].lower() != 'pdf':
                    path = path_temp_pdf + f"{df_data.Hash[id]}.pdf"
                    # path = path_temp_pdf
                else:
                    path += f"{df_data.Titles[id]}.pdf"

                # We check if file exists
                if Path(path).exists():
                    if radio_pdf == '1':
                        show_pdf(path)
                    else:
                        show_pdf_2(path)

                else:
                    st.info(f"**Aperçu non disponible**")


if __name__ == '__main__':
    main()
