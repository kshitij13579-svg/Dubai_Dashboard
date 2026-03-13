# 🍽️ DinePrice Dubai — Dynamic Restaurant Pricing System

**An AI-driven dynamic pricing engine for Dubai restaurants** that optimizes menu prices in real-time based on demand signals, weather, time-of-day, and customer segments.

This repository contains the **Exploratory Data Analysis (EDA)** dashboard and supporting data pipeline for market validation through a synthetic customer survey (2,500+ respondents).

---

## 📊 Live Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

> Replace the URL above with your deployed Streamlit link.

---

## 🏗️ Project Structure

```
dubai-pricing-dashboard/
├── app.py                          # Streamlit dashboard (main)
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit theme config
├── data/
│   ├── data_raw.csv                # Raw synthetic survey (2,550 rows, dirty)
│   └── data_clean.csv              # Cleaned dataset (2,517 rows)
├── src/
│   ├── 01_generate_data.py         # Synthetic data generation script
│   └── 02_clean_data.py            # Data cleaning & transformation pipeline
├── notebooks/                      # (Optional) Jupyter notebooks
└── assets/                         # Screenshots, diagrams
```

---

## 🎯 Business Context

Dubai's F&B market (13,000+ restaurants) suffers from:
- **Revenue leakage** during off-peak hours (empty tables)
- **Lost demand** during peak hours (overcrowding, no price signal)
- **Flat pricing** that ignores demand variability driven by weather, tourism seasons, and weekend culture

**DinePrice** solves this by providing a SaaS pricing engine that dynamically adjusts menu prices based on:
- Demand level (Low / Medium / High)
- Time of day and day of week
- Weather conditions (extreme heat drives delivery)
- Customer segment and price sensitivity
- Table occupancy rates

---

## 📋 Survey Design

25 questions + 1 classification target capturing:

| Section | Questions | Analytics Use |
|---------|-----------|---------------|
| Demographics | Age, Income, Type, Nationality, Loyalty | Clustering, Segmentation |
| Dining Behaviour | Frequency, Time, Channel, Group, Distance | Clustering, Regression |
| Preferences | Cuisine, Tier, Location | Clustering, Association |
| Price Sensitivity | Sensitivity, Off-peak, Fairness, Discounts | Classification, Clustering |
| Challenges | Multi-select: 8 pain points | Association Rule Mining |
| Features | Multi-select: 8 desired features | Association Rule Mining |
| Attitudes | Weather impact, Seasonality, Rating | Clustering, Regression |
| Target | App Adoption (Yes/No) | Classification |

---

## 📈 Dashboard Sections

| # | Section | Key Insights |
|---|---------|-------------|
| 0 | Overview & KPIs | Adoption rate, spend, surge, delivery share |
| 1 | Customer Profile | Age×Income heatmap, Nationality sunburst |
| 2 | Dining Behaviour | Time by age, channel by age, frequency by income |
| 3 | Price Sensitivity | Sensitivity by income, discount motivation, fairness by age |
| 4 | Dynamic Pricing System | Demand distribution, surge impact, occupancy analysis |
| 5 | Location & Cuisine | Location by income, cuisine by nationality, spend by area |
| 6 | Delivery vs Dine-in | Channel split, weather impact, distance vs time |
| 7 | Correlation Analysis | Full correlation matrix, income vs spend, surge vs rating |
| 8 | Challenges & Features | Top pain points, co-occurrence matrices, ARM preview |
| 9 | App Adoption Deep Dive | Adoption by 10 dimensions, sensitivity×fairness heatmap |
| 10 | Seasonality | Peak months, season by customer type, demand by season |
| 🔀 | Sankey Diagrams | 3 Sankey flows connecting all dimensions to App Adoption |

---

## 🔀 Sankey Diagrams (North Star Flow)

Three Sankey diagrams trace every customer attribute to the **North Star metric (App Adoption)**:

1. **Customer Type → Price Sensitivity → Fairness → Adoption**
2. **Order Channel → Demand Level → Surge Bucket → Adoption**
3. **Income → Restaurant Tier → Location → Adoption**

---

## 🧹 Data Pipeline

### 1. Synthetic Data Generation (`src/01_generate_data.py`)
- 2,500 base records with **realistic cross-variable correlations**
  - Age → Income, Customer Type, Order Time, Channel
  - Income → Frequency, Tier, Location, Sensitivity
  - Nationality → Cuisine preference
  - Sensitivity → Discount motivation, Off-peak willingness
- System-generated variables: Demand Level, Surge Multiplier, Table Occupancy, Final Order Value
- Deliberately injected: duplicates, nulls, typos, outliers, logical contradictions

### 2. Data Cleaning (`src/02_clean_data.py`)
- Removed 33 duplicate rows
- Fixed typos across 6 columns
- Imputed nulls (mode for categorical, median for numerical)
- Clipped outliers to realistic Dubai ranges
- Recalculated derived fields

---

## 🚀 Run Locally

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/dubai-pricing-dashboard.git
cd dubai-pricing-dashboard

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Interactive dashboard
- **Plotly** — Visualizations (heatmaps, Sankey, sunburst, scatter)
- **Pandas / NumPy** — Data processing

---

## 📚 Analytics Roadmap (Group Phase)

| Technique | Target | Features |
|-----------|--------|----------|
| Classification | App_Adoption (Yes/No) | All demographic + behavioural features |
| Regression | Avg_Spend_AED | Income, Tier, Group, Cuisine, Frequency |
| Clustering (K-Means, LCA) | Customer Personas | Demographics + behaviour + attitudes |
| Association Rules (Apriori) | Challenge→Feature patterns | Multi-select columns |

---

## 👤 Author

**Vivek** — GMBA Student, SP Jain School of Global Management (Jan 2025 Cohort)

---

## 📄 License

This project is for academic purposes (Data Analytics — MGB, SP Jain).
