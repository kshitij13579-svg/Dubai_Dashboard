import numpy as np
import pandas as pd
import random

np.random.seed(42)
random.seed(42)

n = 2500

# =============================================================================
# OPTION LISTS & BASE PROBABILITIES
# =============================================================================

age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
age_base_prob = [0.25, 0.35, 0.20, 0.12, 0.08]

income_groups = ["<5000", "5000-10000", "10001-20000", "20001-35000", ">35000"]

# Income conditioned on age (rows=age, cols=income)
income_given_age = {
    "18-24":  [0.45, 0.35, 0.15, 0.04, 0.01],
    "25-34":  [0.10, 0.30, 0.35, 0.18, 0.07],
    "35-44":  [0.05, 0.15, 0.30, 0.30, 0.20],
    "45-54":  [0.05, 0.10, 0.25, 0.30, 0.30],
    "55+":    [0.08, 0.15, 0.25, 0.27, 0.25],
}

customer_types = ["Student", "Professional", "Family", "Tourist"]
ctype_given_age = {
    "18-24":  [0.60, 0.25, 0.05, 0.10],
    "25-34":  [0.10, 0.55, 0.20, 0.15],
    "35-44":  [0.02, 0.45, 0.40, 0.13],
    "45-54":  [0.01, 0.35, 0.45, 0.19],
    "55+":    [0.01, 0.20, 0.45, 0.34],
}

nationalities = ["South Asian", "Arab", "Western Expat", "East Asian", "African"]
nationality_prob = [0.45, 0.20, 0.18, 0.10, 0.07]

loyalty_options = ["Explorer", "Few regulars", "Loyal to 1-2", "Loyalty program user"]
loyalty_given_ctype = {
    "Student":      [0.45, 0.30, 0.20, 0.05],
    "Professional": [0.15, 0.35, 0.30, 0.20],
    "Family":       [0.10, 0.25, 0.45, 0.20],
    "Tourist":      [0.70, 0.20, 0.05, 0.05],
}

# --- Dining Behaviour ---

frequency_options = ["Multiple/week", "Once/week", "2-3/month", "Once/month", "Rarely"]
freq_given_income = {
    "<5000":       [0.10, 0.20, 0.30, 0.25, 0.15],
    "5000-10000":  [0.20, 0.30, 0.25, 0.15, 0.10],
    "10001-20000": [0.25, 0.35, 0.22, 0.12, 0.06],
    "20001-35000": [0.35, 0.30, 0.20, 0.10, 0.05],
    ">35000":      [0.45, 0.30, 0.15, 0.07, 0.03],
}

order_times = ["Breakfast", "Lunch", "Dinner", "Late Night"]
time_given_age = {
    "18-24":  [0.05, 0.20, 0.40, 0.35],
    "25-34":  [0.10, 0.30, 0.40, 0.20],
    "35-44":  [0.15, 0.30, 0.40, 0.15],
    "45-54":  [0.20, 0.35, 0.35, 0.10],
    "55+":    [0.30, 0.35, 0.30, 0.05],
}

day_options = ["Weekdays", "Weekends", "Both"]
day_prob = [0.20, 0.35, 0.45]

channels = ["Dine-in", "Delivery App", "Takeaway", "Restaurant App"]
channel_given_age = {
    "18-24":  [0.20, 0.55, 0.15, 0.10],
    "25-34":  [0.30, 0.45, 0.15, 0.10],
    "35-44":  [0.40, 0.35, 0.15, 0.10],
    "45-54":  [0.45, 0.30, 0.15, 0.10],
    "55+":    [0.50, 0.25, 0.15, 0.10],
}

group_sizes = ["Alone", "2 people", "3-4 people", "5+"]
group_given_ctype = {
    "Student":      [0.35, 0.35, 0.25, 0.05],
    "Professional": [0.30, 0.40, 0.20, 0.10],
    "Family":       [0.05, 0.20, 0.45, 0.30],
    "Tourist":      [0.15, 0.40, 0.35, 0.10],
}

