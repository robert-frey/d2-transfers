import streamlit as st
import pandas as pd

# Google Sheet info
SHEET_ID = "1W4kSomg1hRHVAgperK4FtedsgCmeYFJx0Iw_BoKe3Jc"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# Load sheets
@st.cache_data
def load_sheet(sheet_name):
    url = BASE_URL + sheet_name.replace(" ", "%20")
    return pd.read_csv(url)

in_portal_df = load_sheet("In Portal")
d2_commits_df = load_sheet("D2 Commits")
leaving_d2_df = load_sheet("Leaving D2")

# --- TAB UI ---
st.title("D2 Transfer Portal Tracker")

tab1, tab2, tab3 = st.tabs(["In Portal", "D2 Commits", "Leaving D2"])

# --- TAB 1: IN PORTAL ---
with tab1:
    st.header("Players in the Transfer Portal")
    
    # Parse and format dates
    in_portal_df["enter_date"] = pd.to_datetime(in_portal_df["enter_date"], errors="coerce")
    in_portal_df = in_portal_df.sort_values("enter_date", ascending=False)
    
    # Sidebar filters
    with st.sidebar:
        st.subheader("🔍 Filter Players (In Portal)")
        date_range = st.date_input("Enter Date Range", [])
        school_filter = st.text_input("Previous School Contains", key="portal_school")

    filtered_df = in_portal_df.copy()
    
    if date_range and len(date_range) == 2:
        start, end = date_range
        filtered_df = filtered_df[
            (filtered_df["enter_date"] >= pd.Timestamp(start)) & 
            (filtered_df["enter_date"] <= pd.Timestamp(end))
        ]
    
    if school_filter:
        filtered_df = filtered_df[
            filtered_df["previous_school"].str.contains(school_filter, case=False, na=False)
        ]

    filtered_df["enter_date"] = filtered_df["enter_date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        filtered_df.reset_index(drop=True),
        use_container_width=True,
        height=700,
        column_config={
            "Name": st.column_config.Column("Player Name"),
            "enter_date": st.column_config.Column("Date Entered"),
            "previous_school": st.column_config.Column("Previous School")
        },
        hide_index=True
    )

# --- TAB 2: D2 COMMITS ---
with tab2:
    st.header("D2 Commits")

    st.dataframe(
        d2_commits_df,
        use_container_width=True,
        height=700,
        column_config={
            "Name": st.column_config.Column("Player Name"),
            "Prev School": st.column_config.Column("Previous School"),
            "New School": st.column_config.Column("New School"),
            "Level": st.column_config.Column("Level"),
            "Pos": st.column_config.Column("Position"),
            "Source": st.column_config.Column("Source")
        },
        hide_index=True
    )

# --- TAB 3: LEAVING D2 ---
with tab3:
    st.header("Players Leaving D2")

    # Convert 'Source' column to hyperlinks
    leaving_d2_df["Source"] = leaving_d2_df["Source"].apply(
        lambda x: f'<a href="{x}" target="_blank">Source</a>' if pd.notnull(x) else ""
    )

    st.write(
        leaving_d2_df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
