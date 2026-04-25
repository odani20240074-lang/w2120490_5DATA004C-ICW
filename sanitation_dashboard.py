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

