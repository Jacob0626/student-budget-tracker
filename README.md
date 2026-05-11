# Student Budget & Spending Habit Tracker

---

## Project Description

Student Budget & Spending Habit Tracker is a Streamlit web app that helps students track their income, expenses, budgets, and savings goals.

The app allows users to upload transaction data, view financial summaries, filter transactions, edit saved data, compare spending to budget goals, and download a simple financial summary report.

The main goal of this project is to help students better understand where their money is going each month and whether they are staying within their budget.

---

## Main Features

- Upload a CSV file with income and expense transactions
- Use sample transaction data if no file is uploaded
- Validate that uploaded CSV files have the required columns
- View total income, total expenses, money left, and savings rate
- Filter data by transaction type and category
- View charts for spending by category and income vs expenses
- Edit transaction data inside the app
- Save edited transactions to a CSV file
- Automatically load saved transaction data when the app restarts
- Set a monthly savings goal
- Set category budgets for food, gas, groceries, entertainment, and subscriptions
- Save and load budget settings using a JSON file
- Compare actual spending to budget goals
- Download a financial summary report as a CSV file

---

## Required CSV Format

Uploaded CSV files must include these columns:

```csv
date,description,category,type,amount
```

Example:

```csv
2026-04-01,Paycheck,Income,Income,500.00
2026-04-02,Chipotle,Food,Expense,14.50
2026-04-03,Gas Station,Gas,Expense,42.00
```

The `type` column should use either:

```text
Income
Expense
```

---

## How to Run the App

From the root folder of the project, run:

```bash
streamlit run dist/main.py
```

The production version of the app is inside the `dist/` folder.

---

## File Structure

```text
student-budget-tracker/
├── README.md
├── demo.mp4
├── src/
│   ├── main.py
│   └── data/
│       ├── sample_transactions.csv
│       ├── saved_transactions.csv
│       └── budget_settings.json
└── dist/
    ├── main.py
    └── data/
        ├── sample_transactions.csv
        ├── saved_transactions.csv
        └── budget_settings.json
```

---

## Folder Explanation

- `src/`: Development version of the app. This is where the app was built, tested, and changed during development.
- `dist/`: Stable production version of the app. This is the version that should be graded.
- `data/`: Contains the CSV and JSON files used by the app.
- `sample_transactions.csv`: Default sample data used when no uploaded file is provided.
- `saved_transactions.csv`: Stores edited transaction data saved by the user.
- `budget_settings.json`: Stores the user’s savings goal and category budgets.
- `demo.mp4`: Short demo video showing the app’s main features.

---

## User Instructions

1. Open the app using:

```bash
streamlit run dist/main.py
```

2. Use the sidebar to upload a transaction CSV file or use the sample data.
3. Use the sidebar filters to view specific transaction types or categories.
4. Open the Dashboard page to view summaries and charts.
5. Open the Transactions page to edit and save transaction data.
6. Open the Budget Goals page to set savings goals and category budgets.
7. Download the financial summary report from the Dashboard page.

---

## Tools and Libraries Used

- Python
- Streamlit
- Pandas
- Plotly Express
- JSON
- CSV files
- GitHub
- GitDoc for version control workflow

---

## AI Use Statement

AI assistance was used during this project for debugging errors, improving documentation, explaining some Streamlit/Pandas concepts, and helping write part of the README. 

---

## Known Limitations and Future Improvements

- The app expects uploaded CSV files to follow the required column format.
- The current budget categories are fixed to common student spending categories.
- The app saves data locally in CSV and JSON files instead of using a database.
- Future improvements could include custom budget categories, date range filters, monthly reports, and a more advanced export option.

---