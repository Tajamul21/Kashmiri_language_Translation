import pandas as pd

# List of your Excel files
dataset_files = [
    "4000_new.xlsx",
    "5000_Parallel Corpora.xlsx",
    "500_new.xlsx",
    "Kash Eng 150 sents.xlsx",
    "new_data.xlsx"
]

# Read and merge all Excel files
df_list = [pd.read_excel(file) for file in dataset_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Remove duplicate rows
merged_df.drop_duplicates(inplace=True)

# Save to CSV file
merged_df.to_csv("dataset.csv", index=False)

print("Merged dataset saved as dataset.csv")
