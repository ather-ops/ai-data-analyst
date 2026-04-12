<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,20&height=200&section=header&text=AI%20Data%20Analyst&fontSize=55&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Auto%20Data%20Cleaning%20%26%20Statistical%20Insights%20%E2%80%94%20Built%20With%20Streamlit&descAlignY=58&descSize=14" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.10-f97316?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-06b6d4?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-22c55e?style=for-the-badge&logo=pandas&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-Active%20Ready-22c55e?style=for-the-badge&logoColor=white)]()

</div>

---

## What is AI Data Analyst?

This is a **production-ready data analysis tool** that automatically cleans missing values and generates statistical insights from any dataset.

Instead of manually cleaning data and calculating statistics, this tool gives you the ability to **upload any file** and get **instant insights** with interactive visualizations.
Upload File (CSV/Excel/JSON)
↓
AI detects column data types
↓
Auto-fills missing values based on column type
↓
Generates statistics for each column
↓
Creates interactive visualizations
↓
Download cleaned data (CSV/Excel)

text

---

## Data Cleaning Logic

| Column Type | Detection | Filling Method |
|-------------|-----------|----------------|
| Numeric (int, float) | dtype detection | Mean value |
| Year columns | contains 'year' keyword | Median value |
| Text/Object | string data | "unknown" |
Raw Data ──► Upload ──► Missing Value Detection
│
▼
┌─────────────────┐
│ Column Type? │
└─────────────────┘
│ │ │
▼ ▼ ▼
Numeric Year Text
│ │ │
▼ ▼ ▼
Mean Median "unknown"
│ │ │
└───────┴────────┘
│
▼
Cleaned Data ──► Statistics ──► Visualizations
│
▼
Download (CSV/Excel)

text

---

## Repository Structure
AI-Data-Analyst/
├── app.py ← Streamlit frontend
├── backend.py ← Core analysis logic
├── requirements.txt ← Dependencies
└── README.md ← Documentation

text

---

## Features

### 1. Auto Data Cleaning
- Detects missing values automatically
- Fills numeric columns with mean
- Fills year columns with median (no decimals)
- Fills text columns with "unknown"

### 2. Statistical Analysis

**For Numeric Columns:**

| Statistic | Description |
|-----------|-------------|
| count | Total non-null values |
| mean | Average value |
| std | Standard deviation |
| min | Minimum value |
| 25% | First quartile |
| 50% | Median |
| 75% | Third quartile |
| max | Maximum value |

**For Text Columns:**

| Statistic | Description |
|-----------|-------------|
| count | Total non-null values |
| unique | Number of unique values |
| most_common | Most frequent value |

### 3. Interactive Visualizations

| Chart Type | Purpose |
|------------|---------|
| Histogram | Distribution of numeric data |
| Bar Chart | Top values in text columns |
| Missing Values Chart | Visualize missing data before cleaning |

### 4. Download Options
- Export as CSV
- Export as Excel

---

## Sample Output

For a column like 'release_year':

| Statistic | Value |
|-----------|-------|
| count | 8807.00 |
| mean | 2014.18 |
| std | 8.82 |
| min | 1925.00 |
| 25% | 2013.00 |
| 50% | 2017.00 |
| 75% | 2019.00 |
| max | 2021.00 |

---

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-data-analyst.git
cd ai-data-analyst

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
Open browser at: http://localhost:8501

Requirements
bash
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
openpyxl==3.1.2
xlrd==2.0.1
Deployment
Streamlit Cloud (Free)
Push code to GitHub

Go to share.streamlit.io

Sign in with GitHub

Select repository and branch

Set main file: app.py

Click Deploy

Live URL: https://yourusername-ai-data-analyst.streamlit.app

Skills Demonstrated
https://img.shields.io/badge/Data%2520Cleaning-Auto%2520Imputation-f97316?style=flat-square
https://img.shields.io/badge/Statistical%2520Analysis-Column%2520Wise-f97316?style=flat-square
https://img.shields.io/badge/Streamlit-Full%2520UI-06b6d4?style=flat-square
https://img.shields.io/badge/Pandas-Data%2520Processing-06b6d4?style=flat-square
https://img.shields.io/badge/Plotly-Interactive%2520Charts-22c55e?style=flat-square
https://img.shields.io/badge/File%2520Handling-CSV%252FExcel%252FJSON-22c55e?style=flat-square

Tech Stack
text
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend Processing (Python/Pandas)             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Data Analysis Pipeline                  │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────────┐  │   │
│  │  │ Detect │→ │ Identify│→ │  Fill  │→ │Generate  │  │   │
│  │  │Missing │  │ Column  │  │Missing │  │Statistics│  │   │
│  │  │ Values │  │  Type   │  │ Values │  │          │  │   │
│  │  └────────┘  └────────┘  └────────┘  └──────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Visualization Engine (Plotly)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Histograms  │  │  Bar Charts │  │  Distribution Plots │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
Use Cases
Industry	Application
Business	Clean sales data, analyze trends
Research	Prepare datasets for analysis
Education	Learn data cleaning techniques
Marketing	Process customer data
<div align="center">
https://img.shields.io/badge/GitHub-YourUsername-f97316?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/Live%2520App-Streamlit%2520Cloud-f97316?style=for-the-badge&logo=streamlit&logoColor=white

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,20&height=100&section=footer" width="100%"/></div> ```
