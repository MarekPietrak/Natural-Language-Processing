from typing import Any
from PyPDF2 import PdfReader
import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog

#Getting the PDF text

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

#Cleaning the text

def clean_pdf_page_numbers(text):
    pattern1 = "(?m)^\\s*\\d{1,3}\\s*$" # Removes page numbers
    text = re.sub(pattern1, "", text)

    pattern2 = "(?m)^\\s*\\d{1,3}(?=[A-ZÁÉÍÓÖŐÚÜŰ“\"'])" # Removes numbers attached to words
    text = re.sub(pattern2, "", text)

    text = re.sub(r"(?mi)^\s*Page\s+\d+(\s+of\s+\d+)?\s*$", "", text) # Removes page labels

    return text

def find_common_words(text):
    words = text.split()
    return Counter(words)

common_words = find_common_words(clean_pdf_page_numbers(text))
sorted_words = common_words.most_common(15)  # Only top 15

print("Most common words are:\n")
i = 1
for item in sorted_words:
    word = item[0]
    count = item[1]
    print(str(i) + ") " + word + " - " + str(count))
    i = i + 1