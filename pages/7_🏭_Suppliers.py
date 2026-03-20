import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from styles import apply_global_styles, sidebar_header, success_message, error_message, section_header, warning_message
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Supplier Management", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("🏭 Supplier Management")
st.markdown("Manage suppliers and purchase orders")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 View Suppliers", "➕ Add Supplier", "📦 Purchase Orders"])

# Tab 1: View Suppliers
with tab1:
    section_header("Active Suppliers", "🏭")
    
    suppliers = conn.execute("SELECT id, name, contact_person, phone, email, address, created_at FROM suppliers").fetchall()
    
    if suppliers:
        df = pd.DataFrame(
            suppliers,
            columns=["ID", "Name", "Contact Person", "Phone", "Email", "Address", "Created At"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No suppliers found. Add your first supplier to get started.")

# Tab 2: Add Supplier
with tab2:
    section_header("Register New Supplier", "➕")
    
    with st.form("add_supplier_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Company Name *", placeholder="e.g., PharmaCorp Inc.")
            contact = st.text_input("Contact Person", placeholder="e.g., Jane Smith")
            phone = st.text_input("Phone Number *", placeholder="e.g., +1-234-567-8900")
            
        with col2:
            email = st.text_input("Email Address", placeholder="e.g., sales@pharmacorp.com")
            address = st.text_area("Physical Address", placeholder="Full business address...")
            
        submit = st.form_submit_button("✅ Add Supplier", use_container_width=True)
        
        if submit:
            if not name or not phone:
                error_message("Company Name and Phone are required fields.")
            else:
                try:
                    conn.execute("""
                        INSERT INTO suppliers (name, contact_person, phone, email, address)
                        VALUES (?, ?, ?, ?, ?)
                    """, (name, contact, phone, email, address))
                    conn.commit()
                    success_message(f"✅ Supplier '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    error_message(f"Error adding supplier: {str(e)}")

# Tab 3: Purchase Orders
with tab3:
    section_header("Purchase Order Generator", "📄")
    
    suppliers_list = conn.execute("SELECT id, name FROM suppliers ORDER BY name ASC").fetchall()
    medicines_list = conn.execute("SELECT id, name, cost_price, quantity FROM medicines ORDER BY name ASC").fetchall()
    
    if not suppliers_list:
        st.warning("Please add at least one supplier first.")
    elif not medicines_list:
        st.warning("Please add at least one medicine to the inventory first.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Simple PO generation UI
            with st.form("create_po_form"):
                supplier = st.selectbox("Select Supplier", suppliers_list, format_func=lambda x: x[1])
                medicine = st.selectbox("Select Medicine to Order", medicines_list, format_func=lambda x: f"{x[1]} (Stock: {x[3]})")
                
                order_qty = st.number_input("Order Quantity", min_value=1, step=10, value=50)
                expected_cost = order_qty * (medicine[2] or 0)
                
                st.info(f"Estimated Cost: **{CURRENCY}{expected_cost:,.2f}**")
                
                if st.form_submit_button("✅ Create Order", use_container_width=True):
                    # For a real system, we'd save this to a `purchase_orders` table
                    # Here we just show a success message as a proof of concept
                    success_message(f"Purchase Order created for {order_qty} units of {medicine[1]} from {supplier[1]}.")
        
        with col2:
            st.markdown("### 📊 Recommended Restocks")
            low_stock = pd.read_sql_query("""
                SELECT name as 'Medicine', quantity as 'Current Stock', (100 - quantity) as 'Suggested Order'
                FROM medicines
                WHERE quantity < 50
                ORDER BY quantity ASC
                LIMIT 5
            """, conn)
            
            if not low_stock.empty:
                st.dataframe(low_stock, use_container_width=True, hide_index=True)
            else:
                st.success("All medicines are well stocked!")

st.markdown("---")
st.markdown("*Supplier relationship management module*")

conn.close()
