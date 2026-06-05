from PyPDF2 import PdfReader
import re
import tkinter as tk
from tkinter import filedialog

def get_pdf_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    pdf_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    root.destroy()
    return pdf_path

pdf_path = get_pdf_path()
if not pdf_path:
    print("No file selected.")
    exit(1)

reader = PdfReader(pdf_path)
text = ""

for page in reader.pages:
    text += page.extract_text() or ""

def clean_pdf_page_numbers(text):
    # Remove lines that are only page numbers, like: 1
    pattern1 = "(?m)^\\s*\\d{1,3}\\s*$"
    text = re.sub(pattern1, "", text)

    # Remove page numbers glued to the beginning of a line, like: 1She, 2KopeG, 3“I
    pattern2 = "(?m)^\\s*\\d{1,3}(?=[A-ZÁÉÍÓÖŐÚÜŰ“\"'])"
    text = re.sub(pattern2, "", text)

    #Remove page labels like: Page 1 or Page 1 of 10
    text = re.sub(r"(?mi)^\s*Page\s+\d+(\s+of\s+\d+)?\s*$", "", text)

    return text

number_of_words = len(clean_pdf_page_numbers(text))
print(number_of_words)