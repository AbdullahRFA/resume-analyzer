# app/parser.py
import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF, handling multi-page documents.
    Args:
        pdf_path (str): The file path to the PDF.
    Returns:
        str: The raw text extracted from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        # In a real app, you would log this error. For now, returning it as a string is fine.
        return f"Error reading PDF: {e}"

def clean_text(text):
    """
    Sanitizes raw text for NLP processing. Works for both Resumes and Job Descriptions.
    Args:
        text (str): The raw text string.
    Returns:
        str: The cleaned, lowercased string.
    """
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Remove URLs
    text = re.sub(r'\S+@\S+', '', text) # Remove emails
    text = re.sub(r'[^\w\s\.,#+]', ' ', text) # Remove weird bullets, keep c# and c++ symbols
    text = re.sub(r'\s+', ' ', text).strip() # Squash multiple spaces
    
    return text
