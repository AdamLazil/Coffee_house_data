import re
import os
import pandas as pd

input_path = (
    "E:/práce/firmy/cafe slavia/analysis/Coffee_house_data/data_raw/emailData_csvs"
)
output_path = "E:/práce/firmy/cafe slavia/analysis/Coffee_house_data/data_clean"


# function to extract date from lines based on pattern
def extract_date(lines, pattern):
    text = " ".join(lines)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def extract_sortiment(lines, start_pattern, end_pattern):
    extracting = False
    section_lines = []

    for line in lines:
        line = line.strip("-=")
        if re.match(r"^PLU", line):
            continue  # skip header line
        if re.search(start_pattern, line):
            extracting = True
            continue
        if re.search(end_pattern, line):
            extracting = False
            continue
        if extracting:
            section_lines.append(line)

    return section_lines


def joiner(lines):
    joined_lines = []

    for line in lines:
        line_clean = line.replace('"', "").strip()
        if re.match(r"^\d+,\d+\s+\d+,\d+$", line_clean):
            prev_line = joined_lines[-1]
            joined = prev_line + " " + line_clean
            joined_lines[-1] = joined
            continue
        joined_lines.append(line_clean)

    return joined_lines


def separate_values(lines, pattern, date):
    separated_lines = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            plu = match.group(1)
            name = match.group(2)
            mount = match.group(3)
            price = match.group(4)
            separated_lines.append((plu, name, mount, price, date))

    return separated_lines


def save_section_to_csv(section, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for plu, name, mount, price, date in section:
            mount, price = mount.replace(",", "."), price.replace(
                ",", "."
            )  # normalize decimal points
            file.write(f"{plu},{name},{mount},{price},{date}\n")


def procesed_csvfolder(input_path, output_path):
    """process all CSVs in a folder to extract sections and save to new CSVs."""
    for filename in os.listdir(input_path):
        if not filename.lower().endswith(".csv"):
            continue

        csv_path = os.path.join(input_path, filename)
        output_name = os.path.splitext(filename)[0] + "_extracted_sortiment.csv"
        output_path = os.path.join(output_path, output_name)

        with open(csv_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        start_pattern = r"Kavárna|Kuchyně"
        end_pattern = r"CELKEM"
        # pattern_plu = r"(\d{1,3})\s+(\w[\w\s\w]*)\s+(?:\-\s?\w[\w\s\w]*)\s+(\d{1,2}\,\d{1,2})\s+(\d{1,4}[,\.]\d{2})$"
        pattern_plu = r"^(\d{1,3})\s+(.+?)(?:\s+\d+[,\.]?\d*l.*?-.*?\s+)?(\d+,\d+)\s+(\d+[.,]\d{2})$"
        pattern_date = r"(\d{1,2}\.\d{1,2}\.\d{4})"
        date = extract_date(lines, pattern_date)
        section = extract_sortiment(lines, start_pattern, end_pattern)
        joined = joiner(section)
        separated = separate_values(joined, pattern_plu, date)
        save_section_to_csv(separated, output_path)


def join_cvs(input_folder, output_file):
    dataframes = []
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith("_extracted_sortiment.csv"):
            continue

        csv_path = os.path.join(input_folder, filename)
        df = pd.read_csv(
            csv_path,
            header=None,
            names=["PLU", "Name", "Mount", "Price", "Date"],
            dtype=str,
            sep=",",
            engine="python",
        )
        dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False, header=False)


def main():

    procesed_csvfolder(input_path, output_path)
    output_file = os.path.join(output_path, "combined_sortiment.csv")
    join_cvs(output_path, output_file)


if __name__ == "__main__":
    main()
