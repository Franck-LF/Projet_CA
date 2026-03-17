import os
# import re
import spacy
import pandas as pd
import pdfplumber
from unidecode import unidecode
from typing import List



def extract_text_from_pdf(path_and_filename:str) -> str:
    text = ""
    with pdfplumber.open(path_and_filename) as pdf:
        for i, page in enumerate(pdf.pages):
            current_text = page.extract_text()
            text += ' ' + current_text.strip()
    return text

def clean_folder_path(text:str) -> str:
    return str
    return re.sub(r"/^([a-zA-Z]:\\)([-\u4e00-\u9fa5\w\s.()~!@#$%^&()\[\]{}+=]+\\)*$/gm", ' ', text)

def clean_spaces_and_line_terminator(text:str) -> str:
    text = text.replace('\n', ' ')
    return str
    return re.sub(r" +", ' ', text).strip()

def clean_XXX(text:str) -> str:
    return str
    return re.sub(r"x{2,}", ' ', text)

def clean_special_char(text:str) -> str:
    return str
    text = re.sub(r"…", '.', text)
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace('?', ' ')
    text = text.replace('!', ' ')
    text = text.replace('%', ' ')
    text = text.replace('<', ' ')
    text = text.replace('>', ' ')
    text = text.replace('<', ' ')
    text = text.replace('«', ' ')
    text = text.replace('»', ' ')
    text = text.replace('€', ' ')
    # text = text.replace('’', ' ')
    # return re.sub(r"\.{1,}", '.', re.sub(r"…", '.', text))
    return text

def clean_slashes(text:str) -> str:
    text = text.replace('/', ' ')
    return text.replace('\\', ' ')
    
def cleaning_process(text:str) -> str:
    text = text.lower()
    text = clean_folder_path(text)
    text = clean_special_char(text)
    text = clean_XXX(text)
    text = clean_slashes(text)
    return clean_spaces_and_line_terminator(text)

def extract_text_from_all_docs(path:str, nb_max:int = 10) ->pd.DataFrame:
    lst_texts = []
    lst_titles = []
    for i, item in enumerate(os.listdir(path)):
        if i == nb_max:
            break
        print(item)
        text = extract_text_from_pdf(path + '\\' + item)
        if len(text.strip()) > 0:
            lst_texts.append(text)
            lst_titles.append(item)
    return pd.DataFrame.from_dict({
        'Titles': lst_titles,
        'Texts': lst_texts,
        })

def init_nlp():
    df_sw = pd.read_csv('CSV/stopwords-fr_CUSTOM.csv')
    nlp = spacy.load("fr_core_news_md")
    nlp.Defaults.stop_words.clear()
    nlp.Defaults.stop_words |= {word for word in df_sw.values.flatten().tolist()}
    return nlp

nlp = init_nlp()
# print(nlp.Defaults.stop_words)

def remove_stopwords_punct(text:str) -> List[str]:
    doc = nlp(text)
    # for token in doc:
    #     print(token.text, token.lemma_, token.is_stop)
    temp = [token for token in doc if not (token.is_stop or token.is_punct or token.is_digit or token.is_currency)]
    return [unidecode(token.lemma_) for token in temp if len(token.lemma_) > 2]

def chunks_texts(df:pd.DataFrame) -> List:
    set_data = set()
    for i, row in df.iterrows():
        lst = row['Texts_Token']
        for size in range(2, 8):
            for j in range(len(lst) - size + 1):
                extract = ' '.join(set(lst[j:j+size]))
                set_data.add(extract)
    return list(set_data)