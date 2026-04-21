import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invisible Hair Franchising Model", layout="wide")

st.title("Invisible Hair Franchising Model")

# Sidebar Inputs
st.sidebar.header("Inputs")

store_size = st.sidebar.number_input("Store Size (m2)", value=150.0)
rent_per_m2 = st.sidebar.number_input("Rent per m2 ($)", value=20.0)
decoration_per_m2 = st.sidebar.number_input("Decoration per m2 ($)", value=350.0)

sale_price = st.sidebar.number_input("Average Sale Price ($)", value=3000.0)
cost_price = st.sidebar.number_input("Average Cost ($)", value=1250.0)
monthly_units = st.sidebar.number_input("Monthly Units Sold", value=20.0)

personnel_cost = st.sidebar.number_input("Personnel + Other ($)", value=7000.0)
franchise_fee = st.sidebar.number_input("Franchise Fee ($)", value=40000.0)

# Calculations
monthly_revenue = sale_price * monthly_units
monthly_cost = cost_price * monthly_units
monthly_rent = store_size * rent_per_m2
monthly_profit = monthly_revenue - monthly_cost - monthly_rent - personnel_cost

decoration_total = store_size * decoration_per_m2
total_investment = decoration_total + franchise_fee

payback = total_investment / monthly_profit if monthly_profit > 0 else 0

# Display
col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Revenue", f"${monthly_revenue:,.0f}")
col2.metric("Monthly Profit", f"${monthly_profit:,.0f}")
col3.metric("Total Investment", f"${total_investment:,.0f}")
col4.metric("Payback (Months)", f"{payback:,.1f}")

st.divider()

# Table
df = pd.DataFrame({
    "Metric": ["Revenue", "Cost", "Rent", "Personnel", "Profit"],
    "Value": [monthly_revenue, monthly_cost, monthly_rent, personnel_cost, monthly_profit]
})

st.dataframe(df)
