"""
    Class ParamConversion
    Class Conversion

    ...
"""




import os
import time
import logging
from typing import List, Dict

import pandas as pd

# import pdfplumber
# import pymupdf # Allows to add key-words to the document as metadata
# from pptx import Presentation
# from docx import Document
from docx2pdf import convert as convert_docx
from pptxtopdf import convert as convert_pptx
# from openpyxl import load_workbook
from win32com import client



class ParamConversion:
    ''' Paramètres de conversion '''
    path:str = ""
    path_temp_pdf:str = ""
    max_files:int = 1000
    verbose:int = 0
    lst_filetypes:List[str] = []
    logger:logging.Logger = None


class Conversion:

    def __init__(self, param:ParamConversion, df_old:pd.DataFrame = None):
        ''' Initialise l'objet Extraction '''
        self.set_param(param)
        self._path_temp_pdf:str = ""
        self._list_not_converted:List = []
        self._list_converted:List = []
        self._list_xlsm_problems:List = []
        self._df_old:pd.DataFrame = df_old
        self._lst_needed_pdf:List[str] = []
        self._verbose:int = 0


    def set_param(self, param:ParamConversion):
        param.lst_filetypes = [item.lower() for item in param.lst_filetypes]
        self._param = param
        print(param.path_temp_pdf)
        print(self._param.path_temp_pdf)

    def print_list_not_converted(self):
        print("--- Fichiers non convertis :")
        if self._list_not_converted:
            for item in self._list_not_converted:
                print(f'Document : "{item}"')

    def print_list_converted(self):
        print("--- Fichiers convertis :")
        if self._list_converted:
            for document in self._list_converted:
                print(f'Document : "{document.path}{document.title}.{document.extension}"')

    def create_temp_directory(self) -> bool:
        ''' Create temporary directory to put converted pdf files. '''

        if self._param.path_temp_pdf == '':
            self._param.path_temp_pdf = f"{self._param.path}../_TEMP_PDF/"

        if os.path.exists(self._param.path_temp_pdf):
            print(f"répertoire {self._param.path_temp_pdf} déjà existant")
            return True

        try:
            os.mkdir(self._param.path_temp_pdf)
            print(f'Création du dossier : "{self._param.path_temp_pdf}"')
            self._param.logger.info(f'Création du dossier : "{self._param.path_temp_pdf}"')
            return True
        except PermissionError:
            print(f'Permission refusée : impossible de créer : "{self._param.path_temp_pdf}"')
            self._param.logger.error(f'Permission refusée : impossible de créer : "{self._param.path_temp_pdf}"')
            return False
        except Exception as e:
            print(f"ERROR: {e}")
            self._param.logger.error(f"Impossible de créer le dossier : {self._param.path_temp_pdf}")
            return False
    
    def convert_pptx_to_pdf(self, index):
        ''' convert pptx document to pdf

            Arg:
            - path: full path of file to convert (C:/Documents/..../)
            - filename : name of file + extension (filename.pptx).
        '''
        assert self._df_old.Extensions[index] == 'pptx'
        filename = f'{self._df_old.Titles[index]}.pptx'
        path = self._df_old.Path[index]
        pdf_filename = f'{self._df_old.Titles[index]}.pdf'
        hash_name = f'{self._df_old.Hash.iloc[index]}.pdf'

        try:
            convert_pptx(path + filename, self._param.path_temp_pdf)
            self._param.logger.info(f"Converted to PDF: {path + filename}")
            self._list_converted.append(path + filename)
        except Exception as e:
            # print("Exception: ", e)
            self._list_not_converted.append(path + filename)
            print(f"Cannot convert file {filename} to PDF")
            self._param.logger.error(f"Cannot convert file {filename} to PDF")

        try:
            time.sleep(.5)
            os.rename(f"{self._param.path_temp_pdf}{pdf_filename}", f"{self._param.path_temp_pdf}{hash_name}")
            # print(f'Added FILE: {hash_name}')
        except Exception as e:
            # print("Exception: ", e)
            print(f"Cannot rename file {filename}")
            self._param.logger.error(f"Cannot rename file {filename}")

            try:
                os.remove(f"{self._param.path_temp_pdf}{pdf_filename}")
            except Exception as e:
                print(f"Cannot remove file {self._param.path_temp_pdf}{pdf_filename}")
                self._param.logger.error(f"Cannot remove file {self._param.path_temp_pdf}{pdf_filename}")


    def convert_docx_to_pdf(self, index) -> bool:
        ''' convert docx document to pdf

            Arg:
            - path: full path of file to convert (C:/Documents/..../)
            - filename : name of file + extension (filename.docx).
        '''
        assert self._df_old.Extensions[index] == 'docx'
        filename = f'{self._df_old.Titles[index]}.docx'
        path = self._df_old.Path[index]
        hash_name = f'{self._df_old.Hash.iloc[index]}.pdf'
        # pdf_filename = filename[:-5] + ".pdf"
        st_input = path + filename
        st_output = self._param.path_temp_pdf + hash_name
        try:
            convert_docx(st_input, st_output)
            self._param.logger.info(f"Converted to PDF: {path + filename}")
            self._list_converted.append(st_input)
            return True
        except Exception as e:
            # print("Exception: ", e)
            print(f"Cannot convert file {filename} to PDF")
            self._param.logger.error(f"Cannot convert file {filename} to PDF")
            self._list_not_converted.append(st_input)
            return False

    def convert_xlsx_and_xlsm_to_pdf_2(self, path, filename):
        ''' convert xlsx and xlsm document to pdf
        
            Arg:
            - path: full path of file to convert (C:/Documents/..../)
            - filename : name of file + extension (filename.xlsx).
        '''
        # Not working for some files ... (it seems like macros and vba should be deactivated before ...)
        assert False
        assert filename[-4:] in ["xlsx", "xlsm"]
        pdf_filename = filename[:-5] + ".pdf"
        st_input = path + filename
        st_output = self._param.path_temp_pdf + pdf_filename
        print("Input: ", st_input)
        print("Output:", st_output)
        try:
            excel = client.Dispatch("Excel.Application")
            sheets = excel.Workbooks.Open(st_input)
            work_sheets = sheets.Worksheets[0]
            work_sheets.ExportAsFixedFormat(0, st_output)
            sheets.Close()
            excel.Quit()
            print(f"FILE {path + filename} converted to PDF")
            self._list_converted.append(path + filename)
        except:
            self._list_not_converted.append(st_input)
            print(f"Cannot convert file {filename} to PDF")

    def convert_xlsx_and_xlsm_to_pdf(self, index):
        ''' convert xlsx and xlsm document to pdf

            Arg:
            - path: full path of file to convert (C:/Documents/..../)
            - filename : name of file + extension (filename.xlsx).
        '''

        assert self._df_old.Extensions[index] in ['xlsx', 'xlsm']
        filename = f'{self._df_old.Titles[index]}.{self._df_old.Extensions[index]}'
        path = self._df_old.Path[index]
        hash_name = f'{self._df_old.Hash.iloc[index]}.pdf'

        from win32com.client import DispatchEx
        import pythoncom

        # pdf_filename = filename[:-5] + ".pdf"
        st_input = path + filename
        st_output = self._param.path_temp_pdf + hash_name

        try:
            xl = DispatchEx("Excel.Application")
            wb = xl.Workbooks.Open(st_input)
            pythoncom.PumpWaitingMessages()
            wb.ExportAsFixedFormat(0, st_output)
            xl.DisplayAlerts = False
            wb.Close()
            xl.Quit()
            self._param.logger.info(f"Converted to PDF: {path + filename}")
            self._list_converted.append(path + filename)

        except Exception as e:
            # print("Exception: ", e)
            print(f"Cannot convert file: {filename} to PDF")
            self._param.logger.error(f"Cannot convert file: {filename} to PDF")
            self._list_not_converted.append(st_input)

    def convert_documents(self) -> bool:
        ''' Scan directory and sub directories
            Create document for each file
        '''
        # Create temporary file to put pdf (Needs to be scanned before the process)
        if not self.create_temp_directory():
            return False

        # Conversion
        for index in self._df_old.index:
            if self._df_old.Extensions[index] == 'pdf':
                # Nothing to convert
                if self._param.verbose == 1:
                    print(f'PDF - Nothing to do: {self._df_old.Titles[index]}.{self._df_old.Extensions[index]}')
                self._param.logger.info(f"File already PDF: {self._df_old.Titles[index]}")

            else:
                if self._df_old.Has_changed[index].item(0):
                    # Need to convert
                    if self._param.verbose == 1:
                        print(f'Document has changed {self._df_old.Path[index]}{self._df_old.Titles[index]}.{self._df_old.Extensions[index]}')
                    self.convert_document(index)

                else:
                    # Check if the pdf already exists
                    if self._param.verbose == 1:
                        print(f'No changes {self._df_old.Path[index]}{self._df_old.Titles[index]}.{self._df_old.Extensions[index]}')

                    if f'{self._df_old.Hash[index]}.pdf' in os.listdir(self._param.path_temp_pdf):
                        # pdf already exists
                        if self._param.verbose == 1:
                            print("PDF already there")
                        self._param.logger.info(f"PDF Already there: {self._df_old.Titles[index]}")

                    else:
                        self.convert_document(index)
                self._lst_needed_pdf.append(self._df_old.Hash[index])
    
        return True

    def convert_document(self, index) -> bool:
        ''' Convert document into pdf '''

        print(f'Conversion of file: {self._df_old.Path[index]}{self._df_old.Titles[index]}.{self._df_old.Extensions[index]}')                    
        extension = self._df_old.Extensions[index]

        if extension == 'pptx':
            self.convert_pptx_to_pdf(index)

        elif extension == 'docx':
            self.convert_docx_to_pdf(index)

        elif extension in ['xlsx', 'xlsm']:
            self.convert_xlsx_and_xlsm_to_pdf(index)

        else:
            print("Do not convert this type of file")

        return True

    def clean_directory(self):
        ''' Delete pdf from TEMP directory in order to only keep needed PDF '''

        for file in os.listdir(self._param.path_temp_pdf):
            if file[:-4] not in self._lst_needed_pdf:
                try:
                    os.remove(f"{self._param.path_temp_pdf}{file}")
                except Exception as e:
                    print(f"Cannot remove file {self._param.path_temp_pdf}{file}")
                    self._param.logger.error(f"Cannot remove file {self._param.path_temp_pdf}{file}")


