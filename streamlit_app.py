import streamlit as st
import pandas as pd

# Load and format data
df = pd.read_csv("transfers.csv", parse_dates=["enter_date"])
df = df.sort_values("enter_date", ascending=False)  # Sort from latest to earliest

# Title
st.title("D2 Transfer Portal Tracker")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Players")
    date_range = st.date_input("Enter Date Range", [])
    school_filter = st.text_input("Previous School Contains")

# Apply filters
filtered_df = df.copy()

if date_range and len(date_range) == 2:
    start, end = date_range
    filtered_df = filtered_df[(filtered_df["enter_date"] >= pd.Timestamp(start)) & 
                              (filtered_df["enter_date"] <= pd.Timestamp(end))]

if school_filter:
    filtered_df = filtered_df[filtered_df["previous_school"].str.contains(school_filter, case=False, na=False)]

# Format columns
filtered_df["enter_date"] = filtered_df["enter_date"].dt.strftime("%Y-%m-%d")

# Show styled table
st.dataframe(
    filtered_df.reset_index(drop=True),
    use_container_width=True,
    height=800,  # Increase this for more vertical room
    column_config={
        "Name": st.column_config.Column("Player Name"),
        "enter_date": st.column_config.Column("Date Entered"),
        "previous_school": st.column_config.Column("Previous School"),
        "new_school": st.column_config.Column("New School"),
    },
    hide_index=True
)
