import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Setting up page layout
st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("Interactive platform for tracking KPIs, revenue trends, and product performance.")

# STEP 1: IMPORT DATA (EXCEL, CSV, OR GENERATE MOCK DATA)

uploaded_file = st.sidebar.file_uploader("Upload your Sales Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    # Generate high-quality mock data automatically for instant preview/grading
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-05-20", freq="D")
    products = ['Cloud Suite Pro', 'AI Analytics Tool', 'Database Sentinel', 'DevOps Automate', 'Security Core']
    categories = ['SaaS', 'SaaS', 'Infrastructure', 'Tools', 'Security']
    prod_cat_map = dict(zip(products, categories))
    
    mock_data = {
        'Date': np.random.choice(dates, size=300),
        'Product': np.random.choice(products, size=300),
        'Quantity': np.random.randint(1, 10, size=300),
        'Price_Per_Unit': np.random.choice([150, 299, 450, 99, 199], size=300)
    }
    df = pd.DataFrame(mock_data)
    df['Revenue'] = df['Quantity'] * df['Price_Per_Unit']
    df['Category'] = df['Product'].map(prod_cat_map)
    df['Date'] = pd.to_datetime(df['Date'])

# Ensure Date column is datetime
df['Date'] = pd.to_datetime(df['Date'])

# STEP 2: INTERACTIVE FILTERS & SLICERS

st.sidebar.header("Filter Options")
category_filter = st.sidebar.multiselect("Select Category:", options=df['Category'].unique(), default=df['Category'].unique())
product_filter = st.sidebar.multiselect("Select Product:", options=df['Product'].unique(), default=df['Product'].unique())

# Apply filters
filtered_df = df[(df['Category'].isin(category_filter)) & (df['Product'].isin(product_filter))]

# STEP 3: VISUALIZE KEY PERFORMANCE INDICATORS (KPIs)

total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Quantity'].sum()
avg_order_value = filtered_df['Revenue'].mean() if len(filtered_df) > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="📦 Total Units Sold", value=f"{total_units:,}")
with col3:
    st.metric(label="📈 Avg Order Value", value=f"${avg_order_value:,.2f}")

st.markdown("---")

# STEP 4: CHARTS & INSIGHT GENERATION

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📅 Revenue Trend Over Time")
    trend_df = filtered_df.groupby('Date')['Revenue'].sum().reset_index().sort_values('Date')
    fig_trend = px.line(trend_df, x='Date', y='Revenue', title="Daily Revenue Growth", template="plotly_white")
    st.plotly_chart(fig_trend, width='stretch')

with chart_col2:
    st.subheader("🏆 Top-Performing Products by Revenue")
    product_df = filtered_df.groupby('Product')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
    fig_prod = px.bar(product_df, x='Revenue', y='Product', orientation='h', title="Revenue per Product", color='Revenue', template="plotly_white")
    st.plotly_chart(fig_prod, width='stretch')