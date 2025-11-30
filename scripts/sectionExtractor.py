import re

data_path = "output.csv"


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
def separate_name_value(lines, pattern):
    separated_lines = []

    for line in lines:
        line = line.strip('"')

        match = re.search(pattern, line)
        if match:
            name = match.group(1)
            value = match.group(2)
            separated_lines.append((name, value))

    return separated_lines


# save separated section to a csv with two columns: name and value
def save_separated_to_csv(separated_lines, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for name, value in separated_lines:
            file.write(f"{name},{value}\n")


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
    pattern = r"^(\w[\w\s\w]*?)\s+(\d[\d\s]*[,\.]\d{2})$"
    separated_lines = separate_name_value(section, pattern)
    # save to csv
    output_path = "extracted_rastr.csv"
    save_separated_to_csv(separated_lines, output_path)


if __name__ == "__main__":
    main()
