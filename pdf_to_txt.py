import os
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfReader

# pip install pdfminer.six, pypdf2
def extract_text_with_pdfminer(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

    # Close open handles
    converter.close()
    fake_file_handle.close()

    return text

def extract_text_with_pypdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f"Error reading {pdf_path} with PyPDF2: {e}")
        return ''

def extract_text_from_pdf(pdf_path):
    try:
        # Attempt to use pdfminer to extract text
        return extract_text_with_pdfminer(pdf_path)
    except Exception as e:
        print(f"PDFMiner failed for {pdf_path}, falling back to PyPDF2: {e}")
        # Fallback to PyPDF2
        return extract_text_with_pypdf(pdf_path)

def process_pdfs(pdf_folder, txt_folder):
    # Ensure the txt_folder exists
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    # Iterate through all PDF files in the pdf_folder
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith('.pdf'):
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(txt_folder, txt_filename)

            # Skip processing if the txt file already exists
            if os.path.exists(txt_path):
                print(f"Skipping {filename}, text file already exists.")
                continue

            pdf_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(pdf_path)

            # Validate text before writing to the file
            if text.strip():
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)

# Example usage
pdf_folder = 'pdf_books'  # Folder containing PDF files
txt_folder = 'txt_books'  # Folder where TXT files will be stored
process_pdfs(pdf_folder, txt_folder)