distances = ["<3km", "3-7km", "7-15km", ">15km"]
distance_prob = [0.35, 0.40, 0.20, 0.05]

cuisines = ["Arabic", "Indian/Pakistani", "Asian", "Western", "Fast Food", "Healthy/Vegan"]
cuisine_given_nationality = {
    "South Asian":   [0.10, 0.45, 0.15, 0.10, 0.15, 0.05],
    "Arab":          [0.40, 0.15, 0.10, 0.15, 0.10, 0.10],
    "Western Expat": [0.10, 0.10, 0.15, 0.35, 0.10, 0.20],
    "East Asian":    [0.05, 0.10, 0.45, 0.15, 0.15, 0.10],
    "African":       [0.15, 0.20, 0.15, 0.15, 0.25, 0.10],
}

tiers = ["Budget/Casual", "Mid-range", "Premium/Fine Dining", "Depends on occasion"]
tier_given_income = {
    "<5000":       [0.55, 0.30, 0.02, 0.13],
    "5000-10000":  [0.40, 0.38, 0.05, 0.17],
    "10001-20000": [0.20, 0.42, 0.15, 0.23],
    "20001-35000": [0.10, 0.30, 0.35, 0.25],
    ">35000":      [0.05, 0.20, 0.50, 0.25],
}

locations = ["Downtown", "Marina", "DIFC", "JBR", "Deira", "Business Bay", "Mall"]
location_given_income = {
    "<5000":       [0.05, 0.05, 0.02, 0.05, 0.45, 0.08, 0.30],
    "5000-10000":  [0.08, 0.10, 0.05, 0.10, 0.30, 0.12, 0.25],
    "10001-20000": [0.12, 0.15, 0.10, 0.15, 0.15, 0.15, 0.18],
    "20001-35000": [0.20, 0.20, 0.20, 0.15, 0.05, 0.12, 0.08],
    ">35000":      [0.25, 0.20, 0.25, 0.12, 0.03, 0.10, 0.05],
}

# --- Price Sensitivity & Attitudes ---

sensitivity_options = ["Very sensitive", "Moderately sensitive", "Slightly sensitive", "Not sensitive"]
sensitivity_given_income = {
    "<5000":       [0.55, 0.30, 0.10, 0.05],
    "5000-10000":  [0.40, 0.35, 0.18, 0.07],
    "10001-20000": [0.25, 0.40, 0.25, 0.10],
    "20001-35000": [0.15, 0.30, 0.35, 0.20],
    ">35000":      [0.08, 0.20, 0.32, 0.40],
}

offpeak_options = ["Definitely yes", "Probably yes", "Maybe", "Probably not", "Definitely not"]
fairness_options = ["Very fair", "Somewhat fair", "Neutral", "Unfair", "Very unfair"]
discount_importance_options = ["Extremely important", "Very important", "Moderately important",
                                "Slightly important", "Not important"]

discount_motivation_options = ["5%", "10%", "15%", "20%", ">20%"]
discount_given_sensitivity = {
    "Very sensitive":       [0.02, 0.10, 0.25, 0.35, 0.28],
    "Moderately sensitive": [0.05, 0.25, 0.35, 0.25, 0.10],
    "Slightly sensitive":   [0.10, 0.35, 0.30, 0.18, 0.07],
    "Not sensitive":        [0.25, 0.35, 0.25, 0.10, 0.05],
}

weather_options = ["Dine-in more during heat", "Switch to delivery in heat",
                   "No impact", "Outdoor dining in pleasant weather"]
weather_prob = [0.12, 0.48, 0.20, 0.20]

month_options = ["Oct-Dec", "Jan-Mar", "Apr-Jun", "Jul-Sep"]

rating_options = [1, 2, 3, 4, 5]
rating_prob = [0.03, 0.08, 0.25, 0.40, 0.24]

# --- Multi-select: Challenges & Features ---

challenges_list = [
    "High weekend prices", "Long wait times", "High delivery fees",
    "Limited discounts", "Crowded restaurants", "Unpredictable pricing",
    "Long delivery time", "Hard to find tables"
]

features_list = [
    "Real-time pricing", "Low-demand discounts", "Table availability",
    "Wait time estimate", "Demand alerts", "Loyalty rewards",
    "Personalised discounts", "Group dining deals"
]


def multi_select(options, min_sel=1, max_sel=4):
    k = random.randint(min_sel, max_sel)
    return random.sample(options, min(k, len(options)))


def month_select_seasonal():
    """Dubai dining peaks Oct-Mar, drops Jul-Sep"""
    weights = [0.35, 0.30, 0.20, 0.15]  # Oct-Dec, Jan-Mar, Apr-Jun, Jul-Sep
    k = random.randint(1, 3)
    chosen = np.random.choice(month_options, size=k, replace=False, p=weights)
    return list(chosen)


# =============================================================================
# SYSTEM-GENERATED VARIABLES (derived, not surveyed)
# =============================================================================

def derive_demand_level(day, time, month_list):
    """Demand driven by day, time, and season"""
    score = 0
    if day in ["Weekends", "Both"]:
        score += 1
    if time in ["Dinner", "Late Night"]:
        score += 1
    if any(m in ["Oct-Dec", "Jan-Mar"] for m in month_list):
        score += 1
    if score >= 3:
        return "High"
    elif score >= 1:
        return "Medium"
    else:
        return "Low"


def derive_surge(demand, tier):
    """Surge multiplier based on demand + restaurant tier"""
    base_surge = {"Low": 0.85, "Medium": 1.0, "High": 1.20}
    tier_adj = {"Budget/Casual": -0.05, "Mid-range": 0.0,
                "Premium/Fine Dining": 0.10, "Depends on occasion": 0.0}
    surge = base_surge[demand] + tier_adj.get(tier, 0) + np.random.normal(0, 0.05)
    return round(np.clip(surge, 0.75, 1.40), 2)


def derive_occupancy(demand, time):
    """Table occupancy % for dine-in"""
    base = {"Low": 30, "Medium": 55, "High": 80}
    time_adj = {"Breakfast": -10, "Lunch": 5, "Dinner": 10, "Late Night": -5}
    occ = base[demand] + time_adj.get(time, 0) + np.random.normal(0, 10)
    return round(np.clip(occ, 10, 100), 1)


def derive_spend(income, tier, group):
    """Average spend correlated with income, tier, and group size"""
    income_base = {
        "<5000": 40, "5000-10000": 65, "10001-20000": 95,
        "20001-35000": 140, ">35000": 220
    }
    tier_mult = {"Budget/Casual": 0.75, "Mid-range": 1.0,
                 "Premium/Fine Dining": 1.8, "Depends on occasion": 1.1}
    group_mult = {"Alone": 0.8, "2 people": 1.0, "3-4 people": 1.3, "5+": 1.6}

    base = income_base[income]
    mult = tier_mult.get(tier, 1.0) * group_mult.get(group, 1.0)
    spend = base * mult + np.random.normal(0, base * 0.15)
    return round(max(15, spend), 2)


def derive_delivery_distance(channel, dist_category):
    """Continuous distance in km, null for dine-in"""
    if channel == "Dine-in":
        return np.nan
    dist_map = {"<3km": (1, 3), "3-7km": (3, 7), "7-15km": (7, 15), ">15km": (15, 25)}
    low, high = dist_map[dist_category]
    return round(np.random.uniform(low, high), 1)


def derive_delivery_time(distance_km, channel):
    """Delivery time in minutes, null for dine-in"""
    if channel == "Dine-in" or pd.isna(distance_km):
        return np.nan
    base_time = 15 + distance_km * 2.5 + np.random.normal(0, 5)
    return round(np.clip(base_time, 12, 75), 0)


def derive_adoption(sensitivity, discount_mot, channel, fairness, offpeak, rating):
    """Classification target with multi-factor logic"""
    prob = 0.45

    # Price sensitivity
    sens_adj = {"Very sensitive": 0.18, "Moderately sensitive": 0.10,
                "Slightly sensitive": 0.02, "Not sensitive": -0.05}
    prob += sens_adj.get(sensitivity, 0)

    # Discount motivation
    if discount_mot in [">20%", "20%"]:
        prob += 0.10
    elif discount_mot == "15%":
        prob += 0.05

    # Channel — delivery users more app-ready
    if channel in ["Delivery App", "Restaurant App"]:
        prob += 0.08

    # Fairness perception
    fair_adj = {"Very fair": 0.15, "Somewhat fair": 0.08, "Neutral": 0.0,
                "Unfair": -0.10, "Very unfair": -0.18}
    prob += fair_adj.get(fairness, 0)

    # Off-peak willingness
    if offpeak in ["Definitely yes", "Probably yes"]:
        prob += 0.07

    # Rating — satisfied customers more open
    if rating >= 4:
        prob += 0.05
    elif rating <= 2:
        prob -= 0.08

    prob = np.clip(prob, 0.05, 0.95)
    return np.random.choice(["Yes", "No"], p=[prob, 1 - prob])


# =============================================================================
# MAIN DATA GENERATION LOOP
# =============================================================================

data = []

for i in range(n):

    # --- Demographics (correlated) ---
    age = np.random.choice(age_groups, p=age_base_prob)
    income = np.random.choice(income_groups, p=income_given_age[age])
    ctype = np.random.choice(customer_types, p=ctype_given_age[age])
    nation = np.random.choice(nationalities, p=nationality_prob)
    loyalty = np.random.choice(loyalty_options, p=loyalty_given_ctype[ctype])

    # --- Dining Behaviour (correlated) ---
    freq = np.random.choice(frequency_options, p=freq_given_income[income])
    time = np.random.choice(order_times, p=time_given_age[age])
    day = np.random.choice(day_options, p=day_prob)
    channel = np.random.choice(channels, p=channel_given_age[age])
    group = np.random.choice(group_sizes, p=group_given_ctype[ctype])
    dist_cat = np.random.choice(distances, p=distance_prob)
    cuisine = np.random.choice(cuisines, p=cuisine_given_nationality[nation])
    tier = np.random.choice(tiers, p=tier_given_income[income])
    location = np.random.choice(locations, p=location_given_income[income])

    # --- Price Sensitivity & Attitudes (correlated) ---
    sensitivity = np.random.choice(sensitivity_options, p=sensitivity_given_income[income])
    discount_mot = np.random.choice(discount_motivation_options, p=discount_given_sensitivity[sensitivity])

    # Off-peak willingness — correlated with sensitivity
    if sensitivity in ["Very sensitive", "Moderately sensitive"]:
        offpeak = np.random.choice(offpeak_options, p=[0.30, 0.30, 0.20, 0.12, 0.08])
    else:
        offpeak = np.random.choice(offpeak_options, p=[0.10, 0.15, 0.25, 0.25, 0.25])

    # Fairness — correlated with age (younger = more accepting)
    if age in ["18-24", "25-34"]:
        fairness = np.random.choice(fairness_options, p=[0.20, 0.30, 0.25, 0.15, 0.10])
    else:
        fairness = np.random.choice(fairness_options, p=[0.10, 0.20, 0.25, 0.25, 0.20])

    # Discount importance — correlated with sensitivity
    if sensitivity in ["Very sensitive", "Moderately sensitive"]:
        disc_imp = np.random.choice(discount_importance_options, p=[0.30, 0.30, 0.25, 0.10, 0.05])
    else:
        disc_imp = np.random.choice(discount_importance_options, p=[0.05, 0.10, 0.25, 0.30, 0.30])

    weather = np.random.choice(weather_options, p=weather_prob)
    peak_months = month_select_seasonal()
    rating = np.random.choice(rating_options, p=rating_prob)

    # --- Multi-selects ---
    challenges = multi_select(challenges_list, 1, 4)
    features = multi_select(features_list, 1, 4)

    # --- System-Generated Variables ---
    demand = derive_demand_level(day, time, peak_months)
    base_spend = derive_spend(income, tier, group)
    surge = derive_surge(demand, tier)
    final_spend = round(base_spend * surge, 2)
    occupancy = derive_occupancy(demand, time) if channel == "Dine-in" else np.nan
    discount_pct = round(max(0, (1 - surge) * 100), 1) if surge < 1.0 else 0.0
    del_distance = derive_delivery_distance(channel, dist_cat)
    del_time = derive_delivery_time(del_distance, channel)

    # --- Classification Target ---
    adoption = derive_adoption(sensitivity, discount_mot, channel, fairness, offpeak, rating)

    row = {
        "Age": age,
        "Monthly_Income": income,
        "Customer_Type": ctype,
        "Nationality_Cluster": nation,
        "Loyalty_Status": loyalty,
        "Dining_Frequency": freq,
        "Avg_Spend_AED": base_spend,
        "Order_Time": time,
        "Day_Preference": day,
        "Order_Channel": channel,
        "Group_Size": group,
        "Distance_Category": dist_cat,
        "Cuisine_Preference": cuisine,
        "Restaurant_Tier": tier,
        "Restaurant_Location": location,
        "Price_Sensitivity": sensitivity,
        "Offpeak_Willingness": offpeak,
        "Fairness_Perception": fairness,
        "Discount_Importance": disc_imp,
        "Discount_Motivation": discount_mot,
        "Weather_Behaviour": weather,
        "Peak_Months": ", ".join(peak_months),
        "Experience_Rating": rating,
        "Challenges": ", ".join(challenges),
        "Desired_Features": ", ".join(features),
        # System-generated
        "Demand_Level": demand,
        "Surge_Multiplier": surge,
        "Table_Occupancy_Pct": occupancy,
        "Base_Order_Value": base_spend,
        "Final_Order_Value": final_spend,
        "Discount_Percentage": discount_pct,
        "Delivery_Distance_km": del_distance,
        "Est_Delivery_Time_min": del_time,
        "Customer_Rating": rating,
        "App_Adoption": adoption,
    }

    data.append(row)

