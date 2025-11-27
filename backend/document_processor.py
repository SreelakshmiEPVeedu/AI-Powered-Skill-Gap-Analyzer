#backend/document_processor.py
import re    #regular expression module, here used for cleaning
import docx2txt   # library to extract text from docx file
import PyPDF2 #library to read and extract text from pdfs
from typing import Dict, Any 
'''provide datatype hints if it is any then it can take any value of any datatype'''

class DocumentProcessor:    #define a class 
    
    @staticmethod    #it doesn't need access to class variables like self
    def extract_text_from_pdf(file) -> str:
        try:
            '''creates an object, loads the file, decode the pdf and prepares pages properly'''
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""  # collects the extracted text from the file
            '''pdf_reader.pages=list-like object where each element=one PDF page object'''
            for page in pdf_reader.pages: 
                '''pdf_reader.pages gives a list of Page objects.Each element in that list 
                is an instance of PyPDF2._page.PageObject.the extract_text() is a method of 
                 this PageObject'''
                text += page.extract_text()
            return text
        except Exception as e:  #rasing exception if error in reading the file
            raise Exception(f"Error reading PDF: {str(e)}")
        
    @staticmethod
    def extract_text_from_docx(file) -> str:
        try:
            '''processes the content in the file, the funtion used is present in the docx2txt '''
            return docx2txt.process(file)
        except Exception as e:    #rasing exception if error in reading the file
            raise Exception(f"Error reading DOCX: {str(e)}")
        
    @staticmethod
    def extract_text_from_txt(file) -> str:
        try:
            '''reads the file using read() function and .decode("uft-8") converts to bytes'''
            return file.read().decode("utf-8")
        except Exception as e:    #rasing exception if error in reading the file
            raise Exception(f"Error reading TXT: {str(e)}")
        
    @staticmethod
    def preprocess_text(text: str) -> str:
        #handle empty string
        if not text:
            return ""
        '''Converts any amount of whitespace → single space '\s+' is one or more whitespace 
        characters (space, newline, tab)'''
        text = re.sub(r'\s+', ' ', text) 
        '''Removes unwanted symbols
        substitute with '' if it is not \w(letters,digits or underscore) not whilespace 
        not punctuation'''
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.strip()  #trims spaces
    
    #method called where file is uploaded
    def process_uploaded_file(self, uploaded_file) -> Dict[str, Any]:
        '''gives the mine type of the file, mine type = tells what type of file it is'''
        file_type = uploaded_file.type  #to get the file type
        try:

            if file_type == "application/pdf":  #to check pdf
                text = self.extract_text_from_pdf(uploaded_file) #calls pdf extractor
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #to check docx
                text = self.extract_text_from_docx(uploaded_file) #calls docx extractor
            elif file_type == "text/plain":  #to check txt file
                text = self.extract_text_from_txt(uploaded_file)   #calls txt extractor
            else:
                #for unsupported file type
                return {"success": False, "error": f"Unsupported file type: {file_type}"}
            '''it cleans the text, the funtion preprocess_text() funtion is defined above'''
            processed_text = self.preprocess_text(text)   
            if not processed_text:   #if not able to process
                return {"success": False, "error": "No text could be extracted from the document"}
            #these datas are returned as a dict
            return {
                "success": True,
                "text": processed_text,
                "file_type": file_type,
                "file_name": uploaded_file.name
            }
        except Exception as e:  #overall error handling
            return {"success": False, "error": str(e)}