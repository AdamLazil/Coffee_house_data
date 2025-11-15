import pandas as pd
import re

# načtení souboru
df = pd.read_csv("output.csv", header=None, dtype=str)
pattern = r"[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]"


df.columns = ["raw"]
for word in df["raw"]:
    print("Found date! on position ", df[df["raw"] == word].index[0])
    if re.match(pattern, word):
        print("Found date! on position ", df[df["raw"] == word].index[0])

# pokud má jen jeden sloupec:
df.columns = ["raw"]
for word in df["raw"]:
    if word == "Kavárna":
        print("Found it! on position ", df[df["raw"] == word].index[0])
        print(word.find("Kavárna"))
    else:
        pass


# odstranění prázdných řádků
df = df[df["raw"].notna() & (df["raw"].str.strip() != "")]

# regulární výraz pro oddělení textu, čísla a hodnoty
pattern = r"^(.*?)\s+(\d+)\s+([\d,]+)"

# aplikace regexu
df_extracted = df["raw"].str.extract(pattern)
print(df_extracted)

# přejmenování sloupců
df_extracted.columns = ["polozka", "pocet", "hodnota"]

# převod číselných formátů (např. 156,0 → 156.0)
df_extracted["hodnota"] = (
    df_extracted["hodnota"].str.replace(",", ".", regex=False).astype(float)
)
df_extracted["pocet"] = df_extracted["pocet"].astype(int)

# uložení do nového CSV
df_extracted.to_csv("output_clean.csv", index=False)

print(df_extracted.head())
