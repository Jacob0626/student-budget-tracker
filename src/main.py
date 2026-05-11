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

def validate_columns(df: pd.DataFrame) -> bool:
    """Check if the transaction data has the required columns."""
    required_columns = ["date", "description", "category", "type", "amount"]
    
    for column in required_columns:
        if column not in df.columns:
            return False
    
    return True

def load_transactions(file_source) -> pd.DataFrame:
    """Load transaction data from a CSV file and prepare it for analysis."""
    if isinstance(file_source, str):
        df = pd.read_csv(get_data_path(file_source))
    else:
        df= pd.read_csv(file_source)
    
    if not validate_columns(df):
        st.error("The CSV file must include these columns: date, description, category, type, amount.")
        st.stop()
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    df["description"] = df["description"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["type"] = df["type"].astype(str).str.strip()
    
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

def save_transactions(df: pd.DataFrame, filename: str) -> None:
    """Save transaction data to a CSV file inside the data folder."""
    df.to_csv(get_data_path(filename), index=False)

def get_default_transaction_file() -> str:
    """Choose saved transactions if they exist, otherwise use sample data."""
    saved_file_path = get_data_path("saved_transactions.csv")
    
    if os.path.exists(saved_file_path):
        return "saved_transactions.csv"
    return "sample_transactions.csv"

def load_budget_settings() -> dict:
    """Load budget settings from a JSON file, or return default settings."""
    settings_path = get_data_path("budget_settings.json")
    
    default_settings = {
        "savings_goal": 100.0,
        "category_budgets": {
            "Food": 200.0,
            "Gas": 120.0,
            "Groceries": 250.0,
            "Entertainment": 100.0,
            "Subscriptions": 50.0
        }
    }
    
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_settings

def save_budget_settings(settings: dict) -> None:
    """Save budget settings to a JSON file inside the data folder."""
    with open(get_data_path("budget_settings.json"), "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

def compare_budget_to_spending(df: pd.DataFrame, budget_settings: dict) -> pd.DataFrame:
    """Compare category budgets to actual spending."""
    expenses_df = df[df["type"] == "Expense"]
    
    spending_by_category = expenses_df.groupby("category", as_index=False)["amount"].sum()
    
    budget_rows = []
    
    for category, budget_amount in budget_settings["category_budgets"].items():
        spent_series = spending_by_category[spending_by_category["category"] == category]["amount"]
        
        if spent_series.empty:
            spent = 0.0
        else:
            spent = float(spent_series.iloc[0])
        
        remaining = budget_amount - spent
        
        if remaining >= 0:
            status = "Under Budget"
        else:
            status = "Over budget"
        
        budget_rows.append({
            "Category": category,
            "Budget": budget_amount,
            "Spent": spent,
            "Remaining": remaining,
            "Status": status
        })
    return pd.DataFrame(budget_rows)

def create_summary_report(summary: dict, budget_settings: dict) -> pd.DataFrame:
    """Create a simple financial summary report as a DataFrame."""
    report_data = {
        "Metric": [
            "Total Income",
            "Total Expenses",
            "Money Left",
            "Savings Rate",
            "Monthly Savings Goal",
        ],
        "Value": [
            round(summary["income"], 2),
            round(summary["expenses"], 2),
            round(summary["money_left"], 2),
            round(summary["savings_rate"], 1),
            round(budget_settings["savings_goal"], 2)
        ]
    }
    return pd.DataFrame(report_data)

st.title("Student Budget & Spending Habit Tracker")

st.write('''
This app will help students track income, expenses, budgets, and savings goals.
Users will be able to upload transaction data, view summaries, analyze spending habits, and save budget settings.
''')

st.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload transaction CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = load_transactions(uploaded_file)
    st.sidebar.success("Uploaded CSV loaded successfully.")
else:
    default_file = get_default_transaction_file()
    df = load_transactions(default_file)
    
    if default_file == "saved_transactions.csv":
        st.sidebar.success("Using saved transaction data.")
    else:
        st.sidebar.info("Using sample transaction data.")

category_options = ["All"] + sorted(df["category"].unique())
budget_settings = load_budget_settings()

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
        "Transaction Type",
        ["All", "Income", "Expense"]
    )
    
    category_filter = st.selectbox(
        "Category",
        category_options
    )

# Main page content
if page == "Dashboard":
    st.header("Dashboard")
    st.info("This section will show income, expenses, money left, and spending charts.")
    
    filtered_df = filter_transactions(df, transaction_type, category_filter)
    summary = calculate_summary(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", f"${summary['income']:.2f}")
    with col2:
        st.metric("Total Expenses", f"${summary['expenses']:.2f}")
    with col3:
        st.metric("Money Left", f"${summary['money_left']:.2f}")
    with col4:
        st.metric("Savings Rate", f"{summary['savings_rate']:.1f}%")
    
    report_df = create_summary_report(summary, budget_settings)
    
    csv_report = report_df.to_csv(index=False)
    
    st.download_button(
        label="Download Financial Summary",
        data=csv_report,
        file_name="financial_summary.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    if transaction_type != "Income":
        st.subheader("Spending by Category")
    
        category_summary = get_spending_by_category(filtered_df)
        
        if category_summary.empty:
            st.warning("No expense data available to show")
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
    
    type_summary = get_income_expense_summary(filtered_df)
    
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
    st.info("Upload, view, edit, and save transaction data. The table updates based on the selected filters.")
    
    filtered_df = filter_transactions(df, transaction_type, category_filter)
    
    st.subheader("Transaction Data")
    st.warning("Edit the full table and save your changes. Clear filters before saving.")
    
    edited_df = st.data_editor(
        filtered_df,
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Prevent saving filtered data by mistake
    filters_are_clear = transaction_type == "All" and category_filter == "All"
    
    if filters_are_clear:
        if st.button("Save Edited Transactions"):
            save_transactions(edited_df, "saved_transactions.csv")
            st.success("Edited transactions saved successfully")
    
    else:
        st.warning("Clear all filters before saving edited transactions.")


elif page == "Budget Goals":
    st.header("Budget Goals")
    st.info("Set your savings goal and monthly category budgets, then compare your budget to actual spending.")

    with st.form("budget_settings_form"):
        savings_goal = st.number_input(
            "Monthly Savings Goal",
            min_value=0.0,
            value=float(budget_settings["savings_goal"]),
            step=10.0
        )

        st.subheader("Category Budgets")
        
        food_budget = st.number_input(
            "Food Budget",
            min_value=0.0,
            value=float(budget_settings["category_budgets"].get("Food", 0.0)),
            step=10.0
        )
        
        gas_budget = st.number_input(
            "Gas Budget",
            min_value=0.0,
            value=float(budget_settings["category_budgets"].get("Gas", 0.0)),
            step=10.0
        )
        
        groceries_budget = st.number_input(
            "Groceries Budget",
            min_value=0.0,
            value=float(budget_settings["category_budgets"].get("Groceries", 0.0)),
            step=10.0
        )
        
        entertainment_budget = st.number_input(
            "Entertainment Budget",
            min_value=0.0,
            value=float(budget_settings["category_budgets"].get("Entertainment", 0.0)),
            step=10.0
        )
        
        subscriptions_budget = st.number_input(
            "Subscriptions Budget",
            min_value=0.0,
            value=float(budget_settings["category_budgets"].get("Subscriptions", 0.0)),
            step=10.0
        )
        
        submitted = st.form_submit_button("Save Budget Settings")
        
    if submitted:
        new_settings = {
            "savings_goal": savings_goal,
            "category_budgets": {
                "Food": food_budget,
                "Gas": gas_budget,
                "Groceries": groceries_budget,
                "Entertainment": entertainment_budget,
                "Subscriptions": subscriptions_budget
            }
        }
        
        save_budget_settings(new_settings)
        st.success("Budget settings saved successfully.")
        st.rerun()

    st.divider()
    st.subheader("Budget Progress")
    
    budget_comparison = compare_budget_to_spending(df, budget_settings)
    
    st.dataframe(
        budget_comparison,
        use_container_width=True
    )


elif page == "About":
    st.header("About")
    st.info("This project is being built with Python, Streamlit, Pandas, and GitHub.")