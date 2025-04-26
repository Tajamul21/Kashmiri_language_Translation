# File: prepare_dataset.py
import pandas as pd
from sklearn.model_selection import train_test_split
import os

# --- CONFIGURATION ---
INPUT_FILE = "Final_English_Kashmiri_Corpora.xlsx"  # Change to your filename
SRC_LANG = "English_Sentence"                                # English column name
TGT_LANG = "Kashmiri_Translation"                              # Kashmiri column name
RANDOM_SEED = 42
# ---------------------

# Load data
df = pd.read_excel(os.path.join(os.getcwd(), INPUT_FILE))  # For CSV: pd.read_csv()

# Verify columns exist
assert SRC_LANG in df.columns, f"Column '{SRC_LANG}' not found!"
assert TGT_LANG in df.columns, f"Column '{TGT_LANG}' not found!"

# 7:1:2 Split
train_df, temp_df = train_test_split(
    df,
    test_size=0.3,            # 30% for val+test
    random_state=RANDOM_SEED,
    shuffle=True
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.6666,         # 20% of total data (0.6666 * 0.3 ≈ 0.2)
    random_state=RANDOM_SEED
)

# Save files function
def save_split(data, path, prefix):
    src_path = os.path.join(path, f"{prefix}.eng_Latn")
    tgt_path = os.path.join(path, f"{prefix}.kas_Arab")
    
    data[SRC_LANG].to_csv(src_path, index=False, header=False, encoding='utf-8')
    data[TGT_LANG].to_csv(tgt_path, index=False, header=False, encoding='utf-8')
    print(f"Saved {len(data)} lines to {path}/{prefix}.*")

# Save splits
save_split(
    train_df,
    "en-indic-exp/train/eng_Latn-kas_Arab",
    "train"
)

save_split(
    val_df,
    "en-indic-exp/devtest/all/eng_Latn-kas_Arab",
    "dev"
)

save_split(
    test_df,
    "en-indic-exp/devtest/all/eng_Latn-kas_Arab",
    "test"
)

# Verification
print("\nFinal Counts:")
print(f"Total samples: {len(df)}")
print(f"Train ({len(train_df)}) : {len(train_df)/len(df):.1%}")
print(f"Validation ({len(val_df)}) : {len(val_df)/len(df):.1%}")
print(f"Test ({len(test_df)}) : {len(test_df)/len(df):.1%}")