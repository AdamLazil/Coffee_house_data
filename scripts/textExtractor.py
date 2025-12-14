import os
import csv
from PyPDF2 import PdfReader


input_dir = "E:/práce/firmy/cafe slavia/analysis/Coffee_house_data/data_raw/emailData"
csv_dir = "output_csvs"


def extract_pdf_text(pdf_path: str) -> list[str]:
    """Extract text from a PDF and return as a list of lines."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return [line.strip() for line in text.split("\n") if line.strip()]


def save_lines_to_csv(lines: list[str], output_path: str) -> None:
    """Save a list of lines to a CSV file, one line per row."""
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in lines:
            csvwriter.writerow([line])
    print("Text extracted and saved to output.csv")


def process_pdf_folder(input_dir: str, csv_dir: str) -> None:
    """Process all PDFs in a folder and save extracted text to a CSV."""

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, filename)
        csv_name = os.path.splitext(filename)[0] + ".csv"
        csv_path = os.path.join(csv_dir, csv_name)

        print(f"Processing {filename}...")

        lines = extract_pdf_text(pdf_path)
        save_lines_to_csv(lines, csv_path)


if __name__ == "__main__":
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    process_pdf_folder(input_dir, csv_dir)
    print("All PDFs processed.")
