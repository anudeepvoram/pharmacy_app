import streamlit as st
import sqlite3
import pandas as pd
from styles import apply_global_styles, sidebar_header, success_message, error_message, section_header
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Medicine Management", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("💊 Medicine Management")
st.markdown("Add, edit, and manage medicine inventory")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Inventory", "➕ Add Medicine", "✏️ Update/Delete", "🗑️ Expired"])

# Tab 1: View Inventory
with tab1:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search = st.text_input(
            "🔍 Search medicines",
            placeholder="Type medicine name or category..."
        )
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Name", "Price", "Quantity", "Expiry Date"])
    
    query = "SELECT id, name, category, price, quantity, expiry_date FROM medicines WHERE name LIKE ? OR category LIKE ?"
    data = conn.execute(query, (f"%{search}%", f"%{search}%")).fetchall()
    
    if data:
        df = pd.DataFrame(
            data,
            columns=["ID", "Medicine Name", "Category", f"Price ({CURRENCY})", "Stock Qty", "Expiry Date"]
        )
        
        # Sort based on selection
        if sort_by == "Price":
            df = df.sort_values("Price (₹)", ascending=False)
        elif sort_by == "Quantity":
            df = df.sort_values("Stock Qty", ascending=True)
        elif sort_by == "Expiry Date":
            df = df.sort_values("Expiry Date", ascending=True)
        else:
            df = df.sort_values("Medicine Name")
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(width="small"),
                "Stock Qty": st.column_config.NumberColumn(format="%d"),
            }
        )
        
        st.markdown(f"**Total Medicines:** {len(df)} | **Total Inventory Value:** {CURRENCY}{(df['Price (₹)'] * df['Stock Qty']).sum():,.0f}")
    else:
        st.info("No medicines found. Add some to get started!")

# Tab 2: Add Medicine
with tab2:
    section_header("Add New Medicine", "➕")
    
    with st.form("add_medicine_form"):
        col1, col2 = st.columns(2)
        
    with col1:
        name = st.text_input(
            "Medicine Name *",
            placeholder="e.g., Aspirin",
            key="med_name"
        )
        price = st.number_input(
            f"Selling Price ({CURRENCY}) *",
            min_value=0.0,
            step=0.01,
            key="med_price"
        )
        cost_price = st.number_input(
            f"Cost Price ({CURRENCY})",
            min_value=0.0,
            step=0.01,
            key="med_cost"
        )
        
        with col2:
            category = st.selectbox(
                "Category *",
                ["Painkillers", "Antibiotics", "Vitamins", "Supplements", "Cold & Flu", "Digestive", "Other"],
                key="med_category"
            )
            quantity = st.number_input(
                "Initial Stock *",
                min_value=0,
                step=1,
                key="med_qty"
            )
            wholesale_price = st.number_input(
                f"Wholesale Price ({CURRENCY})",
                min_value=0.0,
                step=0.01,
                key="med_wholesale"
            )
            
        expiry = st.date_input(
            "Expiry Date *",
            key="med_expiry"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submit = st.form_submit_button("✅ Add Medicine", use_container_width=True)
        
        if submit:
            if not name or not category or price <= 0 or quantity < 0:
                error_message("Please fill all required fields with valid values.")
            else:
                try:
                    conn.execute(
                        "INSERT INTO medicines (name, category, price, cost_price, wholesale_price, quantity, expiry_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (name, category, price, cost_price, wholesale_price, quantity, str(expiry))
                    )
                    conn.commit()
                    success_message(f"✅ Medicine '{name}' added successfully! Profit margin: {CURRENCY}{price - cost_price:.2f}")
                    st.rerun()
                except Exception as e:
                    error_message(f"Error adding medicine: {str(e)}")

# Tab 3: Update/Delete
with tab3:
    section_header("Update or Delete Medicine", "✏️")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        med_id = st.number_input("Medicine ID", min_value=1, step=1, key="update_id")
    
    with col2:
        action = st.selectbox("Action", ["Update Price", "Update Stock", "Delete Medicine"])
    
    with col3:
        st.write("")  # Spacer
    
    # Fetch current medicine details
    med_details = conn.execute("SELECT name, price, quantity FROM medicines WHERE id = ?", (med_id,)).fetchone()
    
    if med_details:
        st.info(f"Current: **{med_details[0]}** | Price: {CURRENCY}{med_details[1]} | Stock: {med_details[2]}")
        
        col1, col2 = st.columns(2)
        
        if action == "Update Price":
            with col1:
                new_price = st.number_input(
                    f"New Price ({CURRENCY})",
                    min_value=0.0,
                    step=0.01,
                    value=float(med_details[1])
                )
            with col2:
                if st.button("💾 Update Price", use_container_width=True):
                    try:
                        conn.execute("UPDATE medicines SET price = ? WHERE id = ?", (new_price, med_id))
                        conn.commit()
                        success_message(f"Price updated to {CURRENCY}{new_price}")
                        st.rerun()
                    except Exception as e:
                        error_message(f"Error: {str(e)}")
        
        elif action == "Update Stock":
            with col1:
                new_qty = st.number_input(
                    "New Stock Quantity",
                    min_value=0,
                    step=1,
                    value=int(med_details[2])
                )
            with col2:
                if st.button("💾 Update Stock", use_container_width=True):
                    try:
                        conn.execute("UPDATE medicines SET quantity = ? WHERE id = ?", (new_qty, med_id))
                        conn.commit()
                        success_message(f"Stock updated to {new_qty} units")
                        st.rerun()
                    except Exception as e:
                        error_message(f"Error: {str(e)}")
        
        elif action == "Delete Medicine":
            st.warning("⚠️ This action cannot be undone!")
            if st.button("🗑️ Delete Medicine", use_container_width=True):
                try:
                    med_name = med_details[0]
                    conn.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
                    conn.commit()
                    success_message(f"Medicine '{med_name}' deleted successfully")
                    st.rerun()
                except Exception as e:
                    error_message(f"Error: {str(e)}")
    else:
        st.warning("No medicine found with this ID. Please check and try again.")

# Tab 4: Expired Medicines
with tab4:
    section_header("Manage Expired Medicines", "🗑️")
    
    expired_meds = conn.execute("""
    SELECT id, name, category, quantity, expiry_date
    FROM medicines
    WHERE expiry_date < date('now') AND quantity > 0
    ORDER BY expiry_date ASC
    """).fetchall()
    
    if expired_meds:
        df_expired = pd.DataFrame(
            expired_meds,
            columns=["ID", "Medicine Name", "Category", "Stock", "Expiry Date"]
        )
        
        st.warning(f"⚠️ Found {len(df_expired)} expired medicines!")
        st.dataframe(df_expired, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_id = st.selectbox(
                "Select medicine to delete",
                options=[m[0] for m in expired_meds],
                format_func=lambda x: next((m[1] for m in expired_meds if m[0] == x), "")
            )
        
        with col2:
            if st.button("🗑️ Delete Selected Expired Medicine", use_container_width=True):
                try:
                    med_name = next((m[1] for m in expired_meds if m[0] == selected_id), "Unknown")
                    conn.execute("DELETE FROM medicines WHERE id = ?", (selected_id,))
                    conn.commit()
                    success_message(f"✅ Expired medicine '{med_name}' removed from inventory!")
                    st.rerun()
                except Exception as e:
                    error_message(f"Error deleting medicine: {str(e)}")
        
        st.markdown("---")
        if st.button("🗑️ Delete ALL Expired Medicines (Bulk Action)", use_container_width=True):
            try:
                count = len(expired_meds)
                conn.execute("DELETE FROM medicines WHERE expiry_date < date('now')")
                conn.commit()
                success_message(f"✅ Deleted {count} expired medicines!")
                st.rerun()
            except Exception as e:
                error_message(f"Error: {str(e)}")
    else:
        st.success("✅ No expired medicines in inventory. Great job!")
        
        # Show upcoming expiry (within 30 days)
        upcoming = conn.execute("""
        SELECT id, name, category, quantity, expiry_date
        FROM medicines
        WHERE expiry_date BETWEEN date('now') AND date('now', '+30 days')
        ORDER BY expiry_date ASC
        """).fetchall()
        
        if upcoming:
            st.warning("📅 Medicines expiring within 30 days:")
            df_upcoming = pd.DataFrame(
                upcoming,
                columns=["ID", "Medicine Name", "Category", "Stock", "Expiry Date"]
            )
            st.dataframe(df_upcoming, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("*Medicine management interface - Real-time database*")

conn.close()
