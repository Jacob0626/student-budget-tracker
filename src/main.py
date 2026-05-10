import streamlit as st

st.set_page_config(
    page_title = "Student Budget Tracker",
    page_icon = "💰",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

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
    st.info