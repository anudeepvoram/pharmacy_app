import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from styles import apply_global_styles, sidebar_header, success_message, error_message, section_header, warning_message
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Promotions & Offers", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("🎯 Promotions & Offers")
st.markdown("Manage discount coupons and special promotional offers")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🎟️ Coupons", "🎁 Special Offers", "📊 Usage Stats"])

# Tab 1: Coupons
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        section_header("Active Coupons", "🎟️")
        coupons = conn.execute("SELECT id, code, discount_type, discount_value, max_usage, current_usage, is_active, created_at FROM coupons ORDER BY created_at DESC").fetchall()
        
        if coupons:
            df_coupons = pd.DataFrame(
                coupons,
                columns=["ID", "Code", "Type", "Value", "Max Usage", "Current Usage", "Active", "Created"]
            )
            # Format value column based on type
            df_coupons["Value"] = df_coupons.apply(
                lambda row: f"{row['Value']}%" if row['Type'] == 'percentage' else f"{CURRENCY}{row['Value']}",
                axis=1
            )
            
            # Status indicator
            df_coupons["Status"] = df_coupons.apply(
                lambda row: "🟢 Active" if row["Active"] == 1 and row["Current Usage"] < row["Max Usage"] else "🔴 Exhausted/Inactive",
                axis=1
            )
            
            display_cols = ["Code", "Value", "Current Usage", "Max Usage", "Status"]
            st.dataframe(df_coupons[display_cols], use_container_width=True, hide_index=True)
        else:
            st.info("No coupons found. Create one to get started!")

    with col2:
        section_header("Create New Coupon", "➕")
        with st.form("create_coupon"):
            code = st.text_input("Coupon Code *", placeholder="e.g., SUMMER20")
            
            c1, c2 = st.columns(2)
            with c1:
                discount_type = st.selectbox("Discount Type", ["percentage", "fixed"])
            with c2:
                discount_value = st.number_input("Value *", min_value=1.0, step=1.0)
            
            max_uses = st.number_input("Maximum allowed uses", min_value=1, value=100)
            
            submit = st.form_submit_button("✅ Create Coupon", use_container_width=True)
            
            if submit:
                if not code or discount_value <= 0:
                    error_message("Please provide a valid code and value.")
                else:
                    try:
                        # Check if code exists
                        exists = conn.execute("SELECT 1 FROM coupons WHERE code = ?", (code.upper(),)).fetchone()
                        if exists:
                            error_message(f"Coupon code '{code.upper()}' already exists!")
                        else:
                            conn.execute("""
                                INSERT INTO coupons (code, discount_type, discount_value, max_usage)
                                VALUES (?, ?, ?, ?)
                            """, (code.upper(), discount_type, discount_value, max_uses))
                            conn.commit()
                            success_message(f"✅ Coupon '{code.upper()}' created successfully!")
                            st.rerun()
                    except Exception as e:
                        error_message(f"Database error: {str(e)}")

# Tab 2: Special Offers (Medicines)
with tab2:
    section_header("Medicine Offers", "🎁")
    
    # In a real app, this would be a separate table linking medicines to specific discounts
    # For this dashboard, we simulate an offers table feature
    st.info("Creating seasonal sales or bulk discounts on specific medicines")
    
    medicines = conn.execute("SELECT id, name, price, quantity FROM medicines ORDER BY name ASC").fetchall()
    
    if medicines:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("create_offer"):
                med_id = st.selectbox("Select Medicine", medicines, format_func=lambda x: f"{x[1]} ({CURRENCY}{x[2]})")
                discount = st.number_input(f"Discount Amount ({CURRENCY})", min_value=0.5, step=0.5)
                valid_until = st.date_input("Valid Until")
                
                if st.form_submit_button("✅ Create Offer", use_container_width=True):
                    # We would save this to an `offers` table in a full implementation
                    # Temporary mock implementation
                    success_message(f"Offer created: {CURRENCY}{discount} off on {med_id[1]} until {valid_until}")
        
        with col2:
            st.markdown("### Current Active Offers")
            st.caption("Mock data for demonstration")
            
            mock_offers = pd.DataFrame([
                {"Medicine": "Paracetamol 500mg", "Discount": f"{CURRENCY}5.00 off", "Expires": "2023-12-31", "Status": "🔥 Active"},
                {"Medicine": "Vitamin C Gummies", "Discount": "Buy 1 Get 1", "Expires": "2023-11-30", "Status": "🔥 Active"}
            ])
            st.dataframe(mock_offers, use_container_width=True, hide_index=True)
    else:
        st.warning("Please add medicines to inventory before creating offers.")

# Tab 3: Usage Stats
with tab3:
    section_header("Promotion Analytics", "📊")
    
    # Get total discounts given from bills table
    stats = conn.execute("""
        SELECT 
            COUNT(id) as total_discounted_bills,
            SUM(discount) as total_discount_amount
        FROM bills
        WHERE discount > 0
    """).fetchone()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Discounted Transactions", stats[0] or 0)
    with col2:
        st.metric("Total Promotional Value Given", f"{CURRENCY}{(stats[1] or 0):,.2f}")
    
    st.markdown("---")
    st.caption("Monitor how discounts affect your profit margins in the Financials tab.")

st.markdown("---")
st.markdown("*Promotions and Campaign Management*")

conn.close()
