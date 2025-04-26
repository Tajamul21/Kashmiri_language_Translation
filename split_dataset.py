import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_dataset(excel_path, output_dir):
    # Load dataset
    df = pd.read_excel(excel_path)
    
    # Verify expected columns
    assert 'English_Sentence' in df.columns, "English column missing"
    assert 'Kashmiri_Translation' in df.columns, "Kashmiri column missing"
    
    # Create output directory structure
    os.makedirs(os.path.join(output_dir, "train", "en-ks"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "dev", "en-ks"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "test", "en-ks"), exist_ok=True)

    # Split data (70% train, 10% val, 20% test)
    train_val, test = train_test_split(df, test_size=0.2, random_state=42)
    train, val = train_test_split(train_val, test_size=0.125, random_state=42)  # 0.125*0.8=0.1

    # Save splits
    def save_split(data, split_name):
        src_path = os.path.join(output_dir, split_name, "en-ks", f"{split_name}.en")
        tgt_path = os.path.join(output_dir, split_name, "en-ks", f"{split_name}.ks")
        
        data['English_Sentence'].to_csv(src_path, index=False, header=False)
        data['Kashmiri_Translation'].to_csv(tgt_path, index=False, header=False)

    save_split(train, "train")
    save_split(val, "dev")
    save_split(test, "test")

if __name__ == "__main__":
    split_dataset(
        excel_path="Final_English_Kashmiri_Corpora.xlsx",
        output_dir="dataset_splits"
    )