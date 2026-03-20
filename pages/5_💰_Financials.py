import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from styles import apply_global_styles, sidebar_header, metric_card, section_header, warning_message
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Financial Analytics", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("💰 Financial Analytics")
st.markdown("Detailed profit and revenue analysis")
st.markdown("---")

# Date range filter
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", datetime.now())
with col3:
    st.write("")
    if st.button("🔄 Filter", use_container_width=True):
        st.rerun()

# Financial Overview Metrics
overview = conn.execute("""
    SELECT 
        COUNT(id) as total_bills,
        SUM(total_amount) as revenue,
        SUM(total_amount - discount) as net_revenue
    FROM bills 
    WHERE DATE(created_at) BETWEEN ? AND ?
""", (start_date, end_date)).fetchone()

total_bills = overview[0] or 0
revenue = overview[1] or 0
net_revenue = overview[2] or 0

# Calculate Profit
profit_data = conn.execute("""
    SELECT SUM((bi.price - m.cost_price) * bi.quantity) as profit
    FROM bill_items bi
    JOIN bills b ON bi.bill_id = b.id
    JOIN medicines m ON bi.medicine_id = m.id
    WHERE DATE(b.created_at) BETWEEN ? AND ?
""", (start_date, end_date)).fetchone()

profit = profit_data[0] or 0
profit_margin = (profit / revenue * 100) if revenue > 0 else 0

# Display Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Gross Revenue", f"{CURRENCY}{revenue:,.2f}")
with col2:
    st.metric("Net Revenue", f"{CURRENCY}{net_revenue:,.2f}", f"-{CURRENCY}{revenue-net_revenue:,.2f}")
with col3:
    st.metric("Net Profit", f"{CURRENCY}{profit:,.2f}", f"{profit_margin:.1f}% Margin")
with col4:
    st.metric("Total Invoices", f"{total_bills:,}")

st.markdown("---")

# Tabs for detailed analysis
tab1, tab2, tab3 = st.tabs(["📊 Revenue & Profit", "💳 Payment Methods", "📈 Detailed Reports"])

with tab1:
    section_header("Revenue vs Profit Trend", "📈")
    
    # Daily trend data
    trend_df = pd.read_sql_query("""
        SELECT 
            DATE(b.created_at) as date,
            SUM(b.total_amount) as revenue,
            SUM((bi.price - m.cost_price) * bi.quantity) as profit
        FROM bills b
        JOIN bill_items bi ON b.id = bi.bill_id
        JOIN medicines m ON bi.medicine_id = m.id
        WHERE DATE(b.created_at) BETWEEN ? AND ?
        GROUP BY DATE(b.created_at)
        ORDER BY date ASC
    """, conn, params=(start_date, end_date))
    
    if not trend_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend_df['date'], y=trend_df['revenue'], name='Revenue', line=dict(color='#0066cc', width=3)))
        fig.add_trace(go.Bar(x=trend_df['date'], y=trend_df['profit'], name='Profit', marker_color='#28a745'))
        
        fig.update_layout(
            barmode='group',
            height=400,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category analysis
        st.markdown("---")
        section_header("Profit by Category", "📑")
        
        cat_df = pd.read_sql_query("""
            SELECT 
                m.category as Category,
                SUM(bi.quantity * bi.price) as Revenue,
                SUM((bi.price - m.cost_price) * bi.quantity) as Profit
            FROM bill_items bi
            JOIN bills b ON bi.bill_id = b.id
            JOIN medicines m ON bi.medicine_id = m.id
            WHERE DATE(b.created_at) BETWEEN ? AND ?
            GROUP BY m.category
            ORDER BY Profit DESC
        """, conn, params=(start_date, end_date))
        
        if not cat_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_rev = px.pie(cat_df, values='Revenue', names='Category', title='Revenue Distribution')
                fig_rev.update_layout(height=350)
                st.plotly_chart(fig_rev, use_container_width=True)
                
            with col2:
                fig_profit = px.pie(cat_df, values='Profit', names='Category', title='Profit Distribution')
                fig_profit.update_layout(height=350)
                st.plotly_chart(fig_profit, use_container_width=True)
                
            st.dataframe(cat_df.sort_values('Profit', ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("No transaction data available for this period.")

with tab2:
    section_header("Payment Methods", "💳")
    
    payment_df = pd.read_sql_query("""
        SELECT 
            payment_method as Method,
            COUNT(id) as Transactions,
            SUM(total_amount) as Total_Amount
        FROM bills
        WHERE DATE(created_at) BETWEEN ? AND ? AND payment_method IS NOT NULL
        GROUP BY payment_method
        ORDER BY Total_Amount DESC
    """, conn, params=(start_date, end_date))
    
    if not payment_df.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig = px.bar(
                payment_df,
                x='Method',
                y='Total_Amount',
                color='Method',
                title="Revenue by Payment Method"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.dataframe(payment_df, use_container_width=True, hide_index=True)
            
            # Simple metric
            top_method = payment_df.iloc[0]['Method']
            top_percent = (payment_df.iloc[0]['Total_Amount'] / payment_df['Total_Amount'].sum()) * 100
            st.info(f"💡 **{top_method}** is the most popular payment method ({top_percent:.1f}% of revenue)")
    else:
        st.info("No payment method data recorded.")

with tab3:
    section_header("Top Performing Items", "⭐")
    
    top_df = pd.read_sql_query("""
        SELECT 
            m.name as Medicine,
            m.category as Category,
            SUM(bi.quantity) as Qty_Sold,
            SUM(bi.quantity * bi.price) as Revenue,
            SUM((bi.price - m.cost_price) * bi.quantity) as Profit,
            ((SUM((bi.price - m.cost_price) * bi.quantity) / NULLIF(SUM(bi.quantity * bi.price), 0)) * 100) as Margin_Pct
        FROM bill_items bi
        JOIN bills b ON bi.bill_id = b.id
        JOIN medicines m ON bi.medicine_id = m.id
        WHERE DATE(b.created_at) BETWEEN ? AND ?
        GROUP BY m.id
        ORDER BY Profit DESC
        LIMIT 15
    """, conn, params=(start_date, end_date))
    
    if not top_df.empty:
        # Format columns
        top_df['Margin_Pct'] = top_df['Margin_Pct'].round(1)
        
        fig = px.scatter(
            top_df, 
            x="Qty_Sold", 
            y="Profit", 
            size="Revenue", 
            color="Category",
            hover_name="Medicine",
            title="Item Performance Matrix"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(top_df, use_container_width=True, hide_index=True)
    else:
        st.info("No data available to generate item reports.")
        
    st.markdown("---")
    section_header("Discount Analysis", "🏷️")
    
    discount_df = pd.read_sql_query("""
        SELECT 
            DATE(created_at) as Date,
            COUNT(id) as Bills_With_Discount,
            SUM(discount) as Total_Discount_Given
        FROM bills
        WHERE discount > 0 AND DATE(created_at) BETWEEN ? AND ?
        GROUP BY DATE(created_at)
        ORDER BY Date ASC
    """, conn, params=(start_date, end_date))
    
    if not discount_df.empty:
        total_discount = discount_df['Total_Discount_Given'].sum()
        bills_discounted = discount_df['Bills_With_Discount'].sum()
        
        st.warning(f"Total Discounts Given: {CURRENCY}{total_discount:,.2f} across {bills_discounted} bills.")
        
        st.dataframe(discount_df, use_container_width=True, hide_index=True)
    else:
        st.success("No discounts were given during this period.")

st.markdown("---")
st.markdown("*Financial Analysis Dashboard - Pharmacy Management System*")

conn.close()
