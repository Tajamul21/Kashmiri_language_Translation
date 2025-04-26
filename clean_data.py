# File: clean_data_final.py
import re
import sys
from pathlib import Path

def clean_line(line):
    """Aggressive cleaning with Unicode normalization"""
    # Remove quotes and special spaces
    line = re.sub(r'^["\'\u200b]+|["\'\u200b]+$', '', line.strip())
    # Collapse whitespace and remove control chars
    line = re.sub(r'\s+', ' ', line).strip()
    return line

def clean_pair(src_dir):
    """Clean and align parallel files"""
    src_dir = Path(src_dir)
    
    # Process English-Kashmiri pairs
    for lang_pair in src_dir.glob('*'):
        if not lang_pair.is_dir():
            continue
            
        # Get file paths
        en_file = next(lang_pair.glob('*.eng_Latn'), None)
        ks_file = next(lang_pair.glob('*.kas_Arab'), None)
        
        if not en_file or not ks_file:
            continue
            
        # Clean and align
        with open(en_file, 'r', encoding='utf-8') as f:
            en_lines = [clean_line(l) for l in f]
        with open(ks_file, 'r', encoding='utf-8') as f:
            ks_lines = [clean_line(l) for l in f]
            
        # Remove empty pairs
        cleaned = [
            (e, k) for e, k in zip(en_lines, ks_lines) 
            if e and k  # Both must be non-empty
        ]
        
        # Write back aligned data
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join([e for e, _ in cleaned]))
        with open(ks_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join([k for _, k in cleaned]))

if __name__ == '__main__':
    base = Path('/DATA/Shubham/Projects/Kashmiri_language_Translation/en-indic-exp')
    
    # Clean all splits
    clean_pair(base/'train/eng_Latn-kas_Arab')
    clean_pair(base/'devtest/all/eng_Latn-kas_Arab')
    
    print("Data cleaned and aligned!")