"""

    Class ParamEncoding
    Class Encoding

    
"""





import logging
import scipy as sp
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# from sentence_transformers import SentenceTransformer
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.text_splitter import PythonCodeTextSplitter

# import chromadb




class ParamEncoding:
    ''' Paramètres de conversion '''
    use_title_and_path:bool = False # Parameter to take account the path in the search
    logger:logging.Logger = None


class Encoding():

    def __init__(self, df_no_accent:pd.DataFrame,
                 param:ParamEncoding = None):
        self.df_no_accent = df_no_accent
        assert all([item in self.df_no_accent.columns for item in [
            'Extensions', 'Titles', 'Author', 'Date', 'Path', 'Unit', 'Hash',
            'Has_changed', 'Texts_no_accent', 'Titles_no_accent'
        ]])
        self._param = param
        if self._param.use_title_and_path:
            assert 'Titles_And_Path_Words_no_accent' in self.df_no_accent.columns

    def tfidf(self):
        ''' TF-IDF Process '''
        self._param.logger.info(f'TF-IDF Encoding')

        texts_no_accent = self.df_no_accent.Texts_no_accent
        titles_no_accent = self.df_no_accent.Titles_no_accent

        vectorizer_texts = TfidfVectorizer()
        vectorizer_titles = TfidfVectorizer()

        tfidf_matrix_texts = vectorizer_texts.fit_transform(texts_no_accent)
        tfidf_matrix_titles = vectorizer_titles.fit_transform(titles_no_accent)

        filename = f"VECTORS/tfidf_matrix_titles.npz"
        sp.sparse.save_npz(filename, tfidf_matrix_titles)
        self._param.logger.info(f'Matrix {filename} Saved')

        filename = f"VECTORS/tfidf_matrix_texts.npz"
        sp.sparse.save_npz(filename, tfidf_matrix_texts)
        self._param.logger.info(f'Matrix {filename} Saved')

        filename = f"VECTORS/tfidf_vectorizer_titles.pkl"
        with open(filename, 'wb') as file:
            pickle.dump(vectorizer_titles, file)
        self._param.logger.info(f'Vectorizer {filename} Saved')

        filename = f"VECTORS/tfidf_vectorizer_texts.pkl"
        with open(filename, 'wb') as file:
            pickle.dump(vectorizer_texts, file)
        self._param.logger.info(f'Vectorizer {filename} Saved')

        if self._param.use_title_and_path:
            titles_paths_no_accent = self.df_no_accent.Titles_And_Path_Words_no_accent
            vectorizer_titles_paths = TfidfVectorizer()
            tfidf_matrix_titles_paths = vectorizer_titles_paths.fit_transform(titles_paths_no_accent)
            filename = f"VECTORS/tfidf_matrix_titles_paths.npz"
            sp.sparse.save_npz(filename, tfidf_matrix_titles_paths)

            filename = f"VECTORS/tfidf_vectorizer_titles_paths.pkl"
            with open(filename, 'wb') as file:
                pickle.dump(vectorizer_titles_paths, file)

