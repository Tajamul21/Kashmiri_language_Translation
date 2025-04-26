# File: clean_final_empty_lines.py
from pathlib import Path

def clean_empty_lines(path):
    path = Path(path)
    for file in path.glob('*/*/*'):
        if file.is_file():
            print(f"Cleaning {file}")
            with open(file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            with open(file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

# Run on all splits
base = "/DATA/Shubham/Projects/Kashmiri_language_Translation/en-indic-exp"
clean_empty_lines(f"{base}/train")
clean_empty_lines(f"{base}/devtest")