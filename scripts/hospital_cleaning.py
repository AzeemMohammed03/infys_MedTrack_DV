import pandas as pd
ops=pd.read_csv("../data/raw/hospital_operational_data.csv")
pat=pd.read_csv("../data/raw/patient_admissions_data.csv")
raw=pat.merge(ops,on=["Hospital_ID","Department_Name"],how="left")
raw.to_csv("../data/raw/hospital_raw_data.csv",index=False)
raw=raw.drop_duplicates();raw["Admission_Date"]=pd.to_datetime(raw["Admission_Date"]);raw["Discharge_Date"]=pd.to_datetime(raw["Discharge_Date"]);raw["Length_of_Stay"]=(raw["Discharge_Date"]-raw["Admission_Date"]).dt.days;raw.to_csv("../data/processed/hospital_cleaned.csv",index=False)