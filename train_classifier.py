
# import os
# import re
# import spacy
import scipy as sp
import pandas as pd
# import pdfplumber
# from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, precision_score
import pickle
from tools import cleaning_process, extract_text_from_all_docs, init_nlp, remove_stopwords_punct, chunks_texts


# def extract_text_from_pdf(path_and_filename:str) -> str:
#     text = ""
#     with pdfplumber.open(path_and_filename) as pdf:
#         for i, page in enumerate(pdf.pages):
#             current_text = page.extract_text()
#             text += ' ' + current_text.strip()
#     return text

# def clean_folder_path(text):
#     return re.sub(r"/^([a-zA-Z]:\\)([-\u4e00-\u9fa5\w\s.()~!@#$%^&()\[\]{}+=]+\\)*$/gm", ' ', text)

# def clean_spaces_and_line_terminator(text):
#     text = text.replace('\n', ' ')
#     return re.sub(r" +", ' ', text).strip()

# def clean_XXX(text):
#     return re.sub(r"x{2,}", ' ', text)

# def clean_special_char(text):
#     text = re.sub(r"…", '.', text)
#     text = text.replace('.', ' ')
#     text = text.replace(',', ' ')
#     text = text.replace('-', ' ')
#     text = text.replace('_', ' ')
#     text = text.replace('(', ' ')
#     text = text.replace(')', ' ')
#     text = text.replace('[', ' ')
#     text = text.replace(']', ' ')
#     text = text.replace('?', ' ')
#     text = text.replace('!', ' ')
#     text = text.replace('%', ' ')
#     text = text.replace('<', ' ')
#     text = text.replace('>', ' ')
#     text = text.replace('<', ' ')
#     text = text.replace('«', ' ')
#     text = text.replace('»', ' ')
#     text = text.replace('€', ' ')
#     # text = text.replace('’', ' ')
#     # return re.sub(r"\.{1,}", '.', re.sub(r"…", '.', text))
#     return text

# def clean_slashes(text):
#     text = text.replace('/', ' ')
#     return text.replace('\\', ' ')
    
# def cleaning_process(text):
#     text = text.lower()
#     text = clean_folder_path(text)
#     text = clean_special_char(text)
#     text = clean_XXX(text)
#     text = clean_slashes(text)
#     return clean_spaces_and_line_terminator(text)

# def extract_text_from_all_docs(path, nb_max = 10):
#     lst_texts = []
#     lst_titles = []
#     for i, item in enumerate(os.listdir(path)):
#         if i == nb_max:
#             break
#         print(item)
#         text = extract_text_from_pdf(path + '\\' + item)
#         if len(text.strip()) > 0:
#             lst_texts.append(text)
#             lst_titles.append(item)
#     return pd.DataFrame.from_dict({
#         'Titles': lst_titles,
#         'Texts': lst_texts,
#         })

# def init_nlp():
#     df_sw = pd.read_csv('CSV/stopwords-fr_CUSTOM.csv')
#     nlp = spacy.load("fr_core_news_md")
#     nlp.Defaults.stop_words.clear()
#     nlp.Defaults.stop_words |= {word for word in df_sw.values.flatten().tolist()}
#     return nlp

# def remove_stopwords_punct(text):
#     doc = nlp(text)
#     # for token in doc:
#     #     print(token.text, token.lemma_, token.is_stop)
#     temp = [token for token in doc if not (token.is_stop or token.is_punct or token.is_digit or token.is_currency)]
#     return [unidecode(token.lemma_) for token in temp if len(token.lemma_) > 2]

# def chunks_texts(df):
#     set_data = set()
#     for i, row in df.iterrows():
#         lst = row['Texts_Token']
#         for size in range(2, 8):
#             for j in range(len(lst) - size + 1):
#                 extract = ' '.join(set(lst[j:j+size]))
#                 set_data.add(extract)
#     return list(set_data)



# ---------------------------
# MAIN
# ---------------------------

nlp = init_nlp()

nb_max_docs = 1
nb_max_chunks = 50


print("Extractig texts from ASSURANCE documents")
path1 = "DOC ASSURANCE - Copie"
df = extract_text_from_all_docs(path1, nb_max_docs)

print("Cleaning texts")
df_cleaned = df.copy()
df_cleaned['Texts_Cleaned']  = df_cleaned['Texts'].apply(cleaning_process)
df_cleaned.drop(columns = ['Texts'], inplace = True)

print("Tokenization")
df_token = df_cleaned.copy()
df_token['Texts_Token']  = df_token['Texts_Cleaned'].apply(remove_stopwords_punct)
df_token.drop(columns = ['Texts_Cleaned'], inplace = True)

print("================ Create Data ================")

print("1. From ASSURANCE documents")
set_data = chunks_texts(df_token)
lst_data = list(set_data)[:nb_max_chunks]
print(lst_data[:10])
print("Length Data:", len(lst_data))
labels = [1] * len(lst_data)

print("Extractig texts from NO ASSURANCE documents")
path2 = "DOC NO ASSURANCE"
df = extract_text_from_all_docs(path2, nb_max_docs)

print("Cleaning texts")
df_cleaned = df.copy()
df_cleaned['Texts_Cleaned']  = df_cleaned['Texts'].apply(cleaning_process)
df_cleaned.drop(columns = ['Texts'], inplace = True)

print("Tokenization")
df_token = df_cleaned.copy()
df_token['Texts_Token']  = df_token['Texts_Cleaned'].apply(remove_stopwords_punct)
df_token.drop(columns = ['Texts_Cleaned'], inplace = True)

print("2. From NO ASSURANCE documents")
set_data = chunks_texts(df_token)
lst_temp = list(set_data)[:nb_max_chunks]
print(lst_temp[:10])
print("Length Data:", len(lst_temp))
lst_data.extend(lst_temp)
labels.extend([0] * len(lst_temp))
print("Length Data:  ", len(lst_data))
print("Length Labels:", len(labels))

df_data = pd.DataFrame.from_dict({
    'Texts': lst_data,
    'Labels': labels,
    })

# Vectorization
vectorizer = TfidfVectorizer()
tfidf_texts_matrix = vectorizer.fit_transform(df_data.Texts)
print("X.shape:", tfidf_texts_matrix.shape)

# Save the vectorizer and the matrix
filename = f"VECTORS/X_texts.npz"
sp.sparse.save_npz(filename, tfidf_texts_matrix)

filename = f"VECTORS/vectorizer_ia_texts.pkl"
with open(filename, 'wb') as file:
    pickle.dump(vectorizer, file)
    
# Split the data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(tfidf_texts_matrix, df_data.Labels, test_size=0.2, random_state=42)

# Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model
filename = f"VECTORS/reglog_ia_texts.pkl"
with open(filename, 'wb') as file:
    pickle.dump(model, file)

print("Model Score:", model.score(X_test, y_test))
# print("Model Accuracy:", model.accuracy_score(X_test, y_test))

y_pred = model.predict(X_train)
print("Training Accuracy", accuracy_score(y_train, y_pred))
print("Training Precision", precision_score(y_train, y_pred))
print("Training Recall", recall_score(y_train, y_pred))

# Predicting with a validation dataset
y_pred = model.predict(X_test)
print("Test Accuracy", accuracy_score(y_test, y_pred))
print("Test Precision", precision_score(y_test, y_pred))
print("Test Recall", recall_score(y_test, y_pred))

# test 1
phrase = ["je dois déclarer un sinistre"]
X_test = vectorizer.transform(phrase)
prediction = model.predict(X_test)
print("Assurance ?" , prediction[0])

# test 2
phrase = ["recette de cuisine"]
X_test = vectorizer.transform(phrase)
prediction = model.predict(X_test)
print("Assurance ?" , prediction[0])