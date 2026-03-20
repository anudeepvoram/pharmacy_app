import streamlit as st
import sqlite3
import pandas as pd
from services.billing_service import create_bill
from services.pdf_service import generate_bill_pdf
from styles import apply_global_styles, sidebar_header, success_message, error_message, warning_message, section_header
from config import DB_NAME, CURRENCY

st.set_page_config(page_title="Billing System", layout="wide")
apply_global_styles()

with st.sidebar:
    sidebar_header()

conn = sqlite3.connect(DB_NAME)

st.title("🧾 Billing & Invoice System")
st.markdown("Create and manage customer bills")
st.markdown("---")

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    section_header("Customer Information", "👤")
    customers = conn.execute("SELECT id, name, phone FROM customers ORDER BY name ASC").fetchall()
    
    if customers:
        customer = st.selectbox(
            "Select Customer",
            customers,
            format_func=lambda x: f"{x[1]} ({x[2]})" if x else "No Customers",
            key="customer_select"
        )
    else:
        st.warning("⚠️ No customers available. Please add customers first.")
        customer = None

with col2:
    section_header("Cart Summary", "🛒")
    
    if st.session_state.cart:
        total = sum(item["price"] * item["quantity"] for item in st.session_state.cart)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Items", len(st.session_state.cart))
        with col_b:
            st.metric("Total", f"{CURRENCY}{total:,.2f}")
    else:
        st.metric("Items", "0")
        st.metric("Total", f"{CURRENCY}0.00")

st.markdown("---")

# Medicine Selection
section_header("Add Medicines to Bill", "💊")

col1, col2 = st.columns([3, 1])

with col1:
    search = st.text_input(
        "🔍 Search medicine",
        placeholder="Type medicine name...",
        key="med_search"
    )

medicines = conn.execute(
    "SELECT id, name, price, quantity FROM medicines WHERE name LIKE ? ORDER BY name ASC",
    (f"%{search}%",)
).fetchall()

if medicines:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        med = st.selectbox(
            "Select Medicine",
            medicines,
            format_func=lambda x: f"{x[1]} - {CURRENCY}{x[2]} (Stock: {x[3]})",
            key="med_select"
        )
    
    with col2:
        qty = st.number_input(
            "Quantity",
            min_value=1,
            max_value=med[3] if med else 1,
            step=1,
            key="qty_input"
        )
    
    with col3:
        st.write("")  # Spacer
        if st.button("➕ Add to Cart", use_container_width=True, key="add_btn"):
            if med:
                # Check if item already in cart
                existing = next((item for item in st.session_state.cart if item["medicine_id"] == med[0]), None)
                
                if existing:
                    if existing["quantity"] + qty <= med[3]:
                        existing["quantity"] += qty
                        success_message(f"Updated '{med[1]}' in cart")
                    else:
                        error_message(f"Not enough stock! Available: {med[3]}")
                else:
                    st.session_state.cart.append({
                        "medicine_id": med[0],
                        "name": med[1],
                        "price": med[2],
                        "quantity": qty
                    })
                    success_message(f"Added '{med[1]}' to cart")
                st.rerun()
else:
    st.info("No medicines found. Try different search term.")

st.markdown("---")

# Cart Display
section_header("Shopping Cart", "🛒")

