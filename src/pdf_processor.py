import PyPDF2
from typing import Optional

class PDFProcessor:
    """Handles PDF file processing and text extraction."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        pass
        
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
            
        Raises:
            Exception: If PDF processing fails
        """
        try:
            text_content = []
            with open(pdf_path, 'rb') as file:
                # Create PDF reader object
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Process each page
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                        
            return "\n".join(text_content)
            
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
            
    def get_metadata(self, pdf_path: str) -> dict:
        """
        Extract metadata from PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: PDF metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return pdf_reader.metadata
        except Exception as e:
            return {}
