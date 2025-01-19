#!/usr/bin/env python3
import os
import sys
from pdf_processor import PDFProcessor
from claude_quote_extractor import ClaudeQuoteExtractor
from utils import setup_directory_structure, validate_pdf_file, get_processed_files


def main():
    """Main entry point for the earnings call analysis tool."""
    try:
        # Setup directory structure
        setup_directory_structure()

        # Initialize processors
        pdf_processor = PDFProcessor()
        quote_extractor = ClaudeQuoteExtractor()

        # Get already processed files
        processed_files = get_processed_files()

        # Process only new PDFs in the directory structure
        for fiscal_year in ['FY25', 'FY26']:
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                pdf_dir = os.path.join('pdfs', fiscal_year, quarter)
                if not os.path.exists(pdf_dir):
                    continue

                # Only process files that haven't been processed before
                new_pdfs = [
                    f for f in os.listdir(pdf_dir) if f.endswith('.pdf')
                    and os.path.join(pdf_dir, f) not in processed_files
                ]

                if not new_pdfs:
                    continue

                print(f"\nProcessing new PDFs in {fiscal_year}/{quarter}:")

                # Process only new PDFs
                for filename in new_pdfs:
                    pdf_path = os.path.join(pdf_dir, filename)
                    try:
                        if not validate_pdf_file(pdf_path):
                            print(f"Warning: Invalid PDF file: {pdf_path}")
                            continue

                        # Extract text from PDF
                        text = pdf_processor.extract_text(pdf_path)

                        # Extract company name from filename (split by _Q and take first part)
                        company_name = filename.split('_Q')[0].replace(
                            '_', ' ')

                        # Extract quotes using Claude
                        quotes = quote_extractor.extract_quotes(
                            text, company_name, pdf_path)
                            
                        # Add fiscal year and quarter info to each quote
                        for quote in quotes:
                            quote['fiscal_year'] = fiscal_year
                            quote['quarter'] = quarter

                        # Save quotes to JSON
                        output_dir = os.path.join('output', fiscal_year,
                                                  quarter)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(
                            output_dir,
                            f"{filename.replace('.pdf', '_quotes.json')}")
                        quote_extractor.save_quotes_to_json(
                            quotes, output_path)

                        # Print results
                        print(f"\nAnalysis results for {filename}:")
                        print("-" * 50)
                        for quote in quotes:
                            print(
                                f"{quote['company']} {quote['speaker']} on {quote['description']}:"
                            )
                            print(f"\"{quote['quote']}\"")
                            print(f"{quote['hashtag']}")
                            print("-" * 30)

                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
