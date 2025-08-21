#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 📌 Expense Tracker
# ==============================

# Initialize CSV file
try:
    df = pd.read_csv("expenses.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv("expenses.csv", index=False)

# ------------------------------
# Add New Expense
# ------------------------------
date = input("Enter date (YYYY-MM-DD): ")
category = input("Enter category (Food, Travel, Rent, etc.): ")

# ✅ Input validation for amount
while True:
    try:
        amount = float(input("Enter amount: "))
        break
    except ValueError:
        print("❌ Invalid input! Please enter a number.")

# Save to DataFrame
new_data = pd.DataFrame([[date, category, amount]], 
                        columns=["Date", "Category", "Amount"])
df = pd.concat([df, new_data], ignore_index=True)
df.to_csv("expenses.csv", index=False)

print("\n✅ Expense Added Successfully!\n")

# ------------------------------
# Monthly Summary Option
# ------------------------------
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # convert to datetime

choice = input("Do you want to see a monthly summary? (y/n): ").lower()

if choice == "y":
    year = int(input("Enter year (e.g. 2025): "))
    month = int(input("Enter month (1-12): "))

    # Filter by month & year
    monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    summary = monthly_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    print(f"\n📅 Monthly Summary for {year}-{month:02d}:\n")
else:
    # Show all data
    summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    print("📊 Overall Spending Summary:\n")

print(summary)

# ------------------------------
# Visualization
# ------------------------------
if not summary.empty:
    # ---- Pie Chart ----
    plt.figure(figsize=(7,7))
    explode = [0.05 if x < summary.sum()*0.05 else 0 for x in summary]  # explode small slices
    plt.pie(summary,
            labels=summary.index,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            shadow=True)
    plt.title("💰 Spending by Category", fontsize=14)
    plt.legend(title="Categories", loc="upper right")
    plt.show()

    # ---- Bar Chart ----
    plt.figure(figsize=(8,5))
    summary.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("📈 Spending by Category", fontsize=14)
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("⚠ No data available for the selected period.")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ==============================
# 📌 Expense Tracker (Streamlit)
# ==============================

# Load data
try:
    df = pd.read_csv("expenses.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv("expenses.csv", index=False)

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Personal Expense Tracker")

# ------------------------------
# Add New Expense (Form)
# ------------------------------
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.text_input("Category (Food, Travel, Rent, etc.)")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if category.strip() == "" or amount <= 0:
            st.error("⚠ Please enter a valid category and amount.")
        else:
            new_data = pd.DataFrame([[date, category, amount]],
                                    columns=["Date", "Category", "Amount"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("expenses.csv", index=False)
            st.success("✅ Expense Added Successfully!")

# ------------------------------
# Monthly / Overall Summary
# ------------------------------
st.subheader("📊 View Summary")

option = st.radio("Choose view:", ["Overall", "Monthly"])

if option == "Monthly":
    year = st.number_input("Enter Year", min_value=2000, max_value=2100, value=pd.Timestamp.today().year)
    month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=pd.Timestamp.today().month)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    filtered_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    summary = filtered_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.write(f"📅 Summary for **{year}-{month:02d}**")
else:
    summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.write("📊 Overall Spending Summary")

st.dataframe(summary)

# ------------------------------
# Charts
# ------------------------------
if not summary.empty:
    # Bar Chart
    st.bar_chart(summary)

    # Pie Chart
    fig, ax = plt.subplots(figsize=(6,6))
    explode = [0.05 if x < summary.sum()*0.05 else 0 for x in summary]
    ax.pie(summary, labels=summary.index, autopct='%1.1f%%',
           startangle=140, explode=explode, shadow=True)
    ax.set_title("Spending by Category")
    st.pyplot(fig)
else:
    st.warning("⚠ No data available for the selected period.")

