import streamlit as st

set.set_page_config(
    page_title = "Student Budget Tracker",
    Page_icon = "💰",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

st.title("Student Budget & Spending Habit Tracker")

st.write('''
This app will help students track income, expenses, budgets, and savings goals.
Users will be able to upload transcactions data, view summaries, analyze spendings habits, and save budget settings.
''')

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Transactions",
    "Budget Goals",
    "About"
])

with tab1:
    st.header("Das")