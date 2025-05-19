import kagglehub
import zipfile
import os
import pandas as pd

# Step 1: Download dataset zip
zip_path = kagglehub.dataset_download("hugodarwood/epirecipes")

# Step 2: Extract files
extract_folder = os.path.splitext(zip_path)[0]
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Step 3: List files
print("Extracted files:", os.listdir(extract_folder))

# Step 4: Load your main data file (adjust filename if different)
csv_path = os.path.join(extract_folder, 'epi_r.csv')  # example, change as needed
df = pd.read_csv(csv_path)

print(df.head())
