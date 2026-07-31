import pandas as pd
import os


# ==============================
# File Path using os.path
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "hospital_cleaned.csv"
)


# Load cleaned dataset
df = pd.read_csv(file_path)


# ==============================
# 1. Dataset Completeness Check
# ==============================

total_cells = df.shape[0] * df.shape[1]

non_null_cells = df.notnull().sum().sum()

completeness = (non_null_cells / total_cells) * 100


print("===== DATASET COMPLETENESS =====")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Completeness Score: {completeness:.2f}%")

if completeness > 95:
    print("PASS: Dataset completeness is above 95%")
else:
    print("FAIL: Dataset completeness below target")


# ==============================
# 2. Missing Values Check
# ==============================

missing_values = df.isnull().sum()

missing_percentage = (
    df.isnull().sum().sum() /
    (df.shape[0] * df.shape[1])
) * 100


print("\n===== MISSING VALUE CHECK =====")

print(missing_values)

print(
    f"\nTotal Missing Percentage: {missing_percentage:.2f}%"
)


if missing_percentage < 2:
    print("PASS: Missing values are below 2%")
else:
    print("FAIL: Missing values exceed 2%")


# ==============================
# 3. Consistency Check
# ==============================

print("\n===== CONSISTENCY CHECK =====")


# Department name standardization check

department_count = df["Department_Name"].nunique()

department_values = df["Department_Name"].unique()


print("Unique Departments:")
for dept in department_values:
    print(dept)


# Check spaces and capitalization

invalid_departments = df[
    df["Department_Name"].isnull() |
    (df["Department_Name"].str.strip() == "") |
    df["Department_Name"].str.contains(r"\s{2,}", regex=True, na=False)
]


if len(invalid_departments) == 0:
    print("\nPASS: Department names are standardized")
else:
    print(
        f"\nFAIL: {len(invalid_departments)} inconsistent department values found"
    )


# Operational values check

operational_columns = [
    "Total_Beds",
    "Occupied_Beds",
    "Available_Medical_Equipment",
    "Staff_Allocation_Count"
]



for col in operational_columns:
    if col in df.columns:
        if df[col].isnull().sum() == 0:
            print(f"PASS: {col} values are consistent")
        else:
            print(f"FAIL: {col} contains missing values")


# ==============================
# Final Report
# ==============================

print("\n===== DATA QUALITY REPORT COMPLETED =====")