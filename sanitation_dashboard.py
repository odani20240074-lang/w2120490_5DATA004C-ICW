import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global Sanitation Dashboard",
    page_icon="💧",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("sanitation_clean.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# Continent Groups
continent_groups = {
    "Asia": [
        "India", "China", "Japan", "Thailand", "Nepal", "Pakistan",
        "Bangladesh", "Philippines", "Indonesia", "Turkey", "Iran",
        "Iraq", "Israel", "Jordan", "Kazakhstan", "Myanmar"
    ],
    "Europe": [
        "United Kingdom", "Germany", "France", "Italy", "Spain",
        "Netherlands", "Sweden", "Poland", "Greece", "Austria",
        "Switzerland", "Ireland", "Portugal"
    ],
    "Africa": [
        "Nigeria", "Kenya", "Ethiopia", "Ghana", "Uganda",
        "Tanzania", "Morocco", "Algeria", "Egypt", "Senegal"
    ],
    "North America": [
        "United States", "Canada", "Mexico", "Cuba"
    ],
    "South America": [
        "Brazil", "Argentina", "Chile", "Peru", "Colombia"
    ],
    "Oceania": [
        "Australia", "New Zealand", "Papua New Guinea", "Samoa", "Tonga"
    ]
}

continent_map = {}

for continent, countries in continent_groups.items():
    for country in countries:
        continent_map[country] = continent

df["continent"] = df["country"].map(continent_map)
df["continent"] = df["continent"].fillna("Other")

# Title of the dashboard
st.title("💧 Global Sanitation Dashboard")
st.markdown("Safely managed sanitation coverage across the world (2000–2020)")

# Sidebar filters
st.sidebar.header("Filters")

year = st.sidebar.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max()),
    2020,
    key="year"
)

area_type = st.sidebar.selectbox(
    "Select Area Type",
    ["Total", "Rural area", "Urban area"],
    key="area_type"
)

projection = st.sidebar.selectbox(
    "Map Projection",
    ["natural earth", "orthographic", "mercator", "equirectangular"],
    key="projection"
)

countries = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    key="countries"
)

# Filtered Data
df_filtered = df[
    (df["year"] == year) &
    (df["area_type"] == area_type)
].copy()

df_filtered["continent"] = df_filtered["country"].map(continent_map)

# KPI Metrics
st.subheader("📊 Key Metrics")

avg = df_filtered["value"].mean()
highest = df_filtered.nlargest(1, "value").iloc[0]
lowest = df_filtered.nsmallest(1, "value").iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "🌍 Global Average",
    f"{avg:.1f}%"
)

col2.metric(
    "🏆 Highest Coverage",
    highest["country"],
    f"{highest['value']:.1f}%"
)

col3.metric(
    "⚠️ Lowest Coverage",
    lowest["country"],
    f"{lowest['value']:.1f}%"
)

# Chart 1 - World Map
st.subheader("🗺️ World Map")

df_map = df[
    (df["area_type"] == area_type) &
    (df["year"] == year)
]

fig_map = px.choropleth(
    df_map,
    locations="country_code",
    color="value",
    hover_name="country",
    color_continuous_scale="Blues",
    range_color=(0, 100)
)

fig_map.update_layout(
    geo=dict(
        projection_type=projection,

        showframe=False,
        showcoastlines=True,
        showcountries=True,
        showland=True,
        landcolor="#1f2937",
        oceancolor="#0b1220",
        showocean=True,
        bgcolor="#0b1220"
    ),

    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",

    font=dict(color="white"),
    height=600,
    margin=dict(l=0, r=0, t=40, b=0)
)

fig_map.update_traces(
    marker_line_color="rgba(255,255,255,0.2)",
    marker_line_width=0.4
)

st.plotly_chart(fig_map, use_container_width=True)

# Chart 2 - Trend line
st.subheader("📈 Sanitation Trend Over Time")

df_trend = df[
    (df["country"].isin(selected_countries)) &
    (df["area_type"] == area_type)
]

fig_line = px.line(df_trend, x="year", y="value", color="country")
st.plotly_chart(fig_line, use_container_width=True)

# Chart 3 - Top 10 Countries
st.subheader("🏆 Top Countries")

top_n = st.slider("Top N Countries", 5, 30, 10, key="top_n")

df_top = df_filtered.nlargest(top_n, "value")

fig_top = px.bar(df_top, x="value", y="country", orientation="h", color="value")
st.plotly_chart(fig_top, use_container_width=True)

