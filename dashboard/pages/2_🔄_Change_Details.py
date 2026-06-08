import streamlit as st
import pandas as pd
from monthly_stats import monthly_price_changes,monthly_book_changes,generate_stats_payload
import os

old_df = pd.read_csv("data/Books_cleaned_baseline.csv")
new_df = pd.read_csv("data/Books_cleaned.csv")
logging_df = pd.read_csv("data/monthly_monitor_log.csv")
added_books, removed_books = monthly_book_changes(old_df, new_df)
price_changes = monthly_price_changes(old_df, new_df)

st.set_page_config(
    page_title="Changes — MS Books Dashboard",
    page_icon="dashboard/logos/iconremovebg.ico",
    layout="wide"
)

st.sidebar.title("MS Books")
st.sidebar.caption("Monitoring Platform")

# #test
# removed_books = [
#     {
#         "Title": "IGCSE Unsolved Topical Physics Paper 6 (ATP) (2025-2026 Edition)",
#         "Subject Code": "0625",
#         "Type": "Unsolved Topical",
#         "Price": 1900
#     },
#     {
#         "Title": "IGCSE Unsolved Topical Physics Paper 4 (Theory) (2025-2026 Edition)",
#         "Subject Code": "0625",
#         "Type": "Unsolved Topical",
#         "Price": 2350
#     },
#     {
#         "Title": "IGCSE Unsolved Topical Physics Paper 2 (Mcqs) (2025-2026 Edition)",
#         "Subject Code": "Unknown",
#         "Type": "Unsolved Topical",
#         "Price": 1800
#     }
# ]

col1, col2 = st.columns([1,8])
col1.image("dashboard/logos/logoremovebg.png", width=100)
col2.title("Change Details")

col1,col2,col3 = st.columns(3)
col1.metric("Books Added",len(added_books))
col2.metric("Books Removed",len(removed_books))
col3.metric("Price Changes", len(price_changes))

st.subheader("Books Added")
if added_books:
    st.dataframe(added_books)
else:
    st.write("No books added last month")
st.subheader("Books Removed")
if removed_books:
    st.dataframe(removed_books)
else:
    st.write("No books removed last month")
st.subheader("Price Changes")
if price_changes:
    st.dataframe(price_changes)
else:
    st.write("No price changes in last month")

#UNCOMMENT BELOW WHEN DATA IS SUFFICIENT

chart_data = logging_df.drop_duplicates(subset=["Date"],keep="last").set_index("Date")
size_chart_data = chart_data["Total Books"].dropna()
changes_table_data = chart_data[["New Books","Removed Books"]]
if len(size_chart_data) >= 3:
    st.subheader("Inventory Size Over Time")
    st.line_chart(size_chart_data)
if len(changes_table_data) >= 3:
    st.subheader("Book Additions and Removals Over Time")
    st.table(changes_table_data)


history_files = sorted([f for f in os.listdir("data/history")if f.endswith("_catalog.csv")])
if len(history_files) >= 3:
    dates = [f.replace("_catalog.csv","")for f in history_files]
    st.subheader("Historical Catalog Snapshots")
    selected_file = st.selectbox("Select Snapshot",dates)

    snapshot_df = pd.read_csv(f"data/history/{selected_file}_catalog.csv")
    inventory = generate_stats_payload(snapshot_df)

    inventory_overview = inventory["inventory_overview"]
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Books", inventory_overview["total_books"])
    col2.metric("Unique Subjects", inventory_overview["unique_subjects"])
    col3.metric("Unique Authors", inventory_overview["unique_authors"])

    filtered_df = snapshot_df.copy()
    grades = ["All"] + sorted(snapshot_df["Grade"].dropna().unique().tolist())
    types = ["All"] + sorted(snapshot_df["Type"].dropna().unique().tolist())

    col1,col2,col3,col4 = st.columns(4)
    search = col1.text_input("Search Title")
    selected_grade = col2.selectbox("Grade",grades)
    selected_type = col3.selectbox("Book Type",types)
    sort_by = col4.selectbox("Sort By",["Title", "Price", "Subject code"])
    if search:
        filtered_df = filtered_df[filtered_df["Title"].str.contains(search, case=False, na=False)]
    if selected_grade != "All":
        filtered_df = filtered_df[filtered_df["Grade"] == selected_grade]
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["Type"] == selected_type]
    filtered_df = filtered_df.sort_values(sort_by)
    st.caption(f"{len(filtered_df)} books found")
    st.dataframe(filtered_df)


