import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Hydrogeology Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Hydrogeology Dashboard")

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("groundwater_data.csv")

# -------------------------
# SIDEBAR FILTER
# -------------------------

st.sidebar.header("Filters")

village = st.sidebar.selectbox(
    "Select Village",
    ["All"] + sorted(df["Village"].unique())
)

if village != "All":
    df = df[df["Village"] == village]

# -------------------------
# KPI CARDS
# -------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Wells",
    len(df)
)

col2.metric(
    "Avg Water Level (m)",
    round(df["Water_Level_m"].mean(), 2)
)

col3.metric(
    "Avg Rainfall (mm)",
    round(df["Rainfall_mm"].mean(), 2)
)

# -------------------------
# DATA TABLE
# -------------------------

st.subheader("Groundwater Data")

st.dataframe(df, use_container_width=True)

# -------------------------
# RISK CLASSIFICATION
# -------------------------

def risk(level):
    if level < 20:
        return "High Risk"
    elif level < 25:
        return "Medium Risk"
    else:
        return "Safe"

df["Risk"] = df["Water_Level_m"].apply(risk)

st.subheader("Risk Classification")

st.dataframe(
    df[
        ["Well_ID",
         "Village",
         "Water_Level_m",
         "Risk"]
    ],
    use_container_width=True
)

# -------------------------
# CHARTS
# -------------------------

col4, col5 = st.columns(2)

with col4:

    st.subheader("Rainfall vs Groundwater")

    fig, ax = plt.subplots()

    ax.scatter(
        df["Rainfall_mm"],
        df["Water_Level_m"],
        color="blue"
    )

    ax.set_xlabel("Rainfall (mm)")
    ax.set_ylabel("Water Level (m)")
    ax.set_title("Rainfall vs Groundwater")

    st.pyplot(fig)

with col5:

    st.subheader("Groundwater Levels")

    fig2, ax2 = plt.subplots()

    ax2.bar(
        df["Well_ID"],
        df["Water_Level_m"],
        color="green"
    )

    ax2.set_xlabel("Well ID")
    ax2.set_ylabel("Water Level (m)")
    ax2.set_title("Water Levels")

    st.pyplot(fig2)

# -------------------------
# RISK PIE CHART
# -------------------------

st.subheader("Risk Distribution")

risk_count = df["Risk"].value_counts()

fig3, ax3 = plt.subplots()

ax3.pie(
    risk_count,
    labels=risk_count.index,
    autopct="%1.1f%%"
)

st.pyplot(fig3)

# -------------------------
# MAP
# -------------------------

st.subheader("Well Locations")

map_df = df.rename(
    columns={
        "Latitude": "lat",
        "Longitude": "lon"
    }
)

st.map(map_df[["lat", "lon"]])

# -------------------------
# ANOMALY DETECTION
# -------------------------

st.subheader("Water Quality Anomalies (TDS > 500)")

anomalies = df[df["TDS"] > 500]

st.dataframe(
    anomalies[
        [
            "Well_ID",
            "Village",
            "TDS"
        ]
    ],
    use_container_width=True
)

# -------------------------
# INSIGHTS
# -------------------------

highest = df.loc[
    df["Water_Level_m"].idxmax()
]

lowest = df.loc[
    df["Water_Level_m"].idxmin()
]

st.subheader("Insights")

st.success(f"""
Highest Water Level : {highest['Well_ID']} ({highest['Water_Level_m']} m)

Lowest Water Level : {lowest['Well_ID']} ({lowest['Water_Level_m']} m)

Average Rainfall : {round(df['Rainfall_mm'].mean(),2)} mm

Potential Water Quality Anomalies : {len(anomalies)}
""")