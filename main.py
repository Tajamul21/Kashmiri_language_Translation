# import pandas as pd

# # List of your Excel files
# dataset_files = [
#     "4000_new.xlsx",
#     "5000_Parallel Corpora.xlsx",
#     "500_new.xlsx",
#     "Kash Eng 150 sents.xlsx",
#     "new_data.xlsx"
# ]

# # Read and merge all Excel files
# df_list = [pd.read_excel(file) for file in dataset_files]
# merged_df = pd.concat(df_list, ignore_index=True)

# # Remove duplicate rows
# merged_df.drop_duplicates(inplace=True)

# # Save to CSV file
# merged_df.to_csv("dataset.csv", index=False)

# print("Merged dataset saved as dataset.csv")




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

# Remove unnamed columns
merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]

# Remove duplicate rows
merged_df.drop_duplicates(inplace=True)


# Remove leading/trailing quotes and ensure proper formatting
merged_df = merged_df.map(lambda x: x.strip('"') if isinstance(x, str) else x)

# Ensure English and Kashmiri sentences are properly separated
cleaned_rows = []
for index, row in merged_df.iterrows():
    english_text = str(row.iloc[0]).strip().strip('"')
    kashmiri_text = str(row.iloc[1]).strip().strip('"')
    if english_text and kashmiri_text:
        cleaned_rows.append([english_text, kashmiri_text])

cleaned_df = pd.DataFrame(cleaned_rows, columns=["English", "Kashmiri"])

# Save to CSV file
merged_df.to_csv("dataset1.csv", index=False)

print("Merged dataset saved as dataset1.csv")
