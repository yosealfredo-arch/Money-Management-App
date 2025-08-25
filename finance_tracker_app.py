import streamlit as st
import pandas as pd
import datetime

# Initialize session state for data storage if not exists
if "transactions" not in st.session_state:
    st.session_state["transactions"] = pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount"])

st.title("💰 Personal Finance Tracker")

# Sidebar for navigation
menu = st.sidebar.radio("Menu", ["Add Transaction", "Dashboard", "Data Table"])

# Add Transaction Page
if menu == "Add Transaction":
    st.header("➕ Add Transaction")
    with st.form("transaction_form"):
        date = st.date_input("Date", datetime.date.today())
        trans_type = st.selectbox("Type", ["Income", "Expense"])
        if trans_type == "Income":
            category = st.selectbox("Category", ["Freelance", "Trading", "Bank Interest", "Salary"])
        else:
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Shopping"])
        description = st.text_input("Description")
        amount = st.number_input("Amount (IDR)", min_value=0, step=1000)
        submitted = st.form_submit_button("Add")

        if submitted and amount > 0:
            new_transaction = pd.DataFrame({
                "Date": [date],
                "Type": [trans_type],
                "Category": [category],
                "Description": [description],
                "Amount": [amount]
            })
            st.session_state["transactions"] = pd.concat([st.session_state["transactions"], new_transaction], ignore_index=True)
            st.success("Transaction added successfully!")

# Dashboard Page
elif menu == "Dashboard":
    st.header("📊 Financial Dashboard")
    df = st.session_state["transactions"]

    if not df.empty:
        total_income = df[df["Type"] == "Income"]["Amount"].sum()
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expense

        st.metric("Total Income", f"Rp {total_income:,.0f}")
        st.metric("Total Expense", f"Rp {total_expense:,.0f}")
        st.metric("Balance", f"Rp {balance:,.0f}")

        # Income and Expense breakdown
        st.subheader("Breakdown by Category")
        breakdown = df.groupby(["Type", "Category"])["Amount"].sum().reset_index()
        st.dataframe(breakdown)

        # Chart
        st.subheader("Income vs Expense Over Time")
        chart_df = df.groupby(["Date", "Type"])["Amount"].sum().reset_index()
        st.line_chart(chart_df, x="Date", y="Amount", color="Type")
    else:
        st.info("No transactions yet. Add some in 'Add Transaction'.")

# Data Table Page
elif menu == "Data Table":
    st.header("📑 All Transactions")
    st.dataframe(st.session_state["transactions"])