if st.session_state.cart:
    # Cart table
    cart_data = []
    total_amount = 0
    
    for i, item in enumerate(st.session_state.cart):
        item_total = item["price"] * item["quantity"]
        total_amount += item_total
        cart_data.append({
            "No.": i + 1,
            "Medicine": item["name"],
            f"Unit Price ({CURRENCY})": f"{item['price']:.2f}",
            "Quantity": item["quantity"],
            f"Total ({CURRENCY})": f"{item_total:.2f}"
        })
    
    df = pd.DataFrame(cart_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Remove items
    col1, col2 = st.columns([3, 1])
    
    with col1:
        item_to_remove = st.selectbox(
            "Remove item",
            range(len(st.session_state.cart)),
            format_func=lambda i: f"{i+1}. {st.session_state.cart[i]['name']}",
            key="remove_select"
        )
    
    with col2:
        st.write("")  # Spacer
        if st.button("🗑️ Remove", use_container_width=True):
            st.session_state.cart.pop(item_to_remove)
            st.rerun()
    
    st.markdown("---")
    
    # Billing details
    section_header("Billing Details", "💰")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        discount = st.number_input(
            f"Discount ({CURRENCY})",
            min_value=0.0,
            step=10.0,
            value=0.0,
            key="discount"
        )
    
    with col2:
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"],
            key="payment_method"
        )
    
    with col3:
        # Get available coupons
        coupons = conn.execute("""
            SELECT id, code, discount_type, discount_value, max_usage, current_usage
            FROM coupons
            WHERE is_active = 1 AND current_usage < max_usage
            ORDER BY code ASC
        """).fetchall()
        
        if coupons:
            coupon_option = st.selectbox(
                "Apply Coupon",
                ["None"] + [f"{c[1]} ({c[2]}: {c[3]})" for c in coupons],
                key="coupon_select"
            )
        else:
            coupon_option = "None"
            st.write("*No active coupons available*")
    
    # Calculate summary with coupon
    coupon_discount = 0
    if coupon_option != "None":
        coupon_data = next((c for c in coupons if f"{c[1]} ({c[2]}: {c[3]})" == coupon_option), None)
        if coupon_data:
            if coupon_data[2] == "percentage":
                coupon_discount = (total_amount * coupon_data[3]) / 100
            else:
                coupon_discount = coupon_data[3]
    
    final_amount = max(0, total_amount - discount - coupon_discount)
    
    # Calculate profit from cart items
    total_cost = 0
    for item in st.session_state.cart:
        med = conn.execute("SELECT cost_price FROM medicines WHERE id = ?", (item["medicine_id"],)).fetchone()
        if med and med[0]:
            total_cost += med[0] * item["quantity"]
    
    profit = final_amount - total_cost
    profit_margin = (profit / final_amount * 100) if final_amount > 0 else 0
    
    st.markdown("---")
    
    # Summary display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Subtotal:**")
        st.markdown("**Manual Discount:**")
        if coupon_option != "None":
            st.markdown(f"**Coupon Discount ({coupon_option.split()[0]}):**")
        st.markdown("### **Total to Pay:**")
        st.markdown("---")
        st.markdown("**Cost Price (Wholesale):**")
        st.markdown("### **Estimated Profit:**")
    
    with col2:
        st.markdown(f"{CURRENCY}{total_amount:,.2f}")
        st.markdown(f"-{CURRENCY}{discount:,.2f}")
        if coupon_option != "None":
            st.markdown(f"-{CURRENCY}{coupon_discount:,.2f}")
        st.markdown(f"### {CURRENCY}{final_amount:,.2f}")
        st.markdown("---")
        st.markdown(f"{CURRENCY}{total_cost:,.2f}")
        st.markdown(f"### {CURRENCY}{profit:,.2f} ({profit_margin:.1f}%)")
    
    st.markdown("---")
    
    # Action buttons
    if customer:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Create Bill", use_container_width=True, key="create_btn"):
                try:
                    items = [
                        {"medicine_id": item["medicine_id"], "quantity": item["quantity"]}
                        for item in st.session_state.cart
                    ]
                    
                    # Get user ID from session
                    user_id = st.session_state.user_info['id'] if st.session_state.user_info else None
                    
                    bill_id = create_bill(
                        customer[0],
                        items,
                        user_id=user_id,
                        discount=discount,
                        payment_method=payment_method
                    )
                    
                    # Generate PDF
                    bill_data = [
                        {
                            "name": item["name"],
                            "quantity": item["quantity"],
                            "price": item["price"]
                        }
                        for item in st.session_state.cart
                    ]
                    
                    customer_name = customer[1] if customer else "Walk-in Customer"
                    file = generate_bill_pdf(
                        bill_data,
                        filename=f"bill_{bill_id}.pdf",
                        customer_name=customer_name,
                        bill_id=bill_id
                    )
                    
                    with open(file, "rb") as f:
                        st.download_button(
                            "📄 Download Bill PDF",
                            f,
                            file_name=f"bill_{bill_id}.pdf",
                            use_container_width=True
                        )
                    
                    success_message(f"✅ Bill Created Successfully! Bill ID: {bill_id}")
                    st.session_state.cart = []
                    st.rerun()
                
                except Exception as e:
                    error_message(f"Error creating bill: {str(e)}")
        
        with col2:
            if st.button("🔄 Clear Cart", use_container_width=True, key="clear_btn"):
                st.session_state.cart = []
                st.rerun()
        
        with col3:
            if st.button("💾 Print Bill", use_container_width=True, key="print_btn", disabled=True):
                st.info("Print feature coming soon")
    else:
        st.warning("Please select a customer to proceed")
else:
    st.info("🛒 Add medicines to cart to create a bill")

st.markdown("---")
st.markdown("*Professional Billing System - Real-time Inventory*")

conn.close()
