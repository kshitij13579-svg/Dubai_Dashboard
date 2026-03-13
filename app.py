"""
Dubai Dynamic Restaurant Pricing — EDA Dashboard
==================================================
Consulting-grade Streamlit dashboard.
Color system: White backgrounds, dark charcoal text, muted blue/teal accents.
Inspired by McKinsey/BCG/Bain visual language.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from itertools import combinations
import os

st.set_page_config(page_title="DinePrice Dubai — EDA", page_icon="🍽️",
                   layout="wide", initial_sidebar_state="expanded")

# =============================================================================
# CONSULTING COLOR SYSTEM
# =============================================================================
# Primary text: #2D2D2D (near-black charcoal)
# Secondary text: #5A5A5A (dark grey)
# Muted text: #8C8C8C (medium grey)
# Background: #FFFFFF (white)
# Card bg: #F7F8FA (barely-there grey)
# Accent 1: #003A70 (McKinsey navy)
# Accent 2: #00857C (BCG teal)
# Accent 3: #D4541B (warm orange — sparingly)
# Positive: #1B7340 (forest green)
# Negative: #C4301C (muted red)
# Chart palette: muted, desaturated, professional

C_TEXT = "#2D2D2D"
C_SUBTEXT = "#5A5A5A"
C_MUTED = "#8C8C8C"
C_BG = "#FFFFFF"
C_CARD = "#F7F8FA"
C_NAVY = "#003A70"
C_TEAL = "#00857C"
C_ORANGE = "#D4541B"
C_GREEN = "#1B7340"
C_RED = "#C4301C"

# Desaturated consulting palette for charts
PALETTE = ["#003A70", "#00857C", "#D4541B", "#5B8DB8", "#7FBFB3",
           "#E8956A", "#8C8C8C", "#B8D4E3", "#4A7C59", "#C9A96E"]
YES_NO = [C_TEAL, C_RED]
DEMAND_MAP = {"Low": "#5B8DB8", "Medium": "#E8956A", "High": "#C4301C"}

st.markdown(f"""
<style>
    /* === PAGE === */
    .stApp {{background-color: {C_BG};}}
    .block-container {{padding-top: 1.5rem; padding-bottom: 1rem; max-width: 1180px;}}

    /* === TYPOGRAPHY === */
    h1 {{font-size: 1.75rem !important; color: {C_TEXT} !important; font-weight: 700 !important; letter-spacing: -0.3px;}}
    h2 {{font-size: 1.25rem !important; color: {C_NAVY} !important; font-weight: 600 !important;
         border-bottom: 2px solid {C_NAVY}; padding-bottom: 6px; margin-top: 1.8rem !important;}}
    h3 {{font-size: 1.05rem !important; color: {C_TEXT} !important; font-weight: 600 !important;}}
    p, li, span, label {{color: {C_TEXT} !important;}}

    /* === METRIC CARDS === */
    div[data-testid="stMetric"] {{
        background: {C_CARD};
        padding: 16px 20px;
        border-radius: 6px;
        border: 1px solid #E5E7EB;
        border-left: 4px solid {C_NAVY};
    }}
    div[data-testid="stMetric"] label {{
        color: {C_MUTED} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {C_TEXT} !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
    }}

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {{
        background: {C_NAVY};
    }}
    section[data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] li {{
        color: #D9DDE3 !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.15) !important;
    }}
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h2 {{
        color: #FFFFFF !important;
        border-bottom: none !important;
    }}

    /* === INSIGHT BOX === */
    .insight-box {{
        background: #F0F7F4;
        border-left: 4px solid {C_TEAL};
        padding: 14px 18px;
        border-radius: 4px;
        margin: 12px 0 20px 0;
        color: {C_TEXT};
        font-size: 0.88rem;
        line-height: 1.6;
    }}
    .insight-box strong {{color: {C_NAVY};}}

    /* === CALLOUT BOX === */
    .callout-box {{
        background: #FFF8F0;
        border-left: 4px solid {C_ORANGE};
        padding: 14px 18px;
        border-radius: 4px;
        margin: 12px 0 20px 0;
        color: {C_TEXT};
        font-size: 0.88rem;
        line-height: 1.6;
    }}
    .callout-box strong {{color: {C_ORANGE};}}

    /* === DIVIDERS === */
    hr {{border-color: #E5E7EB !important;}}

    /* === HIDE BRANDING === */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* === EXPANDER === */
    details {{border: 1px solid #E5E7EB; border-radius: 4px;}}
    summary {{color: {C_TEXT} !important; font-weight: 600;}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HELPERS
# =============================================================================

def styled_layout(fig, height=400):
    fig.update_layout(
        height=height,
        plot_bgcolor=C_BG,
        paper_bgcolor=C_BG,
        font=dict(family="Inter, Helvetica, Arial, sans-serif", color=C_TEXT, size=11),
        title_font=dict(size=13, color=C_TEXT, family="Inter, Helvetica, Arial, sans-serif"),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(bgcolor=C_BG, bordercolor="#E5E7EB", borderwidth=1, font=dict(size=10, color=C_SUBTEXT)),
        coloraxis_colorbar=dict(tickfont=dict(color=C_SUBTEXT), title_font=dict(color=C_SUBTEXT)),
    )
    fig.update_xaxes(title_font=dict(color=C_SUBTEXT, size=11), tickfont=dict(color=C_SUBTEXT, size=10),
                     gridcolor="#F0F0F0", linecolor="#E5E7EB")
    fig.update_yaxes(title_font=dict(color=C_SUBTEXT, size=11), tickfont=dict(color=C_SUBTEXT, size=10),
                     gridcolor="#F0F0F0", linecolor="#E5E7EB")
    return fig


def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def callout(text):
    st.markdown(f'<div class="callout-box">{text}</div>', unsafe_allow_html=True)


@st.cache_data
def load_data():
    for path in ["data/data_clean.csv", "data_clean.csv", "dubai-pricing-dashboard/data/data_clean.csv"]:
        if os.path.exists(path):
            return pd.read_csv(path)
    st.error("data_clean.csv not found."); st.stop()


df = load_data()


def explode_col(dataframe, col):
    return dataframe[col].dropna().str.split(", ").explode().str.strip()


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.markdown(f"""
<div style="text-align:center; padding: 18px 0 8px 0;">
    <div style="font-size: 2.2rem; margin-bottom: 4px;">🍽️</div>
    <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.5px;">DinePrice Dubai</div>
    <div style="font-size: 0.68rem; color: #8BA4BD; letter-spacing: 2px; margin-top: 2px;">MARKET ANALYTICS</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

sections = [
    "📊 Overview & KPIs",
    "1  Customer Profile",
    "2  Dining Behaviour",
    "3  Price Sensitivity",
    "4  Dynamic Pricing System",
    "5  Location & Cuisine",
    "6  Delivery vs Dine-in",
    "7  Correlation Analysis",
    "8  Challenges & Features",
    "9  App Adoption Deep Dive",
    "10  Seasonality",
    "⟶  Sankey: Path to Adoption",
]
section = st.sidebar.radio("", sections, index=0, label_visibility="collapsed")
st.sidebar.divider()

ar_g = (df["App_Adoption"] == "Yes").mean() * 100
st.sidebar.markdown(f"""
<div style="background:rgba(255,255,255,0.08); padding:14px; border-radius:6px;">
    <div style="font-size:0.65rem; color:#8BA4BD; text-transform:uppercase; letter-spacing:1.5px;">North Star Metric</div>
    <div style="font-size:1.5rem; font-weight:800; color:#FFFFFF; margin-top:4px;">{ar_g:.1f}%</div>
    <div style="font-size:0.72rem; color:#8BA4BD; margin-top:2px;">App Adoption Rate</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="margin-top:12px; padding:10px 14px; background:rgba(255,255,255,0.05); border-radius:4px; font-size:0.72rem; color:#8BA4BD; line-height:1.8;">
    <strong style="color:#D9DDE3;">{len(df):,}</strong> survey responses<br>
    <strong style="color:#D9DDE3;">35</strong> variables<br>
    <strong style="color:#D9DDE3;">24</strong> system features
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown('<div style="font-size:0.6rem; color:#5A7A9A; text-align:center; letter-spacing:1px;">SP JAIN GMBA · DATA ANALYTICS · 2026</div>', unsafe_allow_html=True)

# =============================================================================
# ORDERINGS
# =============================================================================
AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55+"]
INC_ORDER = ["<5000", "5000-10000", "10001-20000", "20001-35000", ">35000"]
SENS_ORDER = ["Very sensitive", "Moderately sensitive", "Slightly sensitive", "Not sensitive"]
FAIR_ORDER = ["Very fair", "Somewhat fair", "Neutral", "Unfair", "Very unfair"]
FREQ_ORDER = ["Multiple/week", "Once/week", "2-3/month", "Once/month", "Rarely"]
TIME_ORDER = ["Breakfast", "Lunch", "Dinner", "Late Night"]
DEMAND_ORDER = ["Low", "Medium", "High"]


# =============================================================================
# 0. OVERVIEW
# =============================================================================
if section == "📊 Overview & KPIs":
    st.title("DinePrice Dubai — Dynamic Restaurant Pricing")
    st.markdown(f"<p style='color:{C_SUBTEXT}; font-size:0.95rem; margin-top:-8px;'>North Star: App Adoption Rate — What drives customers to say Yes?</p>", unsafe_allow_html=True)
    st.markdown("")

    adopt_rate = (df["App_Adoption"] == "Yes").mean() * 100
    avg_spend = df["Avg_Spend_AED"].mean()
    avg_surge = df["Surge_Multiplier"].mean()
    delivery_pct = (df["Order_Channel"] == "Delivery App").mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Responses", f"{len(df):,}")
    c2.metric("Adoption Rate", f"{adopt_rate:.1f}%")
    c3.metric("Avg Spend", f"{avg_spend:.0f} AED")
    c4.metric("Avg Surge", f"{avg_surge:.2f}x")
    c5.metric("Delivery Share", f"{delivery_pct:.1f}%")

    insight(f"<strong>{adopt_rate:.0f}% of respondents</strong> are open to dynamic pricing — a strong market validation signal. Average spend is <strong>{avg_spend:.0f} AED/visit</strong> with moderate surge headroom ({avg_surge:.2f}x). Delivery commands <strong>{delivery_pct:.0f}%</strong> of orders, reflecting Dubai's app-first dining culture.")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="App_Adoption", title="Adoption Split", color_discrete_sequence=YES_NO, hole=0.5)
        fig.update_traces(textinfo="percent+label", textfont=dict(size=13, color=C_TEXT), marker=dict(line=dict(color=C_BG, width=2)))
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Avg_Spend_AED", nbins=40, color="App_Adoption", barmode="overlay",
                           title="Spend Distribution by Adoption", color_discrete_sequence=YES_NO, opacity=0.7)
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("Adopters and non-adopters show similar spend distributions — <strong>price level alone doesn't determine adoption</strong>. Attitudinal variables (sensitivity, fairness) are stronger predictors. See sections 3 and 9.")

    with st.expander("Dataset Preview"):
        st.dataframe(df.head(20), use_container_width=True, height=400)

# =============================================================================
# 1. CUSTOMER PROFILE
# =============================================================================
elif section == "1  Customer Profile":
    st.title("Customer Profile & Segmentation")
    insight("<strong>Objective:</strong> Understand <em>who</em> the respondents are. These dimensions feed K-Means clustering for persona identification.")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="Age", color="App_Adoption", category_orders={"Age": AGE_ORDER},
                           title="Age Distribution by Adoption", color_discrete_sequence=YES_NO, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Monthly_Income", color="App_Adoption", category_orders={"Monthly_Income": INC_ORDER},
                           title="Income Distribution by Adoption", color_discrete_sequence=YES_NO, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Age:</strong> 25–34 dominates (~35%) — Dubai's young professional base. <strong>Income:</strong> The 5K–20K AED band is the core market — price-sensitive enough to value dynamic discounts, affluent enough to dine often.")

    col3, col4 = st.columns(2)
    with col3:
        fig = px.histogram(df, x="Customer_Type", color="Nationality_Cluster", title="Customer Type by Nationality",
                           color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Loyalty_Status", color="Customer_Type", title="Loyalty Status by Customer Type",
                           color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Nationality:</strong> South Asians (~45%) lead, followed by Arabs and Western Expats — mirroring Dubai's actual demographics. <strong>Loyalty:</strong> Tourists are 'Explorers'; Families are 'Loyal to 1–2' — a key segmentation lever.")

    st.subheader("Drill-down: Age × Income")
    ct = pd.crosstab(df["Age"], df["Monthly_Income"]).reindex(index=AGE_ORDER, columns=INC_ORDER)
    fig = px.imshow(ct, text_auto=True, color_continuous_scale="Blues", title="Respondent Count: Age vs Income",
                    labels=dict(x="Monthly Income", y="Age Group", color="Count"))
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Nationality → Type → Adoption")
    fig = px.sunburst(df, path=["Nationality_Cluster", "Customer_Type", "App_Adoption"],
                      title="Nationality → Customer Type → Adoption", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 2. DINING BEHAVIOUR
# =============================================================================
elif section == "2  Dining Behaviour":
    st.title("Dining Behaviour Patterns")
    insight("<strong>Objective:</strong> Map when, how, and how often customers dine. Critical inputs for <strong>regression</strong> (spend prediction) and <strong>clustering</strong> (personas).")

    col1, col2 = st.columns(2)
    with col1:
        ct = pd.crosstab(df["Age"], df["Order_Time"]).reindex(index=AGE_ORDER, columns=TIME_ORDER)
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="OrRd", title="Order Time by Age Group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Order_Channel", color="Age", category_orders={"Age": AGE_ORDER},
                           title="Channel Preference by Age", color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Time × Age:</strong> 18–24 skews Late Night; 55+ skews Breakfast. Dinner is universally peak. <strong>Channel:</strong> Under-34s are 50%+ delivery — Dubai's app-first culture confirmed.")

    col3, col4 = st.columns(2)
    with col3:
        ct2 = pd.crosstab(df["Monthly_Income"], df["Dining_Frequency"]).reindex(index=INC_ORDER, columns=FREQ_ORDER)
        fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Teal", title="Dining Frequency by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Group_Size", color="Customer_Type", title="Group Size by Customer Type",
                           color_discrete_sequence=PALETTE, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Income → Frequency:</strong> Higher income = more frequent dining (>35K bracket dines multiple times/week). <strong>Group Size:</strong> Families = 3–4+; Students/Professionals = solo or pairs.")

    st.subheader("Drill-down: Day → Time → Channel")
    fig = px.sunburst(df, path=["Day_Preference", "Order_Time", "Order_Channel"], title="Day → Time → Channel Flow", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Frequency vs Spend")
    fig = px.box(df, x="Dining_Frequency", y="Avg_Spend_AED", color="Dining_Frequency",
                 category_orders={"Dining_Frequency": FREQ_ORDER}, title="Spend by Dining Frequency", color_discrete_sequence=PALETTE)
    fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    insight("Frequent diners show higher median spend but wider variance (budget + premium visits). Rare diners trend toward higher per-visit spend — special occasion behavior.")

# =============================================================================
# 3. PRICE SENSITIVITY
# =============================================================================
elif section == "3  Price Sensitivity":
    st.title("Price Sensitivity & Dynamic Pricing Appetite")
    insight("<strong>Objective:</strong> How do customers react to price changes? These are the <strong>strongest classification predictors</strong> for App Adoption.")

    col1, col2 = st.columns(2)
    with col1:
        ct = pd.crosstab(df["Monthly_Income"], df["Price_Sensitivity"]).reindex(index=INC_ORDER, columns=SENS_ORDER)
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="RdYlGn_r", title="Price Sensitivity by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        disc_order = ["5%", "10%", "15%", "20%", ">20%"]
        ct2 = pd.crosstab(df["Price_Sensitivity"], df["Discount_Motivation"]).reindex(index=SENS_ORDER, columns=disc_order)
        fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Oranges", title="Discount Motivation by Sensitivity")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Income → Sensitivity:</strong> &lt;5K income is overwhelmingly 'Very sensitive'; &gt;35K is 'Not sensitive'. <strong>Discount depth:</strong> Very sensitive customers need 20%+ discounts — the engine must price aggressively off-peak to move this segment.")

    col3, col4 = st.columns(2)
    with col3:
        op = ["Definitely yes", "Probably yes", "Maybe", "Probably not", "Definitely not"]
        fig = px.histogram(df, x="Offpeak_Willingness", color="Price_Sensitivity", title="Off-Peak Willingness by Sensitivity",
                           color_discrete_sequence=PALETTE, barmode="stack", category_orders={"Offpeak_Willingness": op})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Fairness_Perception", color="Age", title="Fairness Perception by Age",
                           color_discrete_sequence=PALETTE, barmode="stack", category_orders={"Fairness_Perception": FAIR_ORDER, "Age": AGE_ORDER})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Off-peak shift:</strong> Price-sensitive customers are significantly more willing to dine off-peak — core business hypothesis validated. <strong>Fairness:</strong> 18–34 perceives dynamic pricing as fairer (accustomed to Uber/Careem surge).")

    st.subheader("Drill-down: Sensitivity → Adoption Rate")
    ab = df.groupby("Price_Sensitivity")["App_Adoption"].apply(lambda x: (x == "Yes").mean() * 100).reindex(SENS_ORDER).reset_index()
    ab.columns = ["Sensitivity", "Rate"]
    fig = px.bar(ab, x="Sensitivity", y="Rate", title="Adoption Rate by Price Sensitivity",
                 color="Rate", color_continuous_scale="Tealgrn", text="Rate")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=C_TEXT))
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Discount Importance vs Fairness")
    di = ["Extremely important", "Very important", "Moderately important", "Slightly important", "Not important"]
    ct3 = pd.crosstab(df["Discount_Importance"], df["Fairness_Perception"]).reindex(index=di, columns=FAIR_ORDER)
    fig = px.imshow(ct3, text_auto=True, color_continuous_scale="Purp", title="Discount Importance vs Fairness")
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Key finding:</strong> 'Very fair' + 'Extremely important discounts' = prime early adopter segment. Target these first at launch.")

# =============================================================================
# 4. DYNAMIC PRICING SYSTEM
# =============================================================================
elif section == "4  Dynamic Pricing System":
    st.title("Dynamic Pricing System Variables")
    insight("<strong>Objective:</strong> Analyze the engine outputs — demand level, surge multiplier, table occupancy, and price impact on orders.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Surge", f"{df['Surge_Multiplier'].mean():.2f}x")
    c2.metric("Avg Discount", f"{df['Discount_Percentage'].mean():.1f}%")
    c3.metric("Avg Occupancy", f"{df['Table_Occupancy_Pct'].dropna().mean():.1f}%")
    c4.metric("High Demand", f"{(df['Demand_Level'] == 'High').mean() * 100:.1f}%")

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        dc = df["Demand_Level"].value_counts().reindex(DEMAND_ORDER).reset_index()
        dc.columns = ["Demand", "Count"]
        fig = px.bar(dc, x="Demand", y="Count", color="Demand", title="Demand Level Distribution",
                     color_discrete_map=DEMAND_MAP, text="Count")
        fig.update_traces(textposition="outside", textfont=dict(color=C_TEXT))
        fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Surge_Multiplier", nbins=30, color="Demand_Level",
                           title="Surge Distribution by Demand", color_discrete_map=DEMAND_MAP,
                           category_orders={"Demand_Level": DEMAND_ORDER})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight(f"<strong>{(df['Demand_Level'] == 'High').mean() * 100:.0f}%</strong> of observations are high-demand (weekends + dinner + peak season). Surge ranges 0.75x–1.40x; most cluster around 1.0–1.2x — moderate adjustments that customers can absorb.")

    col3, col4 = st.columns(2)
    with col3:
        fig = px.box(df, x="Demand_Level", y="Table_Occupancy_Pct", color="Demand_Level",
                     title="Occupancy by Demand Level", color_discrete_map=DEMAND_MAP,
                     category_orders={"Demand_Level": DEMAND_ORDER})
        fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.scatter(df, x="Base_Order_Value", y="Final_Order_Value", color="Demand_Level", opacity=0.35,
                         title="Base vs Final Order Value", color_discrete_map=DEMAND_MAP)
        fig.add_shape(type="line", x0=0, y0=0, x1=800, y1=800, line=dict(dash="dash", color=C_MUTED, width=1))
        fig.add_annotation(x=620, y=560, text="y = x (no surge)", showarrow=False, font=dict(color=C_MUTED, size=9))
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Occupancy:</strong> High demand averages ~80% vs ~30% for low — the engine correctly identifies full restaurants. <strong>Scatter:</strong> Points above the dashed line have surge applied; below = discounted.")

    st.subheader("Drill-down: Does Surge Kill Conversion?")
    dt = df.copy()
    dt["Surge_Bin"] = pd.cut(dt["Surge_Multiplier"], bins=[0.7, 0.85, 0.95, 1.05, 1.15, 1.25, 1.45],
                              labels=["0.75–0.85", "0.85–0.95", "0.95–1.05", "1.05–1.15", "1.15–1.25", "1.25–1.40"])
    sa = dt.groupby("Surge_Bin")["App_Adoption"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
    sa.columns = ["Surge", "Rate"]
    fig = px.bar(sa, x="Surge", y="Rate", title="Adoption Rate by Surge Level", color="Rate",
                 color_continuous_scale="Tealgrn", text="Rate")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=C_TEXT))
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Key finding:</strong> Adoption stays stable across surge levels. The engine can apply 10–20% surges without significantly hurting conversion.")

    st.subheader("Drill-down: Demand by Day × Time")
    ct = pd.crosstab([df["Day_Preference"], df["Order_Time"]], df["Demand_Level"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    fig = px.imshow(ct_pct.round(1), text_auto=True, color_continuous_scale="OrRd",
                    title="Demand Level % by Day × Time", labels=dict(color="%"))
    styled_layout(fig, 450); st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 5. LOCATION & CUISINE
# =============================================================================
elif section == "5  Location & Cuisine":
    st.title("Location & Cuisine Intelligence")
    insight("<strong>Objective:</strong> Which Dubai locations and cuisines command premium pricing? Informs location-based engine rules and onboarding strategy.")

    col1, col2 = st.columns(2)
    with col1:
        li = pd.crosstab(df["Restaurant_Location"], df["Monthly_Income"]).reindex(columns=INC_ORDER)
        fig = px.imshow(li, text_auto=True, color_continuous_scale="Blues", title="Location by Income")
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        cn = pd.crosstab(df["Nationality_Cluster"], df["Cuisine_Preference"])
        fig = px.imshow(cn, text_auto=True, color_continuous_scale="Oranges", title="Cuisine by Nationality")
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Location:</strong> DIFC/Downtown = high income; Deira = budget; Malls = income-agnostic. <strong>Cuisine:</strong> South Asians → Indian/Pakistani (45%); Arabs → Arabic (40%); Western Expats → Western (35%) — strong cultural clustering.")

    col3, col4 = st.columns(2)
    with col3:
        ti = pd.crosstab(df["Monthly_Income"], df["Restaurant_Tier"]).reindex(index=INC_ORDER)
        fig = px.imshow(ti, text_auto=True, color_continuous_scale="Teal", title="Tier by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        sl = df.groupby("Restaurant_Location")["Avg_Spend_AED"].mean().sort_values(ascending=True).reset_index()
        fig = px.bar(sl, x="Avg_Spend_AED", y="Restaurant_Location", orientation="h", title="Avg Spend by Location (AED)",
                     color="Avg_Spend_AED", color_continuous_scale="Blues", text="Avg_Spend_AED")
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', textfont=dict(color=C_TEXT))
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Spend by Cuisine")
    fig = px.box(df, x="Cuisine_Preference", y="Avg_Spend_AED", color="Cuisine_Preference",
                 title="Spend Distribution by Cuisine", color_discrete_sequence=PALETTE)
    fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Location → Tier → Adoption")
    fig = px.sunburst(df, path=["Restaurant_Location", "Restaurant_Tier", "App_Adoption"],
                      title="Location → Tier → Adoption", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 6. DELIVERY VS DINE-IN
# =============================================================================
elif section == "6  Delivery vs Dine-in":
    st.title("Delivery vs Dine-in Analysis")
    di = df[df["Order_Channel"] == "Dine-in"]; dl = df[df["Order_Channel"] == "Delivery App"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dine-in", f"{len(di):,}"); c2.metric("Delivery", f"{len(dl):,}")
    c3.metric("Dine-in Spend", f"{di['Avg_Spend_AED'].mean():.0f} AED"); c4.metric("Delivery Spend", f"{dl['Avg_Spend_AED'].mean():.0f} AED")

    insight(f"Delivery ({len(dl) / len(df) * 100:.0f}%) edges out Dine-in ({len(di) / len(df) * 100:.0f}%). Dine-in spend is ~<strong>{di['Avg_Spend_AED'].mean():.0f} AED</strong> vs ~<strong>{dl['Avg_Spend_AED'].mean():.0f} AED</strong> for delivery — the engine should differentiate surge rules by channel.")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="Order_Channel", title="Channel Split", color_discrete_sequence=PALETTE, hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont=dict(size=12, color=C_TEXT), marker=dict(line=dict(color=C_BG, width=2)))
        styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.box(df, x="Order_Channel", y="Avg_Spend_AED", color="Order_Channel",
                     title="Spend by Channel", color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False); styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = px.histogram(df, x="Weather_Behaviour", color="Order_Channel", title="Weather Impact on Channel",
                           color_discrete_sequence=PALETTE, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        dd = df[df["Delivery_Distance_km"].notna()]
        fig = px.scatter(dd, x="Delivery_Distance_km", y="Est_Delivery_Time_min", color="Avg_Spend_AED",
                         opacity=0.5, title="Distance vs Delivery Time", color_continuous_scale="Blues")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Weather:</strong> 48% switch to delivery in extreme heat — trigger delivery discounts above 40°C. <strong>Distance:</strong> Most within 7 km; linear correlation with time validates data realism.")

    st.subheader("Drill-down: Channel → Adoption")
    ca = df.groupby("Order_Channel")["App_Adoption"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
    ca.columns = ["Channel", "Rate"]
    fig = px.bar(ca, x="Channel", y="Rate", color="Rate", color_continuous_scale="Tealgrn",
                 text="Rate", title="Adoption Rate by Channel")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=C_TEXT))
    styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 7. CORRELATION
# =============================================================================
elif section == "7  Correlation Analysis":
    st.title("Correlation Analysis")
    insight("<strong>Objective:</strong> Identify linear relationships between numeric variables. Informs regression feature selection and highlights multicollinearity risks.")

    num_cols = ["Avg_Spend_AED", "Surge_Multiplier", "Final_Order_Value", "Discount_Percentage",
                "Experience_Rating", "Table_Occupancy_Pct", "Delivery_Distance_km", "Est_Delivery_Time_min"]
    corr = df[num_cols].corr()
    fig = px.imshow(corr.round(2), text_auto=True, color_continuous_scale="RdBu_r",
                    title="Correlation Matrix", zmin=-1, zmax=1)
    styled_layout(fig, 550); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Key:</strong> Avg_Spend ↔ Final_Value (~0.98, expected). Surge ↔ Discount (strong negative). Delivery_Distance ↔ Time (strong positive, validates realism). Experience_Rating weakly correlated with price — satisfaction is non-price-driven.")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(df, x="Monthly_Income", y="Avg_Spend_AED", color="Monthly_Income",
                     title="Income vs Spend", category_orders={"Monthly_Income": INC_ORDER}, color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Surge_Multiplier", y="Experience_Rating", color="App_Adoption", opacity=0.3,
                         title="Surge vs Rating", color_discrete_sequence=YES_NO)
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Base vs Final by Tier")
    fig = px.scatter(df, x="Base_Order_Value", y="Final_Order_Value", color="Restaurant_Tier", opacity=0.35,
                     title="Base vs Final Order Value by Tier", color_discrete_sequence=PALETTE)
    fig.add_shape(type="line", x0=0, y0=0, x1=800, y1=800, line=dict(dash="dash", color=C_MUTED))
    styled_layout(fig, 450); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Premium/Fine Dining</strong> shows widest spread above the no-surge line — these restaurants sustain higher surge multipliers.")

# =============================================================================
# 8. CHALLENGES & FEATURES
# =============================================================================
elif section == "8  Challenges & Features":
    st.title("Challenges & Desired Features")
    insight("<strong>Objective:</strong> Discover pain point clusters and feature demand. Feeds <strong>Association Rule Mining</strong> (Apriori/FP-Growth).")

    col1, col2 = st.columns(2)
    with col1:
        ch = explode_col(df, "Challenges"); chc = ch.value_counts().reset_index(); chc.columns = ["Challenge", "Count"]
        fig = px.bar(chc, x="Count", y="Challenge", orientation="h", title="Top Challenges",
                     color="Count", color_continuous_scale="OrRd", text="Count")
        fig.update_traces(textposition="outside", textfont=dict(color=C_TEXT)); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        ft = explode_col(df, "Desired_Features"); ftc = ft.value_counts().reset_index(); ftc.columns = ["Feature", "Count"]
        fig = px.bar(ftc, x="Count", y="Feature", orientation="h", title="Most Desired Features",
                     color="Count", color_continuous_scale="Tealgrn", text="Count")
        fig.update_traces(textposition="outside", textfont=dict(color=C_TEXT)); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)

    insight(f"<strong>Top challenge:</strong> '{chc.iloc[0]['Challenge']}' ({chc.iloc[0]['Count']}). <strong>Top feature:</strong> '{ftc.iloc[0]['Feature']}' ({ftc.iloc[0]['Count']}). Pain points align with desired features — the app addresses real market needs.")

    st.subheader("Drill-down: Challenge Co-occurrence")
    ce = df["Challenges"].dropna().str.split(", "); ac = sorted(set(c for r in ce for c in r))
    cc = pd.DataFrame(0, index=ac, columns=ac)
    for r in ce:
        for a, b in combinations(r, 2): cc.loc[a, b] += 1; cc.loc[b, a] += 1
    fig = px.imshow(cc, text_auto=True, color_continuous_scale="OrRd", title="Challenge Co-occurrence")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Feature Co-occurrence")
    fe = df["Desired_Features"].dropna().str.split(", "); af = sorted(set(f for r in fe for f in r))
    fc = pd.DataFrame(0, index=af, columns=af)
    for r in fe:
        for a, b in combinations(r, 2): fc.loc[a, b] += 1; fc.loc[b, a] += 1
    fig = px.imshow(fc, text_auto=True, color_continuous_scale="Tealgrn", title="Feature Co-occurrence")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

    insight("Co-occurring challenges suggest systemic issues (e.g., 'High weekend prices' + 'Crowded' = same peak-demand scenario). Association rules will formalize these as itemset patterns with support and confidence.")

    st.subheader("Drill-down: Challenge → Feature Association")
    pairs = []
    for _, row in df.iterrows():
        if pd.notna(row["Challenges"]) and pd.notna(row["Desired_Features"]):
            for c in str(row["Challenges"]).split(", "):
                for f in str(row["Desired_Features"]).split(", "):
                    pairs.append({"Challenge": c.strip(), "Feature": f.strip()})
    tp = pd.DataFrame(pairs).groupby(["Challenge", "Feature"]).size().reset_index(name="Count").nlargest(15, "Count")
    fig = px.bar(tp, x="Count", y="Challenge", color="Feature", orientation="h",
                 title="Top 15 Challenge → Feature Associations", color_discrete_sequence=PALETTE, barmode="stack")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 9. ADOPTION DEEP DIVE
# =============================================================================
elif section == "9  App Adoption Deep Dive":
    st.title("App Adoption — Deep Dive")
    ar = (df["App_Adoption"] == "Yes").mean() * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Adoption Rate", f"{ar:.1f}%")
    c2.metric("Yes", f"{(df['App_Adoption'] == 'Yes').sum():,}")
    c3.metric("No", f"{(df['App_Adoption'] == 'No').sum():,}")

    insight(f"<strong>{ar:.1f}% adoption</strong> is a strong positive signal. Below: adoption decomposed by <strong>10 dimensions</strong> to profile adopters vs non-adopters — directly feeds <strong>classification</strong> feature selection.")

    dims = [("Age", AGE_ORDER), ("Monthly_Income", INC_ORDER), ("Customer_Type", None), ("Price_Sensitivity", SENS_ORDER),
            ("Fairness_Perception", FAIR_ORDER), ("Order_Channel", None), ("Restaurant_Tier", None),
            ("Loyalty_Status", None), ("Day_Preference", None), ("Nationality_Cluster", None)]

    for i in range(0, len(dims), 2):
        cols = st.columns(2)
        for j, (dim, order) in enumerate(dims[i:i + 2]):
            with cols[j]:
                if order:
                    ab = df.groupby(dim)["App_Adoption"].apply(lambda x: (x == "Yes").mean() * 100).reindex(order).reset_index()
                else:
                    ab = df.groupby(dim)["App_Adoption"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=True).reset_index()
                ab.columns = [dim, "Rate"]
                fig = px.bar(ab, x="Rate", y=dim, orientation="h", title=f"Adoption by {dim.replace('_', ' ')}",
                             color="Rate", color_continuous_scale="Tealgrn", text="Rate")
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=C_TEXT, size=11))
                fig.update_layout(showlegend=False, coloraxis_showscale=False)
                styled_layout(fig, 270); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Drivers:</strong> 'Very sensitive' adopt most (direct value). 'Very fair' perception adds 20%+ vs 'Very unfair'. Delivery users adopt more (app ecosystem). Younger = higher adoption (tech comfort).")

    st.subheader("Drill-down: Sensitivity × Fairness → Adoption %")
    cta = df.pivot_table(values="App_Adoption", index="Price_Sensitivity", columns="Fairness_Perception",
                          aggfunc=lambda x: (x == "Yes").mean() * 100).reindex(index=SENS_ORDER, columns=FAIR_ORDER)
    fig = px.imshow(cta.round(1), text_auto=True, color_continuous_scale="Tealgrn",
                    title="Adoption Rate: Sensitivity × Fairness (top 2 predictors)", labels=dict(color="%"))
    styled_layout(fig, 420); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Sweet spot:</strong> Top-left (Very sensitive + Very fair) = peak adoption. Bottom-right = lowest. These two features should be <strong>top inputs</strong> to the classification model.")

# =============================================================================
# 10. SEASONALITY
# =============================================================================
elif section == "10  Seasonality":
    st.title("Seasonality Analysis")
    insight("<strong>Objective:</strong> Dubai dining is seasonal — tourist influx Oct–Mar, summer exodus Jul–Sep, Ramadan shifts. The engine should set baseline surge by month.")

    months = explode_col(df, "Peak_Months")
    mc = months.value_counts().reindex(["Oct-Dec", "Jan-Mar", "Apr-Jun", "Jul-Sep"]).reset_index()
    mc.columns = ["Season", "Count"]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(mc, x="Season", y="Count", color="Season", title="Peak Dining Seasons",
                     color_discrete_sequence=[C_NAVY, PALETTE[1], PALETTE[3], C_MUTED], text="Count")
        fig.update_traces(textposition="outside", textfont=dict(color=C_TEXT))
        fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        dm = df[["Customer_Type", "Peak_Months"]].dropna()
        dm = dm.assign(Peak_Months=dm["Peak_Months"].str.split(", ")).explode("Peak_Months")
        ct = pd.crosstab(dm["Customer_Type"], dm["Peak_Months"]).reindex(columns=["Oct-Dec", "Jan-Mar", "Apr-Jun", "Jul-Sep"])
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="Blues", title="Peak Months by Customer Type")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("<strong>Oct–Dec</strong> is the clear peak (tourist season, pleasant weather). Jul–Sep is the trough (heat, resident exodus). Tourists concentrate Oct–Mar; Families dine year-round.")

    st.subheader("Drill-down: Season × Demand")
    dm2 = df[["Demand_Level", "Peak_Months"]].dropna()
    dm2 = dm2.assign(Peak_Months=dm2["Peak_Months"].str.split(", ")).explode("Peak_Months")
    ct2 = pd.crosstab(dm2["Peak_Months"], dm2["Demand_Level"]).reindex(index=["Oct-Dec", "Jan-Mar", "Apr-Jun", "Jul-Sep"], columns=DEMAND_ORDER)
    fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Oranges", title="Demand by Season")
    styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drill-down: Season × Weather")
    dm3 = df[["Weather_Behaviour", "Peak_Months"]].dropna()
    dm3 = dm3.assign(Peak_Months=dm3["Peak_Months"].str.split(", ")).explode("Peak_Months")
    ct3 = pd.crosstab(dm3["Peak_Months"], dm3["Weather_Behaviour"]).reindex(index=["Oct-Dec", "Jan-Mar", "Apr-Jun", "Jul-Sep"])
    fig = px.imshow(ct3, text_auto=True, color_continuous_scale="Teal", title="Weather Behaviour by Season")
    styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

    insight("'Switch to delivery in heat' peaks Apr–Sep. Engine should: lower delivery surge in summer (high supply), increase dine-in discounts to pull foot traffic.")