df = pd.DataFrame(data)

# =============================================================================
# INJECT DIRTY DATA, OUTLIERS, NOISE
# =============================================================================

print(f"Clean rows: {len(df)}")

# --- 1. Duplicate rows (~2%) ---
dup_idx = np.random.choice(df.index, size=int(n * 0.02), replace=False)
duplicates = df.loc[dup_idx].copy()
df = pd.concat([df, duplicates], ignore_index=True)
print(f"After duplicates: {len(df)}")

# --- 2. Null values (~5% scattered) ---
null_cols = ["Monthly_Income", "Dining_Frequency", "Cuisine_Preference",
             "Restaurant_Tier", "Price_Sensitivity", "Weather_Behaviour",
             "Experience_Rating", "Loyalty_Status", "Fairness_Perception"]

for col in null_cols:
    null_idx = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
    df.loc[null_idx, col] = np.nan

# Sprinkle nulls in numeric columns too
for col in ["Avg_Spend_AED", "Surge_Multiplier", "Final_Order_Value"]:
    null_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
    df.loc[null_idx, col] = np.nan

print(f"Nulls injected across {len(null_cols) + 3} columns")

# --- 3. Typos in categorical columns (~3%) ---
typo_map = {
    "Customer_Type": {"Professional": "Profesional", "Student": "Studnet", "Tourist": "Touri st"},
    "Order_Channel": {"Dine-in": "dine-in", "Delivery App": "DELIVERY APP", "Takeaway": "Take away"},
    "Cuisine_Preference": {"Arabic": "Arebic", "Indian/Pakistani": "indian/pakistani", "Western": "WESTERN"},
    "Day_Preference": {"Weekends": "Weekend", "Weekdays": "weekdays"},
    "Restaurant_Tier": {"Budget/Casual": "budget/casual", "Premium/Fine Dining": "Premium / Fine dining"},
    "Nationality_Cluster": {"South Asian": "south asian", "Western Expat": "western expat"},
}

