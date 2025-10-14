# pages/1_Deep_Insights.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("📉 Deep Insights and Advanced Visuals")

df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')
df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_category = st.sidebar.multiselect(
    "Choose Category:", df['Category'].unique(), default=df['Category'].unique()
)
df_filtered = df[df['Category'].isin(selected_category)]

# --- 1️⃣ Correlation Heatmap ---
st.subheader("📊 Correlation Heatmap")
corr = df_filtered[['Sales', 'Quantity', 'Discount', 'Profit', 'Profit Margin (%)']].corr()

fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax1)
st.pyplot(fig1)

# --- 2️⃣ Category Contribution (Pie) ---
st.subheader("🥧 Sales Contribution by Category")
cat_sales = df_filtered.groupby('Category')['Sales'].sum()

fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(cat_sales.values, labels=cat_sales.index, autopct='%1.1f%%', startangle=140)
ax2.set_title("Sales Share by Category")
st.pyplot(fig2)

# --- 3️⃣ Profit Margin by Sub-Category ---
st.subheader("💰 Average Profit Margin by Sub-Category")
margin = df_filtered.groupby('Sub-Category')['Profit Margin (%)'].mean().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(x=margin.values, y=margin.index, palette="viridis", ax=ax3)
ax3.set_xlabel("Profit Margin (%)")
ax3.set_ylabel("Sub-Category")
st.pyplot(fig3)

# --- 4️⃣ Profit Margin Trend over Time ---
st.subheader("📈 Profit Margin Trend Over Time")
monthly_margin = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M'))['Profit Margin (%)'].mean()
monthly_margin.index = monthly_margin.index.to_timestamp()

fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.plot(monthly_margin.index, monthly_margin.values, marker='o', color='orange')
ax4.set_title("Monthly Profit Margin Trend")
ax4.set_ylabel("Profit Margin (%)")
st.pyplot(fig4)

st.markdown("---")
st.caption("Page 2 – Deep Analytics | Built with Streamlit, Matplotlib & Seaborn")
