from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pdf():
    # Create pdfs/FY25/Q4 directory if it doesn't exist
    pdf_dir = os.path.join('pdfs', 'FY25', 'Q4')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Create PDF
    pdf_path = os.path.join(pdf_dir, 'test_earnings.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Read sample text
    with open('test/sample_earnings.txt', 'r') as f:
        text = f.read()
    
    # Write text to PDF
    y = 750  # Start from top of page
    for line in text.split('\n'):
        if line.strip():
            c.drawString(50, y, line)
            y -= 15  # Move down for next line
    
    c.save()
    return pdf_path

if __name__ == "__main__":
    create_test_pdf()
