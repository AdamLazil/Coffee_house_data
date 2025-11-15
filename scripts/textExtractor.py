# extract text from pdf files with encoding for czech characters and save as csv

import csv
from PyPDF2 import PdfReader
from pprint import pprint
import tabula

dfs = tabula.read_pdf(
    "Uzaverka_pokladny_901_1_20231210_285.pdf", pages="all", multiple_tables=True
)
for i, df in enumerate(dfs):
    print(f"Table {i}:")
    pprint(df)

with open("Uzaverka_pokladny_901_1_20231210_285.pdf", "rb") as file:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    lines = text.split("\n")
    ind = lines.index("Kavárna")
    print(ind)

    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in lines:
            csvwriter.writerow([line])
    print("Text extracted and saved to output.csv")
