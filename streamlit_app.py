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
d2_bat_stats = load_sheet("D2 Commits Batting Stats")
d2_pit_stats = load_sheet("D2 Commits Pitching Stats")

# --- TAB UI ---
st.title("D2 Transfer Portal Tracker")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["In Portal", "D2 Commits", "D2 Commits Batting Stats","D2 Commits Pitching Stats","Leaving D2"])

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

    sorted_df = d2_commits_df.sort_values(by="New School", ascending=True)

    st.dataframe(
        sorted_df.iloc[:, 0:5],
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

# --- TAB 5: LEAVING D2 ---
with tab5:
    st.header("Players Leaving D2")

    sort_df = leaving_d2_df.sort_values(by="Prev School", ascending=True)


    st.dataframe(
        sort_df.iloc[:, 0:5],
        use_container_width=True,
        height=700,
        column_config={
            "Name": st.column_config.Column("Player Name"),
            "Prev School": st.column_config.Column("Previous School"),
            "New School": st.column_config.Column("New School"),
            "Level": st.column_config.Column("Level"),
            "Pos": st.column_config.Column("Position")        },
        hide_index=True
    )
# --- TAB 3: Batting Stats ---
with tab3:
    st.header("D2 Commits Batting Stats")

    # Unique New School values for the filter
    school_options = sorted(d2_bat_stats["New School"].dropna().unique())

    # Sidebar or inline filter
    selected_schools = st.multiselect("Filter by New School", options=school_options)

    # Filter the DataFrame based on selection
    if selected_schools:
        filtered_df = d2_bat_stats[d2_bat_stats["New School"].isin(selected_schools)]
    else:
        filtered_df = d2_bat_stats

    # Sort the filtered DataFrame
    bat_sort_df = filtered_df.sort_values(by="New School", ascending=True)

    # Display the table
    st.dataframe(
        bat_sort_df,
        use_container_width=True,
        height=700,
        column_config={
            "Name": st.column_config.Column("Player Name"),
            "Prev School": st.column_config.Column("Previous School"),
            "New School": st.column_config.Column("New School"),
            "Level": st.column_config.Column("Level"),
            "Pos": st.column_config.Column("Position"),
            "PA": st.column_config.Column("PA"),
            "BA": st.column_config.Column("BA"),
            "OPS": st.column_config.Column("OPS"),
            "HR": st.column_config.Column("HR"),
            "RBI": st.column_config.Column("RBI"),
            "SB": st.column_config.Column("SB"),
            "FLD": st.column_config.Column("FLD"),
        },
        hide_index=True
    )

# --- TAB 4: Pitching Stats ---
with tab4:
    st.header("D2 Commits Pitching Stats")

    # Create list of unique New School values for filtering
    school_options = sorted(d2_pit_stats["New School"].dropna().unique())

    # Multiselect filter for New School
    selected_schools = st.multiselect("Filter by New School", options=school_options)

    # Filter the DataFrame based on selected schools
    if selected_schools:
        filtered_df = d2_pit_stats[d2_pit_stats["New School"].isin(selected_schools)]
    else:
        filtered_df = d2_pit_stats

    # Sort the filtered DataFrame
    pit_sort_df = filtered_df.sort_values(by="New School", ascending=True)

    # Display the table
    st.dataframe(
        pit_sort_df,
        use_container_width=True,
        height=700,
        column_config={
            "Name": st.column_config.Column("Player Name"),
            "Prev School": st.column_config.Column("Previous School"),
            "New School": st.column_config.Column("New School"),
            "Level": st.column_config.Column("Level"),
            "Pos": st.column_config.Column("Position"),
            "IP": st.column_config.Column("IP"),
            "ERA": st.column_config.Column("ERA"),
            "WHIP": st.column_config.Column("WHIP"),
            "W": st.column_config.Column("W"),
            "L": st.column_config.Column("L"),
            "SO": st.column_config.Column("SO"),
            "KBB": st.column_config.Column("KBB"),
        },
        hide_index=True
    )
