import os
from typing import List
import PyPDF2

def setup_directory_structure():
    """
    Create the required directory structure for PDF organization and output.
    """
    # Define fiscal years and quarters
    fiscal_years = ['FY25', 'FY26']
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    # Create base directories if they don't exist
    for base_dir in ['pdfs', 'output']:
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        # Create fiscal year and quarter directories
        for fy in fiscal_years:
            fy_path = os.path.join(base_dir, fy)
            if not os.path.exists(fy_path):
                os.mkdir(fy_path)

            for q in quarters:
                q_path = os.path.join(fy_path, q)
                if not os.path.exists(q_path):
                    os.mkdir(q_path)
                    # Create .gitkeep to track empty directories
                    if base_dir == 'pdfs':
                        with open(os.path.join(q_path, '.gitkeep'), 'w') as f:
                            pass

def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        bool: True if valid PDF, False otherwise
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, 'rb') as file:
            # Try to create a PDF reader object
            PyPDF2.PdfReader(file)
        return True
    except Exception:
        return False

def get_all_pdf_files() -> List[str]:
    """
    Get list of all PDF files in the directory structure.

    Returns:
        List[str]: List of PDF file paths
    """
    pdf_files = []

    for root, _, files in os.walk('pdfs'):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    return pdf_files
def get_processed_files() -> set:
    """Get set of already processed PDF files."""
    processed = set()
    for root, _, files in os.walk('output'):
        for file in files:
            if file.endswith('_quotes.json'):
                # Convert output path back to source PDF path
                pdf_name = file.replace('_quotes.json', '.pdf')
                # Get fiscal year and quarter from the current directory structure
                parts = root.split(os.sep)
                if len(parts) >= 3:  # Ensure we have enough path components
                    fiscal_year = parts[-2]  # Second to last component
                    quarter = parts[-1]      # Last component
                    source_pdf = os.path.join('pdfs', fiscal_year, quarter, pdf_name)
                    processed.add(source_pdf)
    return processed
