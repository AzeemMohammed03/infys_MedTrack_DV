import pandas as pd
import os

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
raw_dir = os.path.join(BASE_DIR, "data", "raw")
processed_dir = os.path.join(BASE_DIR, "data", "processed")

# Create processed folder if it does not exist
os.makedirs(processed_dir, exist_ok=True)

ops_path = os.path.join(raw_dir, "hospital_operational_data.csv")
pat_path = os.path.join(raw_dir, "patient_admissions_data.csv")

raw_path = os.path.join(raw_dir, "hospital_raw_data.csv")
cleaned_path = os.path.join(processed_dir, "hospital_cleaned.csv")


# Read datasets
ops = pd.read_csv(ops_path)
pat = pd.read_csv(pat_path)


# Merge datasets
raw = pat.merge(
    ops,
    on=["Hospital_ID", "Department_Name"],
    how="left"
)


# Save raw merged data
raw.to_csv(raw_path, index=False)