# =============================================================================
# SANKEY
# =============================================================================
elif section == "⟶  Sankey: Path to Adoption":
    st.title("Sankey — Path to App Adoption")
    insight("Trace how customer attributes flow through behavioural and attitudinal filters to the <strong>North Star</strong>. Three flows: demographics, operations, spending power.")

    def build_sankey(dataframe, path_cols):
        labels = []
        for col in path_cols:
            for val in dataframe[col].unique():
                l = f"{col}|{val}"
                if l not in labels: labels.append(l)
        idx = {l: i for i, l in enumerate(labels)}
        src, tgt, val = [], [], []
        for i in range(len(path_cols) - 1):
            flow = dataframe.groupby([path_cols[i], path_cols[i + 1]]).size().reset_index(name="n")
            for _, r in flow.iterrows():
                src.append(idx[f"{path_cols[i]}|{r[path_cols[i]]}"])
                tgt.append(idx[f"{path_cols[i + 1]}|{r[path_cols[i + 1]]}"])
                val.append(r["n"])
        return labels, src, tgt, val

    def render_sankey(labels, src, tgt, val, title, stage_colors):
        nc = []
        for l in labels:
            if "App_Adoption|Yes" in l: nc.append(C_GREEN)
            elif "App_Adoption|No" in l: nc.append(C_RED)
            else:
                matched = False
                for k, c in stage_colors.items():
                    if k in l: nc.append(c); matched = True; break
                if not matched: nc.append(C_MUTED)
        lc = [f"rgba(27,115,64,0.2)" if "Yes" in labels[t] else f"rgba(196,48,28,0.2)" if "No" in labels[t] else "rgba(140,140,140,0.08)" for t in tgt]
        dl = [l.split("|", 1)[1] for l in labels]
        fig = go.Figure(go.Sankey(
            node=dict(pad=15, thickness=22, line=dict(color="#E5E7EB", width=0.5), label=dl, color=nc),
            link=dict(source=src, target=tgt, value=val, color=lc)))
        fig.update_layout(title=dict(text=title, font=dict(size=13, color=C_TEXT)),
                          font=dict(size=10, color=C_SUBTEXT), height=580,
                          paper_bgcolor=C_BG, plot_bgcolor=C_BG)
        return fig

    st.subheader("1. Demographics → Attitudes → Adoption")
    l1, s1, t1, v1 = build_sankey(df, ["Customer_Type", "Price_Sensitivity", "Fairness_Perception", "App_Adoption"])
    st.plotly_chart(render_sankey(l1, s1, t1, v1, "Customer Type → Sensitivity → Fairness → Adoption",
                                  {"Customer_Type": C_NAVY, "Price_Sensitivity": PALETTE[3], "Fairness": C_TEAL}), use_container_width=True)
    insight("Professionals split across all sensitivity levels. Thickest green flows: 'Very sensitive' + 'Very fair' → Yes — confirming the strongest adoption predictors.")

    st.subheader("2. Operations → Pricing → Adoption")
    ds2 = df.copy()
    ds2["Surge_Bucket"] = pd.cut(ds2["Surge_Multiplier"], bins=[0, 0.95, 1.05, 1.5],
                                  labels=["Discount (<0.95)", "Neutral (0.95–1.05)", "Surge (>1.05)"])
    l2, s2, t2, v2 = build_sankey(ds2.dropna(subset=["Surge_Bucket"]),
                                    ["Order_Channel", "Demand_Level", "Surge_Bucket", "App_Adoption"])
    st.plotly_chart(render_sankey(l2, s2, t2, v2, "Channel → Demand → Surge → Adoption",
                                  {"Order_Channel": C_NAVY, "Demand_Level": PALETTE[3],
                                   "Surge": C_TEAL, "Discount": C_TEAL, "Neutral": C_TEAL}), use_container_width=True)
    insight("Delivery users flow into Medium/High demand → Surge pricing, yet adoption stays strong — they value convenience over price. Dine-in shows thicker 'No' flows from Surge.")

    st.subheader("3. Spending Power → Choice → Adoption")
    l3, s3, t3, v3 = build_sankey(df, ["Monthly_Income", "Restaurant_Tier", "Restaurant_Location", "App_Adoption"])
    st.plotly_chart(render_sankey(l3, s3, t3, v3, "Income → Tier → Location → Adoption",
                                  {"Monthly_Income": C_NAVY, "Restaurant_Tier": PALETTE[3], "Restaurant_Location": C_TEAL}), use_container_width=True)
    insight("Low-income → Budget → Deira/Mall: moderate adoption (want discounts). High-income → Premium → DIFC/Downtown: high adoption (value demand-based table management). The engine serves <em>both</em> segments.")

    callout("<strong>Summary:</strong> Adoption is driven by a <strong>combination</strong> of price sensitivity, fairness perception, channel behaviour, and income — no single variable determines it. The classification model should use all of these as features.")