for col, typos in typo_map.items():
    for original, typo in typos.items():
        mask = df[col] == original
        typo_idx = np.random.choice(df[mask].index, size=max(1, int(mask.sum() * 0.03)), replace=False)
        df.loc[typo_idx, col] = typo

print("Typos injected")

# --- 4. Outliers in numeric columns ---
# Extreme spend values
outlier_idx = np.random.choice(df.index, size=25, replace=False)
df.loc[outlier_idx[:10], "Avg_Spend_AED"] = np.random.choice([5, 8, 12, 950, 1100, 1500], size=10)
df.loc[outlier_idx[:10], "Base_Order_Value"] = df.loc[outlier_idx[:10], "Avg_Spend_AED"]
df.loc[outlier_idx[:10], "Final_Order_Value"] = df.loc[outlier_idx[:10], "Avg_Spend_AED"]

# Extreme delivery distances
outlier_del = df[df["Delivery_Distance_km"].notna()].index
if len(outlier_del) > 10:
    extreme_del_idx = np.random.choice(outlier_del, size=8, replace=False)
    df.loc[extreme_del_idx, "Delivery_Distance_km"] = np.random.choice([0.2, 0.5, 38, 42, 55], size=8)

# Surge outliers
surge_outlier_idx = np.random.choice(df[df["Surge_Multiplier"].notna()].index, size=10, replace=False)
df.loc[surge_outlier_idx, "Surge_Multiplier"] = np.random.choice([0.50, 0.55, 1.65, 1.80, 2.0], size=10)

# Occupancy outliers (negative or >100 before cleaning)
occ_valid = df[df["Table_Occupancy_Pct"].notna()].index
if len(occ_valid) > 5:
    occ_outlier_idx = np.random.choice(occ_valid, size=5, replace=False)
    df.loc[occ_outlier_idx, "Table_Occupancy_Pct"] = np.random.choice([-5, 0, 105, 110, 120], size=5)

print("Outliers injected")

# --- 5. Logical noise / contradictions (~2%) ---
# "Not sensitive" but wants >20% discount
noise_idx = df[df["Price_Sensitivity"] == "Not sensitive"].index
if len(noise_idx) > 5:
    noise_sel = np.random.choice(noise_idx, size=min(15, len(noise_idx)), replace=False)
    df.loc[noise_sel, "Discount_Motivation"] = ">20%"

# High rating but adoption = No
high_rate_idx = df[df["Experience_Rating"] == 5].index
if len(high_rate_idx) > 5:
    flip_idx = np.random.choice(high_rate_idx, size=min(10, len(high_rate_idx)), replace=False)
    df.loc[flip_idx, "App_Adoption"] = "No"

# Low rating but adoption = Yes
low_rate_idx = df[df["Experience_Rating"] == 1].index
if len(low_rate_idx) > 2:
    flip_idx2 = np.random.choice(low_rate_idx, size=min(5, len(low_rate_idx)), replace=False)
    df.loc[flip_idx2, "App_Adoption"] = "Yes"

print("Noise injected")

# --- 6. Shuffle row order ---
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# =============================================================================
# SUMMARY
# =============================================================================

print(f"\n{'='*50}")
print(f"FINAL DATASET SUMMARY")
print(f"{'='*50}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Null values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"\nColumn list:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col} ({df[col].dtype})")

print(f"\nApp_Adoption distribution:\n{df['App_Adoption'].value_counts()}")
print(f"\nSample rows:")
print(df.head(3).to_string())

# Save
df.to_csv("dubai_dynamic_pricing_survey_RAW.csv", index=False)
print(f"\nSaved to: dubai_dynamic_pricing_survey_RAW.csv")
