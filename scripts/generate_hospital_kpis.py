import pandas as pd
import numpy as np
import os

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "hospital_cleaned.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "hospital_final_dataset.xlsx"
)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# ============================================================
# DATE CONVERSION
# ============================================================

df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"],
    errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"],
    errors="coerce"
)

# ============================================================
# NUMERIC CONVERSION
# ============================================================

numeric_columns = [
    "Total_Beds",
    "Occupied_Beds",
    "Available_Medical_Equipment",
    "Staff_Allocation_Count"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# ============================================================
# LENGTH OF STAY
# ============================================================

df["Length_of_Stay"] = (
    df["Discharge_Date"] -
    df["Admission_Date"]
).dt.days

df["Length_of_Stay"] = df["Length_of_Stay"].clip(lower=0)

# ============================================================
# BED OCCUPANCY RATE
# ============================================================

df["Occupancy_Rate"] = np.where(
    df["Total_Beds"] > 0,
    (df["Occupied_Beds"] / df["Total_Beds"]) * 100,
    0
)

df["Occupancy_Rate"] = df["Occupancy_Rate"].clip(
    lower=0,
    upper=100
)

# ============================================================
# BED UTILIZATION RATE
# ============================================================

df["Bed_Utilization_Rate"] = np.where(
    df["Total_Beds"] > 0,
    (df["Occupied_Beds"] / df["Total_Beds"]) * 100,
    0
)

df["Bed_Utilization_Rate"] = df[
    "Bed_Utilization_Rate"
].clip(
    lower=0,
    upper=100
)

# ============================================================
# READMISSION FLAG
# ============================================================

df["Readmission_Flag"] = np.where(
    df["Readmission_Status"].astype(str).str.strip().str.lower() == "yes",
    1,
    0
)

# ============================================================
# MORTALITY FLAG
# ============================================================

if "Outcome" in df.columns:

    df["Mortality_Flag"] = np.where(
        df["Outcome"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("deceased"),
        1,
        0
    )

else:
    df["Mortality_Flag"] = 0

# ============================================================
# MONTH / YEAR
# ============================================================

df["Admission_Year"] = df["Admission_Date"].dt.year

df["Admission_Month"] = df["Admission_Date"].dt.month

df["Admission_Month_Name"] = (
    df["Admission_Date"]
    .dt.strftime("%B")
)

df["Admission_Year_Month"] = (
    df["Admission_Date"]
    .dt.to_period("M")
    .astype(str)
)

# ============================================================
# DEPARTMENT EFFICIENCY SCORE
# ============================================================

# Patient volume relative to available resources.
# Higher patient volume with reasonable staffing
# produces a higher efficiency score.

department_volume = df.groupby(
    "Department_Name"
)["Patient_ID"].transform("count")

department_staff = df.groupby(
    "Department_Name"
)["Staff_Allocation_Count"].transform("mean")

df["Department_Efficiency_Score"] = np.where(
    department_staff > 0,
    department_volume / department_staff,
    0
)

# Normalize score to 0-100

max_efficiency = df[
    "Department_Efficiency_Score"
].max()

if max_efficiency > 0:

    df["Department_Efficiency_Score"] = (
        df["Department_Efficiency_Score"]
        / max_efficiency
    ) * 100

# ============================================================
# KPI SUMMARY
# ============================================================

total_admissions = df["Patient_ID"].nunique()

total_discharges = df[
    "Discharge_Date"
].notna().sum()

average_los = df[
    "Length_of_Stay"
].mean()

average_occupancy = df[
    "Occupancy_Rate"
].mean()

readmission_rate = (
    df["Readmission_Flag"].sum()
    / total_discharges
) * 100 if total_discharges > 0 else 0

bed_utilization = df[
    "Bed_Utilization_Rate"
].mean()

efficiency_score = df[
    "Department_Efficiency_Score"
].mean()

mortality_rate = (
    df["Mortality_Flag"].sum()
    / total_discharges
) * 100 if total_discharges > 0 else 0

# ============================================================
# KPI SUMMARY TABLE
# ============================================================

kpi_summary = pd.DataFrame({

    "KPI": [
        "Total Admissions",
        "Total Discharges",
        "Occupancy Rate (%)",
        "Average Length of Stay",
        "Readmission Rate (%)",
        "Bed Utilization Rate (%)",
        "Department Efficiency Score",
        "Mortality Rate (%)"
    ],

    "Value": [
        total_admissions,
        total_discharges,
        round(average_occupancy, 2),
        round(average_los, 2),
        round(readmission_rate, 2),
        round(bed_utilization, 2),
        round(efficiency_score, 2),
        round(mortality_rate, 2)
    ]
})

# ============================================================
# HOSPITAL LEVEL KPI
# ============================================================

hospital_kpi = df.groupby(
    [
        "Hospital_ID",
        "Hospital_Name",
        "Region"
    ],
    dropna=False
).agg(

    Total_Admissions=(
        "Patient_ID",
        "nunique"
    ),

    Total_Discharges=(
        "Discharge_Date",
        lambda x: x.notna().sum()
    ),

    Average_Length_of_Stay=(
        "Length_of_Stay",
        "mean"
    ),

    Average_Occupancy_Rate=(
        "Occupancy_Rate",
        "mean"
    ),

    Average_Bed_Utilization=(
        "Bed_Utilization_Rate",
        "mean"
    ),

    Readmissions=(
        "Readmission_Flag",
        "sum"
    ),

    Deaths=(
        "Mortality_Flag",
        "sum"
    ),

    Total_Beds=(
        "Total_Beds",
        "mean"
    ),

    Occupied_Beds=(
        "Occupied_Beds",
        "mean"
    ),

    Staff_Count=(
        "Staff_Allocation_Count",
        "mean"
    )

).reset_index()

hospital_kpi["Readmission_Rate"] = np.where(
    hospital_kpi["Total_Discharges"] > 0,
    (
        hospital_kpi["Readmissions"]
        / hospital_kpi["Total_Discharges"]
    ) * 100,
    0
)

hospital_kpi["Mortality_Rate"] = np.where(
    hospital_kpi["Total_Discharges"] > 0,
    (
        hospital_kpi["Deaths"]
        / hospital_kpi["Total_Discharges"]
    ) * 100,
    0
)

hospital_kpi["Average_Length_of_Stay"] = (
    hospital_kpi["Average_Length_of_Stay"]
    .round(2)
)

hospital_kpi["Average_Occupancy_Rate"] = (
    hospital_kpi["Average_Occupancy_Rate"]
    .round(2)
)

hospital_kpi["Readmission_Rate"] = (
    hospital_kpi["Readmission_Rate"]
    .round(2)
)

hospital_kpi["Mortality_Rate"] = (
    hospital_kpi["Mortality_Rate"]
    .round(2)
)

# ============================================================
# DEPARTMENT KPI
# ============================================================

department_kpi = df.groupby(
    [
        "Department_Name"
    ],
    dropna=False
).agg(

    Total_Admissions=(
        "Patient_ID",
        "nunique"
    ),

    Average_Length_of_Stay=(
        "Length_of_Stay",
        "mean"
    ),

    Average_Occupancy_Rate=(
        "Occupancy_Rate",
        "mean"
    ),

    Average_Bed_Utilization=(
        "Bed_Utilization_Rate",
        "mean"
    ),

    Readmissions=(
        "Readmission_Flag",
        "sum"
    ),

    Deaths=(
        "Mortality_Flag",
        "sum"
    ),

    Average_Staff=(
        "Staff_Allocation_Count",
        "mean"
    )

).reset_index()

department_kpi["Readmission_Rate"] = (
    department_kpi["Readmissions"]
    / department_kpi["Total_Admissions"]
) * 100

department_kpi["Mortality_Rate"] = (
    department_kpi["Deaths"]
    / department_kpi["Total_Admissions"]
) * 100

department_kpi["Department_Efficiency_Score"] = np.where(
    department_kpi["Average_Staff"] > 0,
    department_kpi["Total_Admissions"]
    / department_kpi["Average_Staff"],
    0
)

max_score = department_kpi[
    "Department_Efficiency_Score"
].max()

if max_score > 0:

    department_kpi[
        "Department_Efficiency_Score"
    ] = (
        department_kpi[
            "Department_Efficiency_Score"
        ] / max_score
    ) * 100

department_kpi = department_kpi.round(2)

# ============================================================
# MONTHLY KPI
# ============================================================

monthly_kpi = df.groupby(
    "Admission_Year_Month"
).agg(

    Total_Admissions=(
        "Patient_ID",
        "nunique"
    ),

    Average_Length_of_Stay=(
        "Length_of_Stay",
        "mean"
    ),

    Average_Occupancy_Rate=(
        "Occupancy_Rate",
        "mean"
    ),

    Average_Bed_Utilization=(
        "Bed_Utilization_Rate",
        "mean"
    ),

    Readmissions=(
        "Readmission_Flag",
        "sum"
    ),

    Deaths=(
        "Mortality_Flag",
        "sum"
    )

).reset_index()

monthly_kpi["Readmission_Rate"] = (
    monthly_kpi["Readmissions"]
    / monthly_kpi["Total_Admissions"]
) * 100

monthly_kpi["Mortality_Rate"] = (
    monthly_kpi["Deaths"]
    / monthly_kpi["Total_Admissions"]
) * 100

monthly_kpi = monthly_kpi.round(2)

# ============================================================
# RESOURCE KPI
# ============================================================

resource_kpi = df.groupby(
    [
        "Hospital_ID",
        "Hospital_Name",
        "Department_Name",
        "Region"
    ],
    dropna=False
).agg(

    Total_Beds=(
        "Total_Beds",
        "mean"
    ),

    Occupied_Beds=(
        "Occupied_Beds",
        "mean"
    ),

    Staff_Allocation_Count=(
        "Staff_Allocation_Count",
        "mean"
    ),

    Available_Medical_Equipment=(
        "Available_Medical_Equipment",
        "mean"
    ),

    Patient_Volume=(
        "Patient_ID",
        "nunique"
    )

).reset_index()

resource_kpi["Bed_Utilization_Rate"] = np.where(
    resource_kpi["Total_Beds"] > 0,
    (
        resource_kpi["Occupied_Beds"]
        / resource_kpi["Total_Beds"]
    ) * 100,
    0
)

resource_kpi = resource_kpi.round(2)

# ============================================================
# EXPORT TO EXCEL
# ============================================================

with pd.ExcelWriter(
    OUTPUT_PATH,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Patient_Data",
        index=False
    )

    kpi_summary.to_excel(
        writer,
        sheet_name="KPI_Summary",
        index=False
    )

    hospital_kpi.to_excel(
        writer,
        sheet_name="Hospital_KPI",
        index=False
    )

    department_kpi.to_excel(
        writer,
        sheet_name="Department_KPI",
        index=False
    )

    monthly_kpi.to_excel(
        writer,
        sheet_name="Monthly_KPI",
        index=False
    )

    resource_kpi.to_excel(
        writer,
        sheet_name="Resource_KPI",
        index=False
    )

print("\nKPI ENGINEERING COMPLETED")
print("--------------------------------")
print("Total Admissions:", total_admissions)
print("Total Discharges:", total_discharges)
print("Occupancy Rate:", round(average_occupancy, 2), "%")
print("ALOS:", round(average_los, 2), "days")
print("Readmission Rate:", round(readmission_rate, 2), "%")
print("Bed Utilization:", round(bed_utilization, 2), "%")
print("Efficiency Score:", round(efficiency_score, 2))
print("Mortality Rate:", round(mortality_rate, 2), "%")
print("--------------------------------")
print("Output:", OUTPUT_PATH)