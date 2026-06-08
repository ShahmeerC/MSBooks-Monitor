import streamlit as st
import pandas as pd

books_df = pd.read_csv("data/Books_cleaned.csv")
logging_df = pd.read_csv("data/monthly_monitor_log.csv")

st.set_page_config(
    page_title="MS Books Dashboard",
    page_icon="dashboard/logos/iconremovebg.ico",
    layout="wide"
)

st.sidebar.title("MS Books")
st.sidebar.caption("Monitoring Platform")

col1, col2 = st.columns([1,8])
col1.image("dashboard/logos/logoremovebg.png", width=100)
col2.title("MS Books Monitoring Dashboard")

st.write("Welcome to the monitoring system.")

books = len(books_df)
latest = logging_df.iloc[-1].to_dict()
added = latest["New Books"]
removed = latest["Removed Books"]
price_changes = latest["Price Changes"]
change_details = latest["Change Details"]
latest_run = latest["Date"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", books)
col2.metric("Books Added", added)
col3.metric("Books Removed", removed)
col4.metric("Price Changes", price_changes)

type_distribution = books_df["Type"].value_counts()
st.subheader("Distribution of Books by Type")
st.bar_chart(type_distribution)

chart_data = logging_df.drop_duplicates(subset=["Date"],keep="last").set_index("Date")
size_chart_data = chart_data["Total Books"].dropna()
if len(size_chart_data) >= 3:
    st.subheader("Inventory Size Over Time")
    st.line_chart(size_chart_data)

st.metric("Latest Run",latest_run)



