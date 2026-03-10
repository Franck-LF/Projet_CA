
import os
import re
import spacy
import datetime
import pandas as pd
import pdfplumber
from unidecode import unidecode


def extract_text_from_pdf(path_and_filename:str) -> str:
    text, author, modDate = "", "", ""
    with pdfplumber.open(path_and_filename) as pdf:
        for i, page in enumerate(pdf.pages):
            current_text = page.extract_text()
            text += ' ' + current_text.strip()
    return text

def clean_folder_path(text):
    return re.sub(r"/^([a-zA-Z]:\\)([-\u4e00-\u9fa5\w\s.()~!@#$%^&()\[\]{}+=]+\\)*$/gm", ' ', text)

def clean_spaces_and_line_terminator(text):
    text = text.replace('\n', ' ')
    return re.sub(r" +", ' ', text).strip()

def clean_XXX(text):
    return re.sub(r"x{2,}", ' ', text)

def clean_special_char(text):
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
    # return re.sub(r"\.{1,}", '.', re.sub(r"…", '.', text))
    return text

def clean_slashes(text):
    text = text.replace(' / ', ' ')
    return text.replace(' \\ ', ' ')
    
def cleaning_process(text):
    text = text.lower()
    text = clean_folder_path(text)
    text = clean_special_char(text)
    text = clean_XXX(text)
    text = clean_slashes(text)
    return clean_spaces_and_line_terminator(text)

def extract_text_from_all_docs(path1, path2, texts, labels):
    for item in os.listdir(path1):
        print(item)
        text = extract_text_from_pdf(path1 + '\\' + item)
        if len(text.strip()) > 0:
            texts.append(text)
            labels.append(1)

    for item in os.listdir(path2):
        print(item)
        text = extract_text_from_pdf(path2 + '\\' + item)
        if len(text.strip()) > 0:
            texts.append(text)
            labels.append(0)

    df = pd.DataFrame.from_dict({
        'Texts': texts,
        'Labels': labels,
        })

    return df

def init_nlp():
    df_sw = pd.read_csv('CSV/stopwords-fr_CUSTOM.csv')
    nlp = spacy.load("fr_core_news_md")
    nlp.Defaults.stop_words.clear()
    nlp.Defaults.stop_words |= {word for word in df_sw.values.flatten().tolist()}
    return nlp

nlp = init_nlp()

def remove_stopwords_punct(text):
    print(f"remove_stopwords_punct : {text[:30]}...")
    doc = nlp(text)
    return [token for token in doc if not (token.is_stop or token.is_punct)]

def lemmatizer_EX(doc):
    text = ' '.join([token.lemma_ for token in doc])
    return re.sub(' +', ' ', text).strip() 



# ---------------------------
# MAIN
# ---------------------------

now = datetime.datetime.now()

nb_files = 500
path1 = "DOC ASSURANCE - Copie"
path2 = "DOC NO ASSURANCE"
texts = []
labels = []

df = None
df_cleaned = None
df_token = None
df_lem = None
df_accents = None

b_extraction = False
b_text_cleaning = True
b_tokenization = True
b_lemmatization = True
b_accents = True

if b_extraction:
    print("Extractig texts from documents")
    df = extract_text_from_all_docs(path1, path2, texts, labels)
    df.to_csv('CSV/df_data_ia.csv')

else:
    df = pd.read_csv('CSV/df_data_ia.csv', index_col = [0])

if b_text_cleaning:
    print("Cleaning texts")
    df_cleaned = df.copy()
    df_cleaned['Texts_Cleaned']  = df_cleaned['Texts'].apply(cleaning_process)
    df_cleaned.drop(columns = ['Texts'], inplace = True)
    df_cleaned.to_csv('CSV/df_data_ia_cleaned.csv')

else:
    df_cleaned = pd.read_csv('CSV/df_data_ia_cleaned.csv', index_col = [0])

if b_tokenization:
    print("Tokenization")
    df_token = df_cleaned.copy()
    df_token['Texts_Token']  = df_token['Texts_Cleaned'].apply(remove_stopwords_punct)
    df_token.drop(columns = ['Texts_Cleaned'], inplace = True)
    df_token.to_csv('CSV/df_data_ia_token.csv')

else:
    df_cleaned = pd.read_csv('CSV/df_data_ia_token.csv', index_col = [0])

if b_lemmatization:
    print("Lemmatization")
    df_lemm = df_cleaned.copy()
    df_lemm['Texts_Lemm'] = df_lemm['Texts_Token'].apply(lemmatizer_EX)
    df_lemm.drop(columns=['Texts_Token'], inplace = True)
    df_cleaned.to_csv('CSV/df_data_ia_lemm.csv')

else:
    df_lemm = pd.read_csv('CSV/df_data_ia_lemm.csv', index_col = [0])

if b_accents:
    print("Accents")
    df_no_accents = df_lemm.copy()
    df_no_accents['Texts_no_accent'] = df_no_accents['Texts_Lemm'].apply(unidecode)
    df_no_accents.drop(columns=['Texts_Lemm'], inplace = True)
    df_cleaned.to_csv('CSV/df_data_ia_no_accents.csv')

else:
    df_cleaned = pd.read_csv('CSV/df_data_ia_accents.csv', index_col = [0])



