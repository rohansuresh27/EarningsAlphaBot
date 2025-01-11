#!/usr/bin/env python3
import os
import sys
from pdf_processor import PDFProcessor
from quote_extractor import QuoteExtractor
from utils import setup_directory_structure, validate_pdf_file

def main():
    """Main entry point for the earnings call analysis tool."""
    try:
        # Setup directory structure
        setup_directory_structure()
        
        # Initialize processors
        pdf_processor = PDFProcessor()
        quote_extractor = QuoteExtractor()
        
        # Process all PDFs in the directory structure
        for fiscal_year in ['FY25', 'FY26']:
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                pdf_dir = os.path.join('pdfs', fiscal_year, quarter)
                if not os.path.exists(pdf_dir):
                    continue
                
                # Process each PDF in the quarter directory
                for filename in os.listdir(pdf_dir):
                    if not filename.endswith('.pdf'):
                        continue
                        
                    pdf_path = os.path.join(pdf_dir, filename)
                    try:
                        if not validate_pdf_file(pdf_path):
                            print(f"Warning: Invalid PDF file: {pdf_path}")
                            continue
                            
                        # Extract text from PDF
                        text = pdf_processor.extract_text(pdf_path)
                        
                        # Extract quotes
                        quotes = quote_extractor.extract_quotes(text)
                        
                        # Print results
                        print(f"\nAnalysis results for {filename}:")
                        print("-" * 50)
                        for quote in quotes:
                            print(f"Quote: {quote}")
                            print("-" * 30)
                            
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")
                        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
