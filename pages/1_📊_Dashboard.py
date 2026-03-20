import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import apply_global_styles, sidebar_header, metric_card, section_header, warning_message
from config import COLORS, DB_NAME, LOW_STOCK_THRESHOLD, EXPIRY_ALERT_DAYS, CURRENCY

st.set_page_config(page_title="Dashboard", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()
    # Show logged-in user
    if st.session_state.user_info:
        st.markdown("---")
        st.markdown(f"**👤 {st.session_state.user_info['full_name']}**")
        st.markdown(f"*{st.session_state.user_info['role'].title()}*")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()

conn = sqlite3.connect(DB_NAME)

st.title("📊 Dashboard")
st.markdown("Real-time pharmacy system metrics and alerts")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_meds = conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
today_sales = conn.execute("""
SELECT SUM(total_amount) FROM bills
WHERE DATE(created_at) = DATE('now')
""").fetchone()[0] or 0
low_stock = conn.execute("SELECT COUNT(*) FROM medicines WHERE quantity < ?", (LOW_STOCK_THRESHOLD,)).fetchone()[0]
expiry = conn.execute("""
SELECT COUNT(*) FROM medicines
WHERE expiry_date <= DATE('now', '+' || ? || ' days')
""", (EXPIRY_ALERT_DAYS,)).fetchone()[0]

with col1:
    st.metric(
        "💊 Total Medicines",
        f"{total_meds:,}",
        delta="In Inventory",
        delta_color="normal"
    )

with col2:
    st.metric(
        "💰 Today's Sales",
        f"{CURRENCY}{today_sales:,.0f}",
        delta=f"+{CURRENCY}0" if today_sales > 0 else f"{CURRENCY}0",
        delta_color="normal"
    )

with col3:
    col3_inner1, col3_inner2 = st.columns([2, 1])
    with col3_inner1:
        st.metric(
            "⚠️ Low Stock",
            low_stock,
            delta="Needs Order",
            delta_color="inverse" if low_stock > 0 else "normal"
        )

with col4:
    st.metric(
        "⏳ Expiring Soon",
        expiry,
        delta="Within 30 days",
        delta_color="inverse" if expiry > 0 else "normal"
    )

st.markdown("---")

# Top Section: Sales & Alerts
tab1, tab2, tab3 = st.tabs(["📈 Top Sellers", "⚠️ Stock Alerts", "⏰ Expiry Alerts"])

with tab1:
    top_df = pd.read_sql_query("""
    SELECT m.name, SUM(bi.quantity) as total_sold, SUM(bi.quantity * bi.price) as revenue
    FROM bill_items bi
    JOIN medicines m ON bi.medicine_id = m.id
    GROUP BY m.name
    ORDER BY total_sold DESC
    LIMIT 8
    """, conn)
    
    if not top_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bar = px.bar(
                top_df,
                x="name",
                y="total_sold",
                title="🔥 Top Medicines by Quantity Sold",
                labels={"name": "Medicine", "total_sold": "Units Sold"},
                color="total_sold",
                color_continuous_scale="Blues"
            )
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                hovermode="x unified",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            fig_revenue = px.pie(
                top_df,
                values="revenue",
                names="name",
                title="💹 Revenue Distribution"
            )
            fig_revenue.update_layout(height=400)
            st.plotly_chart(fig_revenue, use_container_width=True)
    else:
        st.info("No sales data available yet.")

with tab2:
    low_df = pd.read_sql_query(
        "SELECT id, name, quantity FROM medicines WHERE quantity < ? ORDER BY quantity ASC",
        conn,
        params=(LOW_STOCK_THRESHOLD,)
    )
    
    if not low_df.empty:
        st.dataframe(
            low_df.rename(columns={
                "id": "ID",
                "name": "Medicine Name",
                "quantity": "Stock Quantity"
            }),
            use_container_width=True,
            hide_index=True
        )
        warning_message(f"{len(low_df)} medicines have low stock levels. Consider placing orders.")
    else:
        st.success("✅ All medicines are well stocked!")

with tab3:
    exp_df = pd.read_sql_query(
        """SELECT id, name, expiry_date, quantity
           FROM medicines
           WHERE expiry_date IS NOT NULL AND expiry_date <= DATE('now', '+' || ? || ' days')
           ORDER BY expiry_date ASC""",
        conn,
        params=(EXPIRY_ALERT_DAYS,)
    )
    
    if not exp_df.empty:
        st.dataframe(
            exp_df.rename(columns={
                "id": "ID",
                "name": "Medicine Name",
                "expiry_date": "Expiry Date",
                "quantity": "Stock"
            }),
            use_container_width=True,
            hide_index=True
        )
        warning_message(f"{len(exp_df)} medicines will expire soon. Review expiry dates.")
    else:
        st.success("✅ No medicines expiring soon!")

st.markdown("---")

# Bottom Section: System Health
section_header("System Health", "🏥")

col1, col2, col3 = st.columns(3)

with col1:
    total_bills = conn.execute("SELECT COUNT(*) FROM bills").fetchone()[0]
    st.metric("📋 Total Transactions", f"{total_bills:,}")

with col2:
    total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    st.metric("👥 Registered Customers", f"{total_customers:,}")

with col3:
    total_stock_value = conn.execute("SELECT SUM(price * quantity) FROM medicines").fetchone()[0] or 0
    st.metric("💼 Total Inventory Value", f"{CURRENCY}{total_stock_value:,.0f}")

# Your Activity
st.markdown("---")
section_header("Your Recent Activity", "📌")

if st.session_state.user_info:
    user_id = st.session_state.user_info['id']
    recent_bills = pd.read_sql_query("""
    SELECT b.id as BillID, c.name as Customer, b.total_amount as Amount, b.created_at as Date
    FROM bills b
    LEFT JOIN customers c ON b.customer_id = c.id
    WHERE b.user_id = ?
    ORDER BY b.created_at DESC
    LIMIT 5
    """, conn, params=(user_id,))
    
    if not recent_bills.empty:
        recent_bills["Amount"] = recent_bills["Amount"].apply(lambda x: f"{CURRENCY}{x:,.2f}")
        st.dataframe(recent_bills, use_container_width=True, hide_index=True)
    else:
        st.info("No bills created yet. Start by creating your first bill!")
else:
    st.warning("User information not available")

st.markdown("---")
st.markdown("*Last updated: Real-time data*")

conn.close()
