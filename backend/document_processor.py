# backend/document_processor.py

import re
import docx2txt
import PyPDF2

class DocumentProcessor:
    
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        pdf_reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() or "" for page in pdf_reader.pages)
        
    @staticmethod
    def extract_text_from_docx(file) -> str:
        return docx2txt.process(file)
        
    @staticmethod
    def extract_text_from_txt(file) -> str:
        return file.read().decode("utf-8")
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.strip()
    
    def process_uploaded_file(self, uploaded_file):
        file_type = uploaded_file.type
        
        extractors = {
            "application/pdf": self.extract_text_from_pdf,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": self.extract_text_from_docx,
            "text/plain": self.extract_text_from_txt
        }
        
        if file_type not in extractors:
            return {"success": False, "error": "File type not correct"}
        
        try:
            text = extractors[file_type](uploaded_file)
            processed_text = self.preprocess_text(text)
            
            if not processed_text:
                return {"success": False, "error": "No text could be extracted"}
            
            return {
                "success": True,
                "text": processed_text
            }
        except Exception as e:
            return False
