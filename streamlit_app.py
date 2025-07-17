import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


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
team_commits = load_sheet("Team Commits")

# --- TAB UI ---
st.title("D2 Transfer Portal Tracker")

tab1, tab6, tab2, tab3, tab4, tab5, = st.tabs(["In Portal", "D2 Team Commits","D2 Commits", "D2 Commits Batting Stats","D2 Commits Pitching Stats","Leaving D2"])

# --- TAB 1: IN PORTAL ---
with tab1:
    st.header("Players in the Transfer Portal")
    
    # Parse and format dates
    in_portal_df["enter_date"] = pd.to_datetime(in_portal_df["enter_date"], errors="coerce")
    in_portal_df = in_portal_df.sort_values("enter_date", ascending=False)
    
    filtered_df = in_portal_df.copy()
    filtered_df["enter_date"] = filtered_df["enter_date"].dt.strftime("%Y-%m-%d")

    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(filtered_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
    )

# --- TAB 2: D2 teAM COMMITS ---
with tab6:
    st.header("D2 Team Commits")

    sorted_df = team_commits.sort_values(by="Total", ascending=False)

    gb = GridOptionsBuilder.from_dataframe(sorted_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(sorted_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
    )

# --- TAB 2: D2 COMMITS ---
with tab2:
    st.header("D2 Commits")

    school_options = sorted(d2_commits_df["New School"].dropna().unique())
    school_options.insert(0, "All") # Add 'All' as the first option

# Selectbox for filtering
    selected_school = st.selectbox(label="Filter by New School", options=school_options)

# Filter the DataFrame based on selection
    if selected_school == "All":
        filtered_df = d2_commits_df
    else:
        filtered_df = d2_commits_df[d2_commits_df["New School"] == selected_school]

    sorted_df = filtered_df.sort_values(by="New School", ascending=True).iloc[:, 0:5]

    gb = GridOptionsBuilder.from_dataframe(sorted_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(sorted_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
    )

# --- TAB 5: LEAVING D2 ---
with tab5:
    st.header("Players Leaving D2")

    sort_df = leaving_d2_df.sort_values(by="Prev School", ascending=True).iloc[:, 0:5]


    gb = GridOptionsBuilder.from_dataframe(sort_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(sort_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
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
    gb = GridOptionsBuilder.from_dataframe(bat_sort_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(bat_sort_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
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

    gb = GridOptionsBuilder.from_dataframe(pit_sort_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid_options = gb.build()

    AgGrid(pit_sort_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
           custom_css={
        ".ag-root-wrapper": {
            "background-color": "#000000",
            "color": "#ffffff"
        },
        ".ag-header": {
            "background-color": "#000000",
            "color": "#ffffff" 
        }
    }
    )
