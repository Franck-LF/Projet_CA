import os
import datetime
import pandas as pd
import pdfplumber

def extract_text_from_pdf(path_and_filename:str) -> str:
    text, author, modDate = "", "", ""
    with pdfplumber.open(path_and_filename) as pdf:
        for i, page in enumerate(pdf.pages):
            current_text = page.extract_text()
            text += ' ' + current_text.strip()
    return text

now = datetime.datetime.now()

nb_files = 500
path1 = "DOC ASSURANCE - Copie"
path2 = "DOC NO ASSURANCE"

for item in os.listdir(path1):
    print(item)
    print(extract_text_from_pdf(path1 + '\\' + item))
    break