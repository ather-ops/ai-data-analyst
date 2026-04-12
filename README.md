<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,20&height=220&section=header&text=AI%20Data%20Analyst&fontSize=58&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Upload%20Any%20Dataset%20%E2%80%94%20Get%20Instant%20Cleaning%2C%20Statistics%20%26%20Visualizations&descAlignY=58&descSize=13" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.10-f97316?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-06b6d4?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Engine-22c55e?style=for-the-badge&logo=pandas&logoColor=white)]()
[![Plotly](https://img.shields.io/badge/Plotly-Visualizations-a855f7?style=for-the-badge&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge&logoColor=white)]()

<br/>

**Upload any CSV, Excel, or JSON file. Get automatic data cleaning, statistical analysis, and interactive charts — in seconds.**

</div>

---

## What Problem Does This Solve?

Every data analyst spends **60-70% of their time cleaning data** before they can even start analysis. Missing values, wrong data types, inconsistent formats — these problems exist in every real-world dataset.

This tool automates that entire process. You upload a file, it handles the rest.

```
Raw messy dataset
        ↓
Auto-detect column types
        ↓
Smart missing value imputation
        ↓
Column-wise statistical breakdown
        ↓
Interactive visualizations
        ↓
Download cleaned data (CSV or Excel)
```

---

## Data Cleaning Logic — Smart Imputation

The engine detects the type of each column and applies the most statistically appropriate filling method.

| Column Type | Detection Method | Filling Strategy | Why |
|-------------|-----------------|-----------------|-----|
| **Numeric (int/float)** | dtype detection | Mean | Preserves distribution center |
| **Year columns** | keyword detection (`year`, `yr`) | Median | Avoids decimal years, outlier-robust |
| **Text / Categorical** | object dtype | `"unknown"` | Preserves category integrity |
| **Boolean** | bool dtype | Mode | Most common true/false |

### Pipeline Flow

```
Raw Data
   │
   ▼
Upload (CSV / Excel / JSON)
   │
   ▼
┌──────────────────────────────┐
│   Missing Value Detection    │
│   isnull().sum() per column  │
└──────────────────────────────┘
   │
   ▼
┌──────────────────────────────┐
│     Column Type Check        │
│                              │
│  Numeric → Mean              │
│  Year    → Median (int)      │
│  Text    → "unknown"         │
└──────────────────────────────┘
   │
   ▼
┌──────────────────────────────┐
│   Statistical Analysis       │
│   count, mean, std, min,     │
│   25%, 50%, 75%, max         │
└──────────────────────────────┘
   │
   ▼
┌──────────────────────────────┐
│   Interactive Visualizations │
│   Histogram / Bar / Missing  │
└──────────────────────────────┘
   │
   ▼
Download Cleaned Dataset
```

---

## Features

### 1. Automatic Missing Value Detection
Detects all missing values across every column before any processing. Shows a visual missing-value chart so you can see the state of your raw data before cleaning begins.

### 2. Smart Imputation Engine
No manual configuration required. The engine reads column names and data types and selects the right strategy automatically.

### 3. Column-Wise Statistical Analysis

**For Numeric Columns:**

| Statistic | What It Tells You |
|-----------|------------------|
| `count` | How many non-null values exist |
| `mean` | Average — central tendency |
| `std` | Spread of values around mean |
| `min` / `max` | Extreme values — outlier hints |
| `25%` / `50%` / `75%` | Distribution quartiles |

**For Text / Categorical Columns:**

| Statistic | What It Tells You |
|-----------|------------------|
| `count` | How many non-null entries |
| `unique` | Cardinality — how many distinct values |
| `most_common` | Dominant category |

### 4. Interactive Visualizations (Plotly)

| Chart | Column Type | Purpose |
|-------|-------------|---------|
| Histogram | Numeric | See value distribution and skew |
| Bar Chart | Categorical | Top N most frequent values |
| Missing Values Chart | All columns | Before/after cleaning comparison |

### 5. Download Options
- Export cleaned data as **CSV**
- Export cleaned data as **Excel (.xlsx)**

---

## Repository Structure

```
AI-Data-Analyst/
├── app.py              ← Streamlit UI — file upload, display, download
├── backend.py          ← Core logic — cleaning, stats, chart generation
├── requirements.txt    ← All dependencies
└── README.md           ← This file
```

### Architecture

```
┌─────────────────────────────────────────────┐
│           Streamlit UI  (app.py)            │
│  File Upload → Display → Charts → Download  │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         Backend Engine  (backend.py)        │
│                                             │
│  detect_missing()   → isnull analysis       │
│  identify_type()    → dtype + name check    │
│  fill_missing()     → mean/median/unknown   │
│  generate_stats()   → describe() per col    │
│  generate_charts()  → Plotly figures        │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│      Visualization Engine  (Plotly)         │
│  Histogram  │  Bar Chart  │  Missing Chart  │
└─────────────────────────────────────────────┘
```

---

## Sample Output — Netflix Dataset

Input: `netflix_titles.csv` — 8,807 rows, 12 columns, 3 columns with missing values

| Column | Missing Before | Method Used | Missing After |
|--------|---------------|-------------|---------------|
| `director` | 2,634 | `"unknown"` | 0 |
| `cast` | 825 | `"unknown"` | 0 |
| `country` | 831 | `"unknown"` | 0 |
| `release_year` | 0 | — | 0 |

**Statistics generated for `release_year`:**

| Statistic | Value |
|-----------|-------|
| count | 8807 |
| mean | 2014.18 |
| std | 8.82 |
| min | 1925 |
| 25% | 2013 |
| 50% | 2017 |
| 75% | 2019 |
| max | 2021 |

---

## Installation and Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/ather-ops/ai-data-analyst
cd ai-data-analyst

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open browser at: `http://localhost:8501`

---

## Requirements

```
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
openpyxl==3.1.2
xlrd==2.0.1
```

---

## Deploy to Streamlit Cloud (Free)

```
1. Push code to GitHub
2. Go to share.streamlit.io
3. Sign in with GitHub
4. Select your repository
5. Set main file: app.py
6. Click Deploy
```

Live URL format: `https://ather-ops-ai-data-analyst.streamlit.app`

---

## Skills Demonstrated

[![Data Cleaning](https://img.shields.io/badge/Data%20Cleaning-Smart%20Imputation-f97316?style=flat-square)]()
[![Statistical Analysis](https://img.shields.io/badge/Statistical%20Analysis-Column%20Wise-f97316?style=flat-square)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Production%20UI-06b6d4?style=flat-square)]()
[![Pandas](https://img.shields.io/badge/Pandas-Full%20Pipeline-06b6d4?style=flat-square)]()
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-22c55e?style=flat-square)]()
[![File Handling](https://img.shields.io/badge/File%20Handling-CSV%20Excel%20JSON-22c55e?style=flat-square)]()
[![Error Handling](https://img.shields.io/badge/Error%20Handling-Production%20Ready-a855f7?style=flat-square)]()

---

## Use Cases

| Domain | Application |
|--------|-------------|
| Business Analytics | Clean sales data, customer records, transaction logs |
| Machine Learning | Prepare raw datasets before model training |
| Research | Process survey data, experiment results |
| Education | Learn data cleaning techniques interactively |
| Marketing | Analyze campaign data and customer segments |

---

## Connection to Larger Projects

This tool directly feeds into the **Cortex-RAG** and **CineSense AI** pipelines:

```
AI Data Analyst          Cortex-RAG           CineSense AI
─────────────            ──────────           ────────────
Clean dataset     →      Embed cleaned   →    Semantic search
Fill missing vals         data in            on clean vectors
Generate stats            ChromaDB
Download CSV
```

A clean dataset leads to better embeddings. Better embeddings lead to more accurate semantic search. This tool is the first step in that chain.

---

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-ather--ops-f97316?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ather-ops)
[![Live App](https://img.shields.io/badge/Live%20App-Rain%20Predictor-06b6d4?style=for-the-badge&logo=streamlit&logoColor=white)](https://rain-predictor-app.streamlit.app)
[![Cortex-RAG](https://img.shields.io/badge/Repo-Cortex--RAG-a855f7?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ather-ops/Cortex-RAG)

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,20&height=100&section=footer" width="100%"/>

</div>
