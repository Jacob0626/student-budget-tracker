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

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Transactions",
    "Budget Goals",
    "About"
])

with tab1:
    st.header("Dashboard")
    st.info("This section will show income, expenses, money left, and spending charts")

with tab2:
    st.header("Transactions")
    st.info("This section will let the user upload, view, and edit transaction data")

with tab3:
    st.header("Budget Goals")
    st.info("This section will let the user set budgets and saving goals.")

with tab4:
    st.header("About")
    st.info("This project is being built with Python, Streamlit, Pandas, and GitHub.")