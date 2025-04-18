import pandas as pd
import json

# Load Excel file
df = pd.read_excel("Final_Combined_Corpora.xlsx")

# Check nulls and drop rows with missing input/output
df = df[["English_Sentence", "Kashmiri_Sentence"]].dropna()

# Create list of dictionaries
jsonl_data = []
for _, row in df.iterrows():
    instruction_entry = {
        "instruction": "Translate the following English sentence to Kashmiri.",
        "input": row["English_Sentence"],
        "output": row["Kashmiri_Sentence"]
    }
    jsonl_data.append(instruction_entry)

# Save to .jsonl
with open("english_to_kashmiri.jsonl", "w", encoding="utf-8") as f:
    for entry in jsonl_data:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print("✅ JSONL file saved as english_to_kashmiri.jsonl")
