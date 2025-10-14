# app.py
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Sales Overview")

df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
avg_discount = df['Discount'].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", total_orders)
col4.metric("Avg. Discount", f"{avg_discount:.2f}%")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
regions = st.sidebar.multiselect("Select Region:", df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category:", df['Category'].unique(), default=df['Category'].unique())

df_filtered = df[(df['Region'].isin(regions)) & (df['Category'].isin(categories))]

# Visualizations
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(4, 2, figsize=(16, 20))

# Sales by Category
cat_sales = df_filtered.groupby('Category')['Sales'].sum()
axes[0,0].bar(cat_sales.index, cat_sales.values, color='skyblue')
axes[0,0].set_title('Sales by Category')

# Profit by Sub-Category
sub_profit = df_filtered.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).head(10)
axes[0,1].barh(sub_profit.index, sub_profit.values, color='lightgreen')
axes[0,1].set_title('Top 10 Sub-Categories by Profit')

# Monthly Sales Trend
monthly = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M'))['Sales'].sum()
monthly.index = monthly.index.to_timestamp()
axes[1,0].plot(monthly.index, monthly.values, marker='o', color='orange')
axes[1,0].set_title('Monthly Sales Trend')

# Sales by Region
reg_sales = df_filtered.groupby('Region')['Sales'].sum()
axes[1,1].bar(reg_sales.index, reg_sales.values, color='teal')
axes[1,1].set_title('Sales by Region')

# Top States
state_sales = df_filtered.groupby('State')['Sales'].sum().nlargest(10)
axes[2,0].barh(state_sales.index, state_sales.values, color='gold')
axes[2,0].invert_yaxis()
axes[2,0].set_title('Top 10 States by Sales')

# Discount vs Profit
axes[2,1].scatter(df_filtered['Discount'], df_filtered['Profit'], alpha=0.5, color='purple')
axes[2,1].set_title('Discount vs Profit')

# Ship Mode Distribution
ship = df_filtered['Ship Mode'].value_counts()
axes[3,0].pie(ship.values, labels=ship.index, autopct='%1.1f%%')
axes[3,0].set_title('Ship Mode Distribution')

# Sales vs Profit
axes[3,1].scatter(df_filtered['Sales'], df_filtered['Profit'], alpha=0.5, color='crimson')
axes[3,1].set_title('Sales vs Profit')

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")
st.caption("Developed using Streamlit + Matplotlib | Dataset: Superstore Sales")
