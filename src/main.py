import streamlit as st
import pandas as pd 
import os 
import json


st.set_page_config(
    page_title = "Student Budget Tracker",
    page_icon = "💰",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    """Return the full path for a file inside the data folder."""
    return os.path.join(APP_PATH, "data", filename)

def load_transactions(filename: str) -> pd.DataFrame:
    """Load transaction data from a CSV file and prepare it for analysis."""
    df = pd.read_csv(get_data_path(filename))
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    df = df.dropna(subset=["date", "amount"])
    
    return df

st.title("Student Budget & Spending Habit Tracker")

st.write('''
This app will help students track income, expenses, budgets, and savings goals.
Users will be able to upload transaction data, view summaries, analyze spending habits, and save budget settings.
''')

st.divider()

# Sidebar navigation menu
with st.sidebar:
    st.header("Navigation")
    
    page = st.radio(
        "Go to",
        ["Dashboard", "Transactions", "Budget Goals", "About"]
    )

# Main page content
if page == "Dashboard":
    st.header("Dashboard")
    st.info("This section will show income, expenses, money left, and spending charts.")

elif page == "Transactions":
    st.header("Transactions")
    st.info("This section will let the user upload, view, and edit transaction data.")
    
    df = load_transactions("sample_transactions.csv")
    
    st.subheader("Sample Transactions Data")
    st.dataframe(df)


elif page == "Budget Goals":
    st.header("Budget Goals")
    st.info("This section will let the user set budgets and savings goals.")

elif page == "About":
    st.header("About")
    st.info("This project is being built with Python, Streamlit, Pandas, and GitHub.")