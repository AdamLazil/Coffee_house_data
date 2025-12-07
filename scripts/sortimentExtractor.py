import re

data_path = "output.csv"


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


def separate_values(lines, pattern):
    separated_lines = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            plu = match.group(1)
            name = match.group(2)
            mount = match.group(3)
            price = match.group(4)
            separated_lines.append((plu, name, mount, price))

    return separated_lines


def save_section_to_csv(section, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for plu, name, mount, price in section:
            file.write(f"{plu},{name},{mount},{price}\n")


def main():
    with open(data_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    start_pattern = r"Kavárna|Kuchyně"
    end_pattern = r"CELKEM"
    # pattern_plu = r"(\d{1,3})\s+(\w[\w\s\w]*)\s+(?:\-\s?\w[\w\s\w]*)\s+(\d{1,2}\,\d{1,2})\s+(\d{1,4}[,\.]\d{2})$"
    pattern_plu = (
        r"^(\d{1,3})\s+(.+?)(?:\s+\d+[,\.]?\d*l.*?-.*?\s+)?(\d+,\d+)\s+(\d+[.,]\d{2})$"
    )
    section = extract_sortiment(lines, start_pattern, end_pattern)
    joined = joiner(section)
    separated = separate_values(joined, pattern_plu)
    output_path = "extracted_sortiment.csv"
    save_section_to_csv(separated, output_path)


if __name__ == "__main__":
    main()
