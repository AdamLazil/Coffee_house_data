import re

data_path = "output.csv"


# function to extract date from lines based on pattern
def extract_date(lines, pattern):
    text = " ".join(lines)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


# extract only the section between start_pattern and end_pattern
def extract_rastr(lines, start_pattern, end_pattern):
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
def separate_name_value(lines, pattern, date):
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
            file.write(f"{name},{value}, {date}\n")


# main code
def main():
    with open(data_path, "r", encoding="utf-8") as file:
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
    output_path = "extracted_rastr.csv"
    save_separated_to_csv(separated_lines, output_path)


if __name__ == "__main__":
    main()
