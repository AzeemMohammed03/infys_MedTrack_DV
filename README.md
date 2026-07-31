# 🏥 MedTrack DV – Hospital Operations & Patient Analytics Dashboard

> An enterprise-grade healthcare analytics project that transforms raw hospital operational and patient admission data into actionable insights using **Python**, **Pandas**, **NumPy**, and **Tableau**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy)
![Tableau](https://img.shields.io/badge/Tableau-Visualization-E97627?logo=tableau)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Project Overview

Hospitals generate massive amounts of operational and patient data every day. Analyzing this data manually is difficult and time-consuming.

**MedTrack DV** provides a centralized analytics solution that:

- Integrates multiple hospital datasets
- Cleans and standardizes healthcare data
- Calculates operational KPIs
- Visualizes insights using interactive Tableau dashboards

The project follows an end-to-end data analytics workflow, from raw CSV files to executive dashboards.

---

## 🎯 Objectives

- Build an automated healthcare data pipeline
- Clean and standardize operational datasets
- Generate hospital performance KPIs
- Develop interactive Tableau dashboards
- Support data-driven hospital management decisions

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python 3.x |
| Data Processing | Pandas, NumPy |
| Visualization | Tableau Desktop / Tableau Public |
| Notebook | Jupyter Notebook |
| Version Control | Git & GitHub |
| Documentation | Markdown |

---

# 📁 Project Structure

```text
MedTrack_DV/
│
├── data/
│   ├── raw/
│   │   ├── hospital_operational_data.csv
│   │   ├── patient_admissions_data.csv
│   │   └── hospital_raw_data.csv
│   │
│   └── processed/
│       └── hospital_cleaned.csv
│
├── scripts/
│   ├── data_collection.py
│   └── hospital_cleaning.ipynb
│
├── dashboard/
│   └── MedTrack_Dashboard.twbx
│
├── docs/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Project Workflow

```text
Raw CSV Files
        │
        ▼
Data Collection
(Pandas)
        │
        ▼
Data Integration
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
KPI Calculation
        │
        ▼
Hospital Clean Dataset
        │
        ▼
Tableau Dashboards
```

---

# 📊 Datasets

### Hospital Operational Dataset

Contains information such as:

- Hospital ID
- Department Name
- Total Beds
- Occupied Beds
- Medical Equipment
- Staff Allocation
- Region

### Patient Admission Dataset

Contains:

- Patient ID
- Admission Date
- Discharge Date
- Patient Type
- Department
- Readmission Status
- Outcome

---

# 🚀 Features

- Automated data ingestion
- Dataset merging
- Duplicate removal
- Missing value handling
- Department name standardization
- Date parsing
- KPI generation
- Tableau-ready dataset creation

---

# 📈 Key Performance Indicators (KPIs)

- Bed Occupancy Rate
- Available Beds
- Total Admissions
- Total Discharges
- Readmission Rate
- Average Length of Stay
- Department Performance
- Patient Flow
- Resource Utilization
- Staff Allocation

---

# 📌 Milestones

## ✅ Milestone 1 – Data Collection & Preparation

- Data ingestion
- Dataset integration
- Duplicate removal
- Missing value handling
- Data standardization
- Date formatting
- Export cleaned dataset

### Deliverables

- `data_collection.py`
- `hospital_raw_data.csv`
- `hospital_cleaning.ipynb`
- `hospital_cleaned.csv`

---

## 🚧 Milestone 2 – KPI Engineering

- Hospital KPIs
- Patient KPIs
- Resource KPIs
- Operational Metrics

---

## 🚧 Milestone 3 – Tableau Dashboard Development

Four interactive dashboards:

### 🏥 Hospital Overview

- Total Admissions
- Total Patients
- Bed Occupancy
- Executive KPIs

### 👨‍⚕️ Patient Flow

- Admission Trends
- Discharge Trends
- Average Length of Stay
- Readmission Analysis

### 🏢 Department Analytics

- Department Comparison
- Patient Distribution
- Operational Efficiency

### 🛏️ Resource Utilization

- Bed Occupancy
- Equipment Availability
- Staff Allocation
- Capacity Analysis

---

# 📋 Data Quality Standards

| Metric | Target |
|----------|---------|
| Dataset Completeness | >95% |
| Remaining Missing Values | <2% |
| Data Consistency | 100% |
| Duplicate Records | 0 |

---

# ▶️ Getting Started

## Clone Repository

```bash
git clone https://github.com/AzeemMohammed03/infys_MedTrack_DV.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Data Collection

```bash
python scripts/data_collection.py
```

## Open Cleaning Notebook

```bash
jupyter notebook
```

---

# 📌 Future Enhancements

- Predictive patient admission forecasting
- Readmission risk prediction
- Bed demand forecasting
- Hospital performance benchmarking
- SQL database integration
- Power BI version
- Cloud deployment
- Real-time dashboard updates

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 👨‍💻 Author

**Mohammed Azeem**

- GitHub: https://github.com/AzeemMohammed03
- LinkedIn: *(Add your LinkedIn profile here)*

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

**Built with ❤️ using Python, Pandas, NumPy, and Tableau**
