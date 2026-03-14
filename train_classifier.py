
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

nb_max_docs = 10
nb_max_chunks = 10000


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
print("Total nb chunks:", len(set_data))
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
print("Total nb chunks:", len(set_data))
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

# Save the data vectorized
filename = f"VECTORS/X_texts.npz"
sp.sparse.save_npz(filename, tfidf_texts_matrix)

# Save the vectorizer
filename = f"MODELS/vectorizer_ia_texts.pkl"
with open(filename, 'wb') as file:
    pickle.dump(vectorizer, file)
    
# Split the data into training and testing sets
from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(tfidf_texts_matrix, df_data.Labels, test_size=0.3, random_state=42)

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
print("MLFlow set_tracking OK")

# Create a new MLflow Experiment
mlflow.set_experiment("MLflow Quickstart")
print("MLFlow set_experiment OK")

# Start an MLflow run
with mlflow.start_run():

    # Set a tag that we can use to remind ourselves what this run was for
    mlflow.set_tag("Régression logistique pour la classification documentaire", "Documents Assurance")

    model = LogisticRegression()
    model.fit(X_train, y_train)
    print('Fit the Model OK')

    # Save the model
    filename = f"MODELS/reglog_ia_texts.pkl"
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

    # ------------------------- #
    #      Log the metrics      #
    # ------------------------- #

    print("Model Score:", model.score(X_test, y_test))
    # mlflow.log_metric("Model Score", accuracy_score(y_train, y_pred))

    y_pred = model.predict(X_train)
    print("Training Accuracy", accuracy_score(y_train, y_pred))
    print("Training Precision", precision_score(y_train, y_pred))
    print("Training Recall", recall_score(y_train, y_pred))
    mlflow.log_metric("Training Accuracy", accuracy_score(y_train, y_pred))
    mlflow.log_metric("Training Precision", precision_score(y_train, y_pred))
    mlflow.log_metric("Training Recall", recall_score(y_train, y_pred))

    # Predicting with a validation dataset
    y_pred = model.predict(X_test)
    print("Test Accuracy", accuracy_score(y_test, y_pred))
    print("Test Precision", precision_score(y_test, y_pred))
    print("Test Recall", recall_score(y_test, y_pred))
    mlflow.log_metric("Test Accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("Test Precision", precision_score(y_test, y_pred))
    mlflow.log_metric("Test Recall", recall_score(y_test, y_pred))

    mlflow.set_tag("Nb documents", nb_max_docs)
    mlflow.set_tag("Nb Chunks", nb_max_chunks)

    print("Log Metric OK")
    # mlflow.trace()

mlflow.end_run()
