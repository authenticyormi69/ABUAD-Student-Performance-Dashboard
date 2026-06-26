# Create README.md
@"
# 📊 ABUAD Student Performance Dashboard

Data Analytics System for Predicting Students' Academic Performance at Afe Babalola University Ado-Ekiti

## 🎯 Project Overview

A comprehensive analytics dashboard that monitors and predicts student academic performance using machine learning and data visualization.

**Institution:** Afe Babalola University Ado-Ekiti (ABUAD)  
**Supervisor:** Dr. Josephine Mebawondu  
**Developer:** AGBELEKALE TOHEEB ORIYOMI (AUTHENTIC)

---

## 📈 Key Features

### 📊 6 Interactive Dashboard Tabs

1. **📊 Overview** - KPIs, Risk Distribution, Grade & Attendance Charts
2. **🏫 By College** - College-Level Performance Analysis (5 Colleges)
3. **📚 By Department** - Department-Specific Insights (10 Departments)
4. **👥 Demographics** - Gender & Academic Level Analysis
5. **⚠️ At-Risk Students** - Detailed Intervention Data (200+ Students)
6. **💡 Interventions** - Evidence-Based Support Framework

### 🔍 8 Interactive Filters

- College & Department Selection
- Academic Level Filter
- Risk Category Classification
- Grade Point Range
- Attendance Rate Range
- Gender Analysis
- Dynamic Data Slicing

---

## 🎓 Academic Data

- **Total Students:** 1,000
- **Colleges:** 5
- **Departments:** 10
- **At-Risk Students:** 200+
- **Data Points per Student:** 20+ attributes

---

## ⚙️ Risk Scoring Formula

\`\`\`
Risk Score = 0.4×Grade + 0.3×CA + 0.2×Attendance + 0.1×Engagement
\`\`\`

### Risk Categories

| Category | Score Range | Status |
|----------|------------|--------|
| 🔴 At Risk | < 45 | Requires Intervention |
| 🟡 Needs Monitoring | 45–69 | Monitor Progress |
| 🟢 On Track | ≥ 70 | Performing Well |

---

## 💻 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.28.1 |
| **Data Processing** | Pandas 2.0.3, NumPy 1.24.3 |
| **Visualization** | Plotly 5.17.0 |
| **Analytics** | Scikit-learn |
| **Database** | Excel CSV Pipeline |

---

## 🚀 Quick Start

### Local Installation

\`\`\`bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ABUAD-Student-Performance-Dashboard.git
cd ABUAD-Student-Performance-Dashboard

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\\Scripts\\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app_PRODUCTION_FINAL.py
\`\`\`

### Access Dashboard

Open your browser and navigate to:
\`\`\`
http://localhost:8501
\`\`\`

---

## 📁 Project Structure

\`\`\`
ABUAD-Student-Performance-Dashboard/
├── app_PRODUCTION_FINAL.py      # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── data/
│   └── student_performance.xlsx  # Dataset
└── models/
    └── (ML models if added)
\`\`\`

---

## 📊 Dashboard Insights

### Performance Distribution
- **Overview Tab** shows student performance across all metrics
- **Real-time KPI cards** displaying key statistics
- **Interactive charts** for grade and attendance analysis

### Risk Identification
- Automated **at-risk student flagging**
- **Detailed student profiles** with all academic metrics
- **Intervention recommendations** based on risk category

### College & Department Analysis
- **Comparative performance metrics** across 5 colleges
- **Department-level insights** across 10 departments
- **Trend analysis** and performance benchmarking

---

## 🔧 Configuration

The dashboard is configured via \`.streamlit/config.toml\`:

\`\`\`toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
\`\`\`

---

## 📋 Data Pipeline

1. **Data Source:** Excel workbook with 1,000 student records
2. **Data Processing:** Pandas-based ETL pipeline
3. **Risk Calculation:** Weighted scoring algorithm
4. **Visualization:** Interactive Plotly charts
5. **Filtering:** Real-time dashboard filtering with Streamlit

---

## 👨‍💼 Contact & Support

**Project Lead:** AGBELEKALE TOHEEB ORIYOMI (AUTHENTIC)

**Questions?** Refer to the dashboard tooltips or contact your supervisor.

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🎓 Academic Citation

\`\`\`
AGBELEKALE, T. O. (2026). Data Analytics for Predicting Students' Academic 
Performance: A Case Study of Afe Babalola University Ado-Ekiti. 
Final Year Project, ABUAD.
\`\`\`

---

**Last Updated:** June 2026  
**Status:** ✅ Production Ready
"@ | Out-File -Encoding UTF8 README.md