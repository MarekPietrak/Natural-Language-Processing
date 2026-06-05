from PyPDF2 import PdfReader
import re
import tkinter as tk
from tkinter import filedialog

def get_pdf_path():
    root = tk.Tk()
    root.withdraw()
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
    pattern1 = "(?m)^\\s*\\d{1,3}\\s*$" # Removes page numbers
    text = re.sub(pattern1, "", text)

    pattern2 = "(?m)^\\s*\\d{1,3}(?=[A-ZÁÉÍÓÖŐÚÜŰ“\"'])" # Removes numbers attached to words
    text = re.sub(pattern2, "", text)

    text = re.sub(r"(?mi)^\s*Page\s+\d+(\s+of\s+\d+)?\s*$", "", text) # Removes page labels

    return text

number_of_words = len(clean_pdf_page_numbers(text))
print(number_of_words)