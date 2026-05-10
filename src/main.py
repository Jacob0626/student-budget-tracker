import streamlit as st
import pandas as pd 
import os 
import json
import plotly.express as px 


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

def calculate_summary(df: pd.DataFrame) -> dict:
    """Calculate basic income and expense summary values."""
    income = df[df["type"] == "Income"]["amount"].sum()
    expenses= df[df["type"] == "Expense"]["amount"].sum()
    money_left = income - expenses 
    
    if income > 0:
        savings_rate = (money_left / income) * 100
    
    else:
        savings_rate = 0
    
    return {
        "income": income,
        "expenses": expenses,
        "money_left": money_left,
        "savings_rate": savings_rate
    }

def get_spending_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Group expense transactions by category."""
    expenses_df = df[df["type"] == "Expense"]
    
    category_summary = expenses_df.groupby("category", as_index=False)["amount"].sum()
    category_summary = category_summary.sort_values("amount", ascending=False)
    
    return category_summary

def get_income_expense_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Group transactions by type to compare income and expenses."""
    type_summary = df.groupby("type", as_index=False)["amount"].sum()
    
    return type_summary

def filter_transactions(df: pd.DataFrame, selected_type: str, selected_category: str) -> pd.DataFrame:
    """Filter transactions by type and category."""
    filtered_df = df.copy()
    
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["type"] == selected_type]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    
    return filtered_df


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
    
    st.divider()
    st.header("Filters")
    
    transaction_type = st.selectbox(
        "transaction Type",
        ["All", "Income", "Expense"]
    )
    
    category_filter = st.selectbox(
        "Category",
        ["All", "Income", "Food", "Gas", "Subscriptions", "Groceries", "Entertainment"]
    )

# Main page content
if page == "Dashboard":
    st.header("Dashboard")
    st.info("This section will show income, expenses, money left, and spending charts.")
    
    df = load_transactions("sample_transactions.csv")
    
    summary = calculate_summary(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", f"${summary['income']:.2f}")
    with col2:
        st.metric("Total Expenses", f"${summary['expenses']:.2f}")
    with col3:
        st.metric("Money Left", f"${summary['money_left']:.2f}")
    with col4:
        st.metric("Savings Rate", f"{summary['savings_rate']:.1f}%")
    
    st.divider()
    st.subheader("Spending by Category")
    
    category_summary = get_spending_by_category(df)
    
    if category_summary.empty:
        st.warning("No expense data avaliable to show")
    else:
        fig = px.bar(
            category_summary,
            x="category",
            y="amount",
            title="Total Expenses by Category",
            text_auto=".2f"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Income vs Expenses")
    
    type_summary = get_income_expense_summary(df)
    
    fig = px.bar(
        type_summary,
        x="type",
        y="amount",
        title="Income Compared to Expenses",
        text_auto=".2f"
    )
    
    st.plotly_chart(fig, use_container_width=True)


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