import scipy as sp
import pandas as pd

import pickle
from tools import cleaning_process, extract_text_from_all_docs, init_nlp, remove_stopwords_punct, chunks_texts


text = "Mes recettes à base de chocolat"

df = pd.DataFrame.from_dict({
    'Texts': [text]
    })

print(df)

df['Texts_Cleaned']  = df['Texts'].apply(cleaning_process)
df['Texts_Token']  = df['Texts_Cleaned'].apply(remove_stopwords_punct)

print(df)
print("Token:", df.Texts_Token.values[0])
print(' '.join(df.Texts_Token.values[0]))