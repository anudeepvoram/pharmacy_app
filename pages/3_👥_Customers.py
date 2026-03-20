import streamlit as st
import sqlite3
import pandas as pd
from styles import apply_global_styles, sidebar_header, success_message, error_message, section_header, warning_message
from config import DB_NAME

st.set_page_config(page_title="Customer Management", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("👥 Customer Management")
st.markdown("Add, view, and manage customer information")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 All Customers", "➕ Add Customer", "✏️ Manage Customers"])

# Tab 1: View All Customers
with tab1:
    customers = conn.execute("SELECT * FROM customers").fetchall()
    
    if customers:
        df = pd.DataFrame(
            customers,
            columns=["ID", "Name", "Phone", "Email", "Address", "City", "Created At"]
        )
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search = st.text_input(
                "🔍 Search customers",
                placeholder="Search by name, phone, or email..."
            )
            if search:
                df = df[
                    df["Name"].str.contains(search, case=False, na=False) |
                    df["Phone"].str.contains(search, case=False, na=False) |
                    df["Email"].str.contains(search, case=False, na=False)
                ]
        
        with col2:
            st.metric("Total", len(df))
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(width="small"),
                "Email": st.column_config.Column(width="medium")
            }
        )
    else:
        st.info("No customers yet. Add your first customer to get started!")

# Tab 2: Add New Customer
with tab2:
    section_header("Add New Customer", "➕")
    
    with st.form("add_customer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name *",
                placeholder="e.g., John Doe",
                key="cust_name"
            )
            phone = st.text_input(
                "Phone Number *",
                placeholder="e.g., +91-9876543210",
                key="cust_phone"
            )
        
        with col2:
            email = st.text_input(
                "Email Address",
                placeholder="e.g., john@example.com",
                key="cust_email"
            )
            st.write("")  # Spacer
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submit = st.form_submit_button("✅ Add Customer", use_container_width=True)
        
        if submit:
            if not name or not phone:
                error_message("Name and Phone number are required fields.")
            elif len(name.strip()) < 2:
                error_message("Please enter a valid name.")
            elif len(phone.strip()) < 7:
                error_message("Please enter a valid phone number.")
            else:
                try:
                    conn.execute(
                        "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
                        (name.strip(), phone.strip(), email.strip() if email else None)
                    )
                    conn.commit()
                    success_message(f"✅ Customer '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    error_message(f"Error adding customer: {str(e)}")

# Tab 3: Manage Customers
with tab3:
    section_header("Edit or Delete Customer", "✏️")
    
    customers = conn.execute("SELECT id, name, phone, email FROM customers ORDER BY name ASC").fetchall()
    
    if customers:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_cust = st.selectbox(
                "Select Customer",
                customers,
                format_func=lambda x: f"{x[1]} - {x[2]}",
                key="manage_select"
            )
        
        with col2:
            action = st.selectbox(
                "Action",
                ["View", "Edit", "Delete"],
                key="manage_action"
            )
        
        if selected_cust:
            cust_id, cust_name, cust_phone, cust_email = selected_cust
            
            if action == "View":
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Name**")
                    st.write(cust_name)
                    st.markdown("**Phone**")
                    st.write(cust_phone)
                
                with col2:
                    st.markdown("**Email**")
                    st.write(cust_email or "Not provided")
                    
                    # Get customer transaction count
                    tx_count = conn.execute(
                        "SELECT COUNT(*) FROM bills WHERE customer_id = ?",
                        (cust_id,)
                    ).fetchone()[0]
                    st.markdown("**Transactions**")
                    st.write(f"{tx_count} bill(s)")
            
            elif action == "Edit":
                st.markdown("---")
                with st.form("edit_customer_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input(
                            "Full Name",
                            value=cust_name,
                            key="edit_name"
                        )
                        new_phone = st.text_input(
                            "Phone Number",
                            value=cust_phone,
                            key="edit_phone"
                        )
                    
                    with col2:
                        new_email = st.text_input(
                            "Email Address",
                            value=cust_email or "",
                            key="edit_email"
                        )
                        st.write("")  # Spacer
                    
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        if not new_name or not new_phone:
                            error_message("Name and Phone are required.")
                        else:
                            try:
                                conn.execute(
                                    "UPDATE customers SET name = ?, phone = ?, email = ? WHERE id = ?",
                                    (new_name, new_phone, new_email or None, cust_id)
                                )
                                conn.commit()
                                success_message("✅ Customer updated successfully!")
                                st.rerun()
                            except Exception as e:
                                error_message(f"Error: {str(e)}")
            
            elif action == "Delete":
                st.markdown("---")
                st.warning("⚠️ Deleting a customer will not affect their billing history.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑️ Delete Customer", use_container_width=True):
                        try:
                            conn.execute("DELETE FROM customers WHERE id = ?", (cust_id,))
                            conn.commit()
                            success_message(f"Customer '{cust_name}' deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            error_message(f"Error: {str(e)}")
    else:
        st.info("No customers to manage. Add customers first!")

st.markdown("---")
st.markdown("*Customer Management System - Professional Interface*")

conn.close()
