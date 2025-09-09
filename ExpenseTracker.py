import streamlit as st
import pandas as pd
import json
import os

st.title("📊 Expense Tracker App")

# Upload or select file
uploaded_file = st.file_uploader("Choose a file", type=["json", "csv", "xlsx"])

if uploaded_file is not None:
    # Detect file type
    file_extension = uploaded_file.name.split('.')[-1]
    
    if file_extension == "json":
        expenses = json.load(uploaded_file)
    elif file_extension == "csv":
        expenses = pd.read_csv(uploaded_file).to_dict(orient="records")
    elif file_extension == "xlsx":
        df = pd.read_excel(uploaded_file)
        expenses = df.to_dict(orient="records")
    else:
        st.error("Unsupported file format")
        expenses = []
else:
    expenses = []

if "expenses" not in st.session_state:
    st.session_state.expenses = expenses

# Form to add new expense
with st.form("add_expense"):
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_expense = {"category": category, "amount": amount}
        st.session_state.expenses.append(new_expense)
        st.success("Expense added!")

# Display expenses
if st.session_state.expenses:
    st.subheader("All Expenses")
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df)
    
    total = df["amount"].sum()
    st.write(f"**Total Expenses:** ₹{total}")
    
    summary = df.groupby("category")["amount"].sum().reset_index()
    st.subheader("Summary by Category")
    st.dataframe(summary)
else:
    st.info("No expenses found.")

# Option to download the file
def convert_df(df, file_format):
    if file_format == "csv":
        return df.to_csv(index=False).encode('utf-8')
    elif file_format == "json":
        return df.to_json(orient="records").encode('utf-8')
    elif file_format == "xlsx":
        with pd.ExcelWriter("temp.xlsx", engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        with open("temp.xlsx", "rb") as f:
            data = f.read()
        os.remove("temp.xlsx")
        return data

file_format = st.selectbox("Choose file format to download", ["csv", "json", "xlsx"])

if st.button("Download Expenses"):
    data = convert_df(df, file_format)
    st.download_button(label="Download file", data=data, file_name=f"expenses.{file_format}")

