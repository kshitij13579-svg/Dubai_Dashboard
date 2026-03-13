"""
Data Cleaning & Transformation Pipeline
Dubai Dynamic Restaurant Pricing Survey
========================================
Input:  dubai_dynamic_pricing_survey_RAW.csv (2550 rows, dirty)
Output: dubai_dynamic_pricing_survey_CLEAN.csv (~2200 rows, clean)
"""

import pandas as pd
import numpy as np

# =============================================================================
# 1. LOAD RAW DATA
# =============================================================================

df = pd.read_csv("dubai_dynamic_pricing_survey_RAW.csv")
print(f"RAW DATA: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Nulls total: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

log = []  # cleaning log

# =============================================================================
# 2. REMOVE DUPLICATES
# =============================================================================

before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
after = len(df)
log.append(f"Duplicates removed: {before - after} rows")
print(f"\n[STEP 1] Removed {before - after} duplicate rows → {len(df)} rows remain")

# =============================================================================
# 3. FIX TYPOS & INCONSISTENT FORMATTING
# =============================================================================

# Customer_Type
ctype_fix = {
    "Profesional": "Professional",
    "Studnet": "Student",
    "Touri st": "Tourist",
}
df["Customer_Type"] = df["Customer_Type"].replace(ctype_fix).str.strip().str.title()

# Order_Channel — standardize casing
channel_fix = {
    "dine-in": "Dine-in",
    "DELIVERY APP": "Delivery App",
    "Take away": "Takeaway",
}
df["Order_Channel"] = df["Order_Channel"].replace(channel_fix).str.strip()

# Cuisine_Preference
cuisine_fix = {
    "Arebic": "Arabic",
    "indian/pakistani": "Indian/Pakistani",
    "WESTERN": "Western",
}
df["Cuisine_Preference"] = df["Cuisine_Preference"].replace(cuisine_fix).str.strip()

# Day_Preference
day_fix = {
    "Weekend": "Weekends",
    "weekdays": "Weekdays",
}
df["Day_Preference"] = df["Day_Preference"].replace(day_fix).str.strip()

# Restaurant_Tier — normalize
tier_fix = {
    "budget/casual": "Budget/Casual",
    "Premium / Fine dining": "Premium/Fine Dining",
    "Premium / Fine Dining": "Premium/Fine Dining",
}
df["Restaurant_Tier"] = df["Restaurant_Tier"].replace(tier_fix).str.strip()

# Nationality_Cluster
nat_fix = {
    "south asian": "South Asian",
    "western expat": "Western Expat",
}
df["Nationality_Cluster"] = df["Nationality_Cluster"].replace(nat_fix).str.strip()

log.append("Typos & formatting fixed across 6 columns")
print("[STEP 2] Typos & formatting standardized")

# Verify unique values after cleanup
for col in ["Customer_Type", "Order_Channel", "Cuisine_Preference", "Day_Preference",
            "Restaurant_Tier", "Nationality_Cluster"]:
    print(f"  {col}: {sorted(df[col].dropna().unique())}")

# =============================================================================
# 4. HANDLE MISSING VALUES
# =============================================================================

print(f"\n[STEP 3] Handling missing values...")
print(f"  Nulls before:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Strategy:
# - Categorical columns: fill with mode (most frequent value)
# - Numerical columns: fill with median
# - Structurally null columns (Table_Occupancy for delivery, Delivery cols for dine-in): leave as NaN

categorical_fill = [
    "Monthly_Income", "Loyalty_Status", "Dining_Frequency",
    "Cuisine_Preference", "Restaurant_Tier", "Price_Sensitivity",
    "Fairness_Perception", "Weather_Behaviour"
]

for col in categorical_fill:
    mode_val = df[col].mode()[0]
    filled = df[col].isnull().sum()
    df[col] = df[col].fillna(mode_val)
    if filled > 0:
        print(f"  Filled {filled} nulls in {col} with mode: '{mode_val}'")

# Experience_Rating — fill with median
med_rating = df["Experience_Rating"].median()
filled_r = df["Experience_Rating"].isnull().sum()
df["Experience_Rating"] = df["Experience_Rating"].fillna(med_rating)
print(f"  Filled {filled_r} nulls in Experience_Rating with median: {med_rating}")

# Avg_Spend_AED, Base_Order_Value — fill with median by income group
for col in ["Avg_Spend_AED", "Base_Order_Value"]:
    null_mask = df[col].isnull()
    if null_mask.sum() > 0:
        medians_by_income = df.groupby("Monthly_Income")[col].transform("median")
        df[col] = df[col].fillna(medians_by_income)
        # If still null (income was also null before), use global median
        df[col] = df[col].fillna(df[col].median())
        print(f"  Filled {null_mask.sum()} nulls in {col} with income-group median")

# Surge_Multiplier — fill with median by Demand_Level
null_surge = df["Surge_Multiplier"].isnull().sum()
if null_surge > 0:
    surge_med = df.groupby("Demand_Level")["Surge_Multiplier"].transform("median")
    df["Surge_Multiplier"] = df["Surge_Multiplier"].fillna(surge_med)
    df["Surge_Multiplier"] = df["Surge_Multiplier"].fillna(df["Surge_Multiplier"].median())
    print(f"  Filled {null_surge} nulls in Surge_Multiplier with demand-level median")

# Recalculate Final_Order_Value where missing
null_fov = df["Final_Order_Value"].isnull().sum()
df["Final_Order_Value"] = df["Final_Order_Value"].fillna(
    df["Base_Order_Value"] * df["Surge_Multiplier"]
)
print(f"  Recalculated {null_fov} nulls in Final_Order_Value")

# Customer_Rating — sync with Experience_Rating
df["Customer_Rating"] = df["Experience_Rating"].astype(int)

# Structural NaNs — leave as-is (Table_Occupancy for delivery, Delivery cols for dine-in)
print(f"\n  Structural NaNs (expected):")
print(f"    Table_Occupancy_Pct: {df['Table_Occupancy_Pct'].isnull().sum()} (delivery/takeaway orders)")
print(f"    Delivery_Distance_km: {df['Delivery_Distance_km'].isnull().sum()} (dine-in orders)")
print(f"    Est_Delivery_Time_min: {df['Est_Delivery_Time_min'].isnull().sum()} (dine-in orders)")

log.append("Missing values imputed (mode for categorical, median for numerical)")

# =============================================================================
# 5. HANDLE OUTLIERS
# =============================================================================

print(f"\n[STEP 4] Handling outliers...")

# Avg_Spend_AED / Base_Order_Value — cap at reasonable Dubai range
for col in ["Avg_Spend_AED", "Base_Order_Value"]:
    before_outliers = ((df[col] < 15) | (df[col] > 800)).sum()
    df[col] = df[col].clip(lower=15, upper=800)
    print(f"  {col}: clipped {before_outliers} outliers to [15, 800] AED")

# Recalculate Final_Order_Value after clipping base
df["Final_Order_Value"] = (df["Base_Order_Value"] * df["Surge_Multiplier"]).round(2)

# Surge_Multiplier — cap at realistic range [0.75, 1.40]
surge_outliers = ((df["Surge_Multiplier"] < 0.75) | (df["Surge_Multiplier"] > 1.40)).sum()
df["Surge_Multiplier"] = df["Surge_Multiplier"].clip(lower=0.75, upper=1.40)
print(f"  Surge_Multiplier: clipped {surge_outliers} outliers to [0.75, 1.40]")

# Table_Occupancy_Pct — must be 0-100
occ_mask = df["Table_Occupancy_Pct"].notna()
occ_outliers = ((df.loc[occ_mask, "Table_Occupancy_Pct"] < 0) |
                (df.loc[occ_mask, "Table_Occupancy_Pct"] > 100)).sum()
df.loc[occ_mask, "Table_Occupancy_Pct"] = df.loc[occ_mask, "Table_Occupancy_Pct"].clip(0, 100)
print(f"  Table_Occupancy_Pct: clipped {occ_outliers} outliers to [0, 100]")

# Delivery_Distance_km — cap at 30 km (Dubai is ~60km end to end)
del_mask = df["Delivery_Distance_km"].notna()
del_outliers = ((df.loc[del_mask, "Delivery_Distance_km"] < 0.5) |
                (df.loc[del_mask, "Delivery_Distance_km"] > 30)).sum()
df.loc[del_mask, "Delivery_Distance_km"] = df.loc[del_mask, "Delivery_Distance_km"].clip(0.5, 30)
print(f"  Delivery_Distance_km: clipped {del_outliers} outliers to [0.5, 30]")

# Recalculate Discount_Percentage
df["Discount_Percentage"] = df["Surge_Multiplier"].apply(
    lambda x: round(max(0, (1 - x) * 100), 1) if x < 1.0 else 0.0
)

log.append("Outliers clipped to realistic ranges")

# =============================================================================
# 6. DATA TYPE CLEANUP & FINAL VALIDATION
# =============================================================================

print(f"\n[STEP 5] Final validation...")

# Experience_Rating as int
df["Experience_Rating"] = df["Experience_Rating"].astype(int)
df["Customer_Rating"] = df["Customer_Rating"].astype(int)

# Ensure Est_Delivery_Time_min is numeric
df["Est_Delivery_Time_min"] = pd.to_numeric(df["Est_Delivery_Time_min"], errors="coerce")

# Round numeric columns
for col in ["Avg_Spend_AED", "Base_Order_Value", "Final_Order_Value",
            "Surge_Multiplier", "Table_Occupancy_Pct", "Delivery_Distance_km"]:
    df[col] = df[col].round(2)

# Final shape
print(f"\nFINAL CLEAN DATA: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Non-structural nulls: {df[['Age','Monthly_Income','Customer_Type','App_Adoption']].isnull().sum().sum()}")
print(f"\nApp_Adoption distribution:")
print(df["App_Adoption"].value_counts())
print(f"\nCleaning Log:")
for entry in log:
    print(f"  • {entry}")

# =============================================================================
# 7. SAVE CLEAN DATA
# =============================================================================

df.to_csv("dubai_dynamic_pricing_survey_CLEAN.csv", index=False)
print(f"\nSaved to: dubai_dynamic_pricing_survey_CLEAN.csv")

# Quick stats
print(f"\n{'='*50}")
print("NUMERIC COLUMN STATS")
print('='*50)
print(df.describe().round(2).to_string())
