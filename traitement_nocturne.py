"""
    Main

"""



import os
import time
import datetime
import logging
import pandas as pd

from extraction import Extraction, ParamExtraction
from conversion import Conversion, ParamConversion
from text_processing import TextProcessing, ParamTextProcessing
from encoding import Encoding, ParamEncoding



if __name__ == '__main__':

    # ------------------------------
    #  PARAMATERS
    # ------------------------------
    
    nb_files = 500

    now = datetime.datetime.now()
    print('-' * 20 + ' START ' + '-' * 20)
    print(f"Date: {now.year:04} {now.month:02} {now.day:02}  --  {now.hour:02}h{now.minute:02}")

    # ------------------------------
    #  Logger
    # ------------------------------

    logging.basicConfig(filename=f"./LOGS/build_{now.year:04}-{now.month:02}-{now.day:02}_{now.hour:02}h{now.minute:02}.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('=' * 20 + " START PROCESS " + '=' * 20)

    # ------------------------------
    #  Checks
    # ------------------------------

    #if "LOGS" not in os.listdir():
    #    pass


    # ------------------------------
    #  Extraction
    # ------------------------------

    # Extraction Parameters
    param = ParamExtraction
    # param.path = "S:\\DAB-ABP\\Equip\\BIBLIOTHEQUE\\"
    # param.path = "C:\\Users\\S589669\\Documents\\DEV\\DOC MODIF\\"
    # param.path = "S:\\DAB-ABP\\RU-Animateurs-Analystes\\BIBLIOTHEQUE\\"
    # param.path = "\\CPCAPD2BURV2.zcam.ztech\CAP10BURS\DAB-ABP\RU-Animateurs-Analystes\\BIBLIOTHEQUE\\"
    # param.real_path = "S:\\DAB-ABP\\RU-Animateurs-Analystes\\BIBLIOTHEQUE\\"
    param.path = "C:\\Users\\Utilisateur\\Documents\\Projet_CA\\DOC ASSURANCE\\"

    param.lst_filetypes = [
        'pdf',
        'pptx',
        'docx',
        # 'doc',
        # 'xlsx',
        # 'xlsm',
        # 'xls',
        ]
    param.max_files = nb_files
    param.verbose = 1
    param.extract_text = True
    param.logger = logger


    df = None
    if 'df_data.csv' in os.listdir(".\\CSV"):
        print("Dossier CSV OK")
        df = pd.read_csv(".\\CSV\\df_data.csv", index_col = [0])
        print(f"-- Previous dataFrame -- shape: {df.shape}")

    extraction = Extraction(param, df)
    logger.info("Start Extraction")
    extraction.create_documents_from_directory()
    extraction.print_files_stats()

    df = extraction.to_dataframe()
    df.to_csv('CSV/df_data.csv')
    time.sleep(3)

    # ------------------------------
    #  Conversion
    # ------------------------------

    # Conversion Parameters
    del param
    param = ParamConversion
    # param.path_temp_pdf = "C:\\Users\\S589669\\Documents\\DEV\\_TEMP_PDF_TEST\\"
    # param.path_temp_pdf = "C:\\Users\\S589669\\Documents\\DEV\\_TEMP_PDF_MODIF\\"
    param.path_temp_pdf = "C:\\Users\\Utilisateur\\Documents\\Projet_CA\\TEMP_PDF\\"

    param.max_files = nb_files
    param.verbose = 0
    param.logger = logger

    conversion = Conversion(param, df)
    logger.info("Start Conversion")
    conversion.convert_documents()
    conversion.clean_directory()
    conversion.print_list_not_converted()
    time.sleep(3)

    # ------------------------------
    #  Text Processing
    # ------------------------------

    # Text processing Parameters
    del param
    param = ParamTextProcessing
    param.logger = logger
    text_processing = TextProcessing(df, param)
    logger.info("Start Text Processing")
    text_processing.process_full()
    df_text_processed = text_processing.df_no_accent
    #df_text_processed.to_csv("CSV/df_text_processed.csv")
    time.sleep(3)

    # ------------------------------
    #  Encoding
    # ------------------------------
    
    # Encoding Parameters
    del param
    param = ParamEncoding
    param.logger = logger
    encoding = Encoding(df_text_processed, param)
    logger.info("TF-IDF Encoding")
    encoding.tfidf()


    logger.info('=' * 20 + " END PROCESS " + '=' * 20)
    logging.shutdown()
    print('-' * 20 + ' END ' + '-' * 20)