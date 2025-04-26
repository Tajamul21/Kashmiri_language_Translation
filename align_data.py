# File: strict_align_train.py
from pathlib import Path

def hard_align():
    base = Path("/DATA/Shubham/Projects/Kashmiri_language_Translation/en-indic-exp")
    en_file = base/"train/eng_Latn-kas_Arab/train.eng_Latn"
    ks_file = base/"train/eng_Latn-kas_Arab/train.kas_Arab"

    # Read files
    with open(en_file, "r") as f:
        en = [l.strip() for l in f if l.strip()]
    with open(ks_file, "r") as f:
        ks = [l.strip() for l in f if l.strip()]

    # Strict 1:1 alignment (trim to shortest length)
    aligned = list(zip(en[:len(ks)], ks[:len(en)]))
    
    # Write aligned files
    with open(en_file, "w") as f:
        f.write("\n".join([e for e,k in aligned]))
    with open(ks_file, "w") as f:
        f.write("\n".join([k for e,k in aligned]))

hard_align()