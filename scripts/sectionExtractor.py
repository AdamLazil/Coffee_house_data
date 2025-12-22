import os
import re
import pandas as pd

input_path = (
    "E:/práce/firmy/cafe slavia/analysis/Coffee_house_data/data_raw/emailData_csvs"
)
output_path = "E:/práce/firmy/cafe slavia/analysis/Coffee_house_data/data_clean"


# function to extract date from lines based on pattern
def extract_date(lines: str, pattern) -> str:
    """date extraction from lines based on pattern"""
    text = " ".join(lines)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


# extract only the section between start_pattern and end_pattern
def extract_rastr(lines, start_pattern, end_pattern) -> list:
    """extract section between start_pattern and end_pattern and normalize spaces"""
    extracting = False
    section_lines = []

    for line in lines:
        line_norm = line.replace("\xa0", " ").strip()  # normalize non-breaking spaces
        if re.search(start_pattern, line_norm):
            extracting = True
            continue
        if re.search(end_pattern, line_norm):
            extracting = False
            continue
        if extracting:
            section_lines.append(line_norm)

    return section_lines


# function to separate name and value with regex pattern
def separate_name_value(lines, pattern, date) -> list:
    """Separate name and value from lines using regex pattern and attach date"""
    separated_lines = []

    for line in lines:
        line = line.strip('"')

        match = re.search(pattern, line)
        if match:
            name = match.group(1)
            value = match.group(2)
            separated_lines.append((name, value, date))

    return separated_lines


# save separated section to a csv with two columns: name and value
def save_separated_to_csv(separated_lines, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for name, value, date in separated_lines:
            value = value.replace(",", ".")  # normalize decimal separator
            file.write(f"{name},{value},{date}\n")


def procesed_csvfolder(input_path, output_path):
    """process all CSVs in a folder to extract sections and save to new CSVs."""
    for filename in os.listdir(input_path):
        if not filename.lower().endswith(".csv"):
            continue

        csv_path = os.path.join(input_path, filename)
        output_name = os.path.splitext(filename)[0] + "_processed.csv"
        output_csv_path = os.path.join(output_path, output_name)

        print(f"Processing {filename}...")

        with open(csv_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # define start and end patterns
        start_pattern = r"103\s+Tr.ba podle rastr."
        end_pattern = r"CELKEM"
        # extract section
        section = extract_rastr(lines, start_pattern, end_pattern)
        # define pattern to separate name and value
        pattern_date = r"(\d{1,2}\.\d{1,2}\.\d{4})"
        pattern = r"^(\w[\w\s\w]*?)\s+(\d[\d\s]*[,\.]\d{2})$"
        date = extract_date(lines, pattern_date)
        separated_lines = separate_name_value(section, pattern, date)
        # save to csv
        save_separated_to_csv(separated_lines, output_csv_path)


def join_csvs(input_path, output_file):
    """join all processed CSVs into a single CSV file with pandas library."""
    dataframes = []
    for filename in os.listdir(input_path):
        if not filename.lower().endswith("_processed.csv"):
            continue

        csv_path = os.path.join(input_path, filename)
        df = pd.read_csv(
            csv_path,
            header=None,
            names=["Name", "Value", "Date"],
            sep=",",
            dtype=str,
            engine="python",
        )
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(output_file, index=False, encoding="utf-8")


# main code
def main():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    procesed_csvfolder(input_path, output_path)

    join_csvs(output_path, os.path.join(output_path, "rastrCombined.csv"))
    print("All CSVs processed.")


if __name__ == "__main__":
    main()
