import streamlit as st
import pandas as pd
from monthly_stats import generate_stats_payload

books_df = pd.read_csv("data/Books_cleaned.csv")
inventory = generate_stats_payload(books_df)

st.set_page_config(
    page_title="Catalog — MS Books Dashboard",
    page_icon="dashboard/logos/iconremovebg.ico",
    layout="wide"
)

st.sidebar.title("MS Books")
st.sidebar.caption("Monitoring Platform")

col1, col2 = st.columns([1,8])
col1.image("dashboard/logos/logoremovebg.png", width=100)
col2.title("Catalog")

inventory_overview = inventory["inventory_overview"]
col1,col2,col3 = st.columns(3)
col1.metric("Total Books", inventory_overview["total_books"])
col2.metric("Unique Subjects", inventory_overview["unique_subjects"])
col3.metric("Unique Authors", inventory_overview["unique_authors"])

filtered_df = books_df.copy()
grades = ["All"] + sorted(books_df["Grade"].dropna().unique().tolist())
types = ["All"] + sorted(books_df["Type"].dropna().unique().tolist())
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

distributions = inventory["distributions"]
col1,col2 = st.columns(2)
col1.subheader("Distribution of Books by Grade")
col1.bar_chart(distributions["grade_distribution"])
col2.subheader("Distribution of Books by Type")
col2.bar_chart(distributions["type_distribution"])

col1,col2 = st.columns(2)
col1.subheader("Top 10 Subjects")
col1.table(distributions["subject_distribution(top 10)"])
col2.subheader("Top 10 Most Expensive Books")
col2.table(inventory["top_expensive_books"])

st.subheader("Average Prices by Book Type")
st.bar_chart(books_df.groupby("Type")["Price"].mean().round(2).to_dict())





