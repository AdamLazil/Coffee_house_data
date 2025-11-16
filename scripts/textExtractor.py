# extract text from pdf files with encoding for czech characters and save as csv

import csv
from PyPDF2 import PdfReader
from pprint import pprint


with open("Uzaverka_pokladny_901_1_20231210_285.pdf", "rb") as file:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        print(line)

    ind = lines.index("Kavárna")
    print(lines)

    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in lines:
            csvwriter.writerow([line])
    print("Text extracted and saved to output.csv")
