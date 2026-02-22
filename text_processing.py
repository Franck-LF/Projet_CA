"""

    Class ParamTextProcessing
    Class TextProcessing
    
"""



import re
import logging
from typing import List
import pandas as pd
from unidecode import unidecode
import spacy


class ParamTextProcessing:
    ''' Paramètres de conversion '''
    use_title_and_path:bool = False # Parameter to take account the path in the search
    logger:logging.Logger = None


class TextProcessing():
    '''' Class to clean the data '''

    def __init__(self, df_data:pd.DataFrame,
                 param:ParamTextProcessing = None,
                 indexes:List = None):
        ''' Initialize Cleaning class '''
        self.df_data:pd.DataFrame = df_data.copy()
        self.df_cleaned:pd.DataFrame = None
        self.df_token:pd.DataFrame = None
        self.df_lemm:pd.DataFrame = None
        self.df_no_accent:pd.DataFrame = None
        self.nlp = None
        self.init_nlp()
        self._param = param
        self._indexes:List = None

        if indexes:
            self._indexes:List = indexes
        else:
            self._indexes:List = list(range(df_data.shape[0]))

    def init_nlp(self):
        df_sw = pd.read_csv('CSV/stopwords-fr_CUSTOM.csv')
        self.nlp = spacy.load("E:\\YBP10\\ApachePub_Php8\\PPB\\bibliotheque-ABP\\fr_core_news_md-3.8.0\\fr_core_news_md\\fr_core_news_md-3.8.0\\")
        self.nlp.Defaults.stop_words.clear()
        self.nlp.Defaults.stop_words |= {word for word in df_sw.values.flatten().tolist()}


    @staticmethod
    def lower(text):
        return text.lower()

    @staticmethod
    def clean_text(text):
        text = text.replace('\n', ' ').replace('_', ' ')
        return re.sub(' +', ' ', text)

    @staticmethod
    def clean_special_char(text):
        """ Remove special characters
            (We should also remove: $&#@+ ???)
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
        # return re.sub(r"\.{1,}", '.', re.sub(r"…", '.', text))
        return text

    @staticmethod
    def clean_XXX(text):
        return re.sub(r"x{2,}", ' ', text)

    @staticmethod
    def clean_folder_path(text):
        # ISSUE: does not work for: s:\dab-abp-car\equip\02 (because not ending by \):
        return re.sub(r"/^([a-zA-Z]:\\)([-\u4e00-\u9fa5\w\s.()~!@#$%^&()\[\]{}+=]+\\)*$/gm", ' ', text)
        # ISSUE: it removes also all texts starting with '\':
        return re.sub(r".+(?=\\)", ' ', text)

    @staticmethod
    def clean_spaces_and_line_terminator(text):
        # text = text.replace('\n{2,}', ' ')
        text = text.replace('\n', ' ')
        return re.sub(r" +", ' ', text).strip()

    @staticmethod
    def clean_slashes(text):
        ''' replace slashes when surrounded by spaces '''
        text = text.replace(' / ', ' ')
        return text.replace(' \\ ', ' ')

    @staticmethod
    def cleaning_process(text):
        text = TextProcessing.lower(text)
        text = TextProcessing.clean_folder_path(text)
        text = TextProcessing.clean_special_char(text)
        text = TextProcessing.clean_XXX(text)
        text = TextProcessing.clean_slashes(text)
        return TextProcessing.clean_spaces_and_line_terminator(text)

    def remove_stopwords_punct_digit(self, text):
        doc = self.nlp(text)
        return [token for token in doc if not (token.is_stop or token.is_punct or token.is_digit)]

    def remove_stopwords_punct(self, text):
        doc = self.nlp(text)
        return [token for token in doc if not (token.is_stop or token.is_punct)]

    @staticmethod
    def remove_duplicate_words(text):
        return ' '.join(set(text.split(' ')))

    @staticmethod
    def rebuilder_EX(doc):
        text = ' '.join([token.text for token in doc])
        return re.sub(' +', ' ', text).strip()

    @staticmethod
    def lemmatizer_EX(doc):
        text = ' '.join([token.lemma_ for token in doc])
        return re.sub(' +', ' ', text).strip()

    @staticmethod
    def add_path_words(path):
        lst = path.split('BIBLIOTHEQUE')
        assert len(lst) == 2
        return ' '.join([item.strip() for item in lst[1].split('\\') if item.strip()])

    def process_cleaning(self):
        ''' Cleaning titles and texts for TF-IDF encoding '''
        assert all(self.df_data != None)
        self._param.logger.info(f'--- Cleaning Text ---')
        self.df_cleaned = self.df_data.copy()

        self.df_cleaned['Titles_Cleaned'] = self.df_cleaned['Titles'].apply(TextProcessing.cleaning_process)
        self.df_cleaned['Texts_Cleaned']  = self.df_cleaned['Texts'].apply(TextProcessing.cleaning_process)

        if self._param.use_title_and_path:
            self.df_cleaned['Titles_And_Path_Words_Cleaned'] = self.df_cleaned['Titles_And_Path_Words'].apply(TextProcessing.cleaning_process)
            self.df_cleaned.drop(columns = ['Titles_And_Path_Words', 'Texts'], inplace = True)
        else:
            self.df_cleaned.drop(columns = ['Texts'], inplace = True)


    def process_tokenization(self):
        ''' Tokenization of titles and texts
            At the same time we remove stop words and punctuation
        '''
        assert all(self.df_cleaned != None)
        self._param.logger.info(f'--- Tokenization ---')
        self.df_token = self.df_cleaned.copy()
        self.df_token['Titles_Token'] = self.df_token['Titles_Cleaned'].apply(self.remove_stopwords_punct)
        self.df_token['Texts_Token']  = self.df_token['Texts_Cleaned'].apply(self.remove_stopwords_punct)

        if self._param.use_title_and_path:
            self.df_token['Titles_And_Path_Words_Token'] = self.df_token['Titles_And_Path_Words_Cleaned'].apply(self.remove_stopwords_punct)
            self.df_token.drop(columns = ['Titles_Cleaned', 'Titles_And_Path_Words_Cleaned', 'Texts_Cleaned'], inplace = True)
        else:
            self.df_token.drop(columns = ['Titles_Cleaned', 'Texts_Cleaned'], inplace = True)

    def process_lemmatization(self):
        ''' Lemmatization of titles and texts '''

        assert all(self.df_token != None)
        self._param.logger.info(f'--- Lemmatization ---')
        self.df_lemm = self.df_token.copy()

        self.df_lemm['Titles_Lemm'] = self.df_lemm['Titles_Token'].apply(TextProcessing.lemmatizer_EX)
        
        # We add the 'normal' title to the lemmatized title because some words (but very few) should not be lemmatized (Agira ...).
        self.df_lemm['Titles_Lemm'] = self.df_lemm['Titles_Lemm'] + ' ' + self.df_lemm['Titles_Token'].apply(TextProcessing.rebuilder_EX)
        self.df_lemm['Titles_Lemm'] = self.df_lemm['Titles_Lemm'].apply(TextProcessing.remove_duplicate_words)

        # Lemmatization of the texts
        self.df_lemm['Texts_Lemm'] = self.df_lemm['Texts_Token'].apply(TextProcessing.lemmatizer_EX)

        if self._param.use_title_and_path:
            # Same proces for 'Titles_And_Path_Words' than for 'Titles'
            self.df_lemm['Titles_And_Path_Words_Lemm'] = self.df_lemm['Titles_And_Path_Words_Token'].apply(TextProcessing.lemmatizer_EX)
            self.df_lemm['Titles_And_Path_Words_Lemm'] = self.df_lemm['Titles_And_Path_Words_Lemm'] + ' ' + self.df_lemm['Titles_And_Path_Words_Token'].apply(TextProcessing.rebuilder_EX)
            self.df_lemm['Titles_And_Path_Words_Lemm'] = self.df_lemm['Titles_And_Path_Words_Lemm'].apply(TextProcessing.remove_duplicate_words)
            self.df_lemm.drop(columns=['Titles_Token', 'Titles_And_Path_Words_Token', 'Texts_Token'], inplace = True)

        else:
            self.df_lemm.drop(columns=['Titles_Token', 'Texts_Token'], inplace = True)

    def process_accents(self):
        ''' Removing accents of titles and texts '''
        assert all(self.df_lemm != None)
        self._param.logger.info(f'--- Accents Processing ---')
        self.df_no_accent = self.df_lemm.copy()
        self.df_no_accent['Texts_no_accent'] = self.df_no_accent['Texts_Lemm'].apply(unidecode)
        self.df_no_accent['Titles_no_accent'] = self.df_no_accent['Titles_Lemm'].apply(unidecode)

        if self._param.use_title_and_path:
            self.df_no_accent['Titles_And_Path_Words_no_accent'] = self.df_no_accent['Titles_And_Path_Words_Lemm'].apply(unidecode)
            self.df_no_accent.drop(columns=['Titles_Lemm', 'Titles_And_Path_Words_Lemm', 'Texts_Lemm'], inplace = True)

        else:
            self.df_no_accent.drop(columns=['Titles_Lemm', 'Texts_Lemm'], inplace = True)


    def process_full(self):
        ''' Proceed to the titles and texts process '''

        if self._param.use_title_and_path:
            # We add a column with all words contained in the file path.
            self.df_data["Titles_And_Path_Words"] = self.df_data['Titles'] + ' ' + \
                                self.df_data['Path'].apply(TextProcessing.add_path_words)

        self.process_cleaning()
        self.process_tokenization()
        self.process_lemmatization()
        self.process_accents()



