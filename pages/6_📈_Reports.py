import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from styles import apply_global_styles, sidebar_header, section_header
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Analytics Reports", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("📈 Detailed Analytics Reports")
st.markdown("Exportable data views and deep insights")
st.markdown("---")

col1, col2 = st.columns([4, 1])
with col1:
    report_type = st.selectbox(
        "Select Report Type",
        ["Sales Summary", "Inventory Status", "Top Products", "Customer Trends"]
    )
with col2:
    st.write("")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.markdown("---")

if report_type == "Inventory Status":
    section_header("Current Inventory Status", "📦")
    
    df_inv = pd.read_sql_query("""
        SELECT 
            name as 'Medicine Name',
            category as Category,
            quantity as 'Stock Quantity',
            price as 'Unit Price',
            cost_price as 'Unit Cost',
            expiry_date as 'Expiry Date'
        FROM medicines
        ORDER BY quantity ASC
    """, conn)
    
    if not df_inv.empty:
        # Calculate totals
        total_val = (df_inv['Stock Quantity'] * df_inv['Unit Price']).sum()
        total_cost = (df_inv['Stock Quantity'] * df_inv['Unit Cost']).sum()
        
        col1, col2, col3 = st.columns(3)
        st.metric("Total Items", len(df_inv))
        st.metric("Total Value", f"{CURRENCY}{total_val:,.2f}")
        st.metric("Total Cost", f"{CURRENCY}{total_cost:,.2f}")
        
        # Display data
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Distribution by Category
            cat_dist = df_inv.groupby('Category')['Stock Quantity'].sum().reset_index()
            fig_qty = px.pie(cat_dist, values='Stock Quantity', names='Category', title='Stock Distribution by Category')
            st.plotly_chart(fig_qty, use_container_width=True)
            
        with col2:
            # Value by Category
            df_inv['Value'] = df_inv['Stock Quantity'] * df_inv['Unit Price']
            val_dist = df_inv.groupby('Category')['Value'].sum().reset_index()
            fig_value = px.pie(val_dist, values='Value', names='Category', title='Value Distribution by Category')
            st.plotly_chart(fig_value, use_container_width=True)
            
        # Full table
        st.dataframe(df_inv, use_container_width=True, hide_index=True)
        
        # Low stock table
        st.markdown("### ⚠️ Critical Low Stock (Below 20 units)")
        low_stock = df_inv[df_inv['Stock Quantity'] < 20]
        st.dataframe(low_stock, use_container_width=True, hide_index=True)
    else:
        st.info("No inventory data found.")

elif report_type == "Sales Summary":
    section_header("Aggregated Sales Data", "📊")
    
    df_sales = pd.read_sql_query("""
        SELECT 
            DATE(b.created_at) as Date,
            COUNT(DISTINCT b.id) as 'Total Bills',
            SUM(b.total_amount) as 'Total Sales',
            SUM(b.discount) as 'Total Discounts',
            SUM(bi.quantity) as 'Items Sold'
        FROM bills b
        JOIN bill_items bi ON b.id = bi.bill_id
        GROUP BY DATE(b.created_at)
        ORDER BY Date DESC
    """, conn)
    
    if not df_sales.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_trend = px.line(df_sales, x='Date', y='Total Sales', title='Daily Sales Trend')
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with col2:
            fig_bills = px.bar(df_sales, x='Date', y='Total Bills', title='Daily Transaction Volume')
            st.plotly_chart(fig_bills, use_container_width=True)
            
        st.dataframe(df_sales, use_container_width=True, hide_index=True)
        
    else:
        st.info("No sales data available.")

elif report_type == "Top Products":
    section_header("Best Selling Products", "🌟")
    
    df_top = pd.read_sql_query("""
        SELECT 
            m.name as 'Product',
            m.category as 'Category',
            SUM(bi.quantity) as 'Units Sold',
            SUM(bi.quantity * bi.price) as 'Revenue Generated'
        FROM bill_items bi
        JOIN medicines m ON bi.medicine_id = m.id
        GROUP BY m.id
        ORDER BY 'Units Sold' DESC
    """, conn)
    
    if not df_top.empty:
        st.dataframe(df_top, use_container_width=True, hide_index=True)
    else:
        st.info("No product data available.")

elif report_type == "Customer Trends":
    section_header("Customer Insights", "👥")
    
    df_cust = pd.read_sql_query("""
        SELECT 
            c.name as 'Customer',
            COUNT(b.id) as 'Total Visits',
            SUM(b.total_amount) as 'Lifetime Value',
            MAX(b.created_at) as 'Last Visit'
        FROM customers c
        JOIN bills b ON c.id = b.customer_id
        GROUP BY c.id
        ORDER BY 'Lifetime Value' DESC
    """, conn)
    
    if not df_cust.empty:
        st.dataframe(df_cust, use_container_width=True, hide_index=True)
    else:
        st.info("No customer data available.")

st.markdown("---")
st.markdown("*Reports generated in real-time*")

conn.close()
