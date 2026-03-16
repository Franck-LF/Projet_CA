import scipy as sp
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle
import mlflow
from tools import cleaning_process, extract_text_from_all_docs, init_nlp, remove_stopwords_punct, chunks_texts


nlp = init_nlp()

nb_max_docs = 1
nb_max_chunks = 10000


print("Extractig texts from ASSURANCE documents")
# path1 = "DOC ASSURANCE - Copie"
# df = extract_text_from_all_docs(path1, nb_max_docs)
text = "La simulation de crédit intégrant les caractéristiques de votre projet de financement."

df = pd.DataFrame.from_dict({
        'Titles': ["titre"],
        'Texts': [text],
        })

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
print("Total nb chunks:", len(set_data))
lst_data = list(set_data)[:nb_max_chunks]
print(lst_data)
