import sqlite3
from datetime import datetime

DB_NAME = "pharmacy.db"


def create_bill(customer_id, items, user_id=None, discount=0, payment_method="Cash"):
    """
    Create a new bill with items and update inventory
    
    Args:
        customer_id: ID of the customer
        items: List of {"medicine_id": int, "quantity": int}
        user_id: ID of the user creating the bill
        discount: Discount amount
        payment_method: Payment method (Cash, Card, UPI, etc.)
    
    Returns:
        bill_id: ID of created bill
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    total_amount = 0

    # Calculate total and validate stock
    for item in items:
        cursor.execute("SELECT price, quantity FROM medicines WHERE id = ?", (item["medicine_id"],))
        result = cursor.fetchone()
        
        if not result:
            raise Exception(f"Medicine ID {item['medicine_id']} not found")
        
        price, stock = result

        if item["quantity"] > stock:
            raise Exception(f"Not enough stock for medicine ID {item['medicine_id']}. Available: {stock}")

        total_amount += price * item["quantity"]

    # Apply discount
    final_amount = max(0, total_amount - discount)

    # Insert into bills
    cursor.execute("""
    INSERT INTO bills (customer_id, user_id, total_amount, discount, payment_method, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, user_id, final_amount, discount, payment_method, datetime.now()))

    bill_id = cursor.lastrowid

    # Insert bill items and update stock
    for item in items:
        cursor.execute("SELECT price FROM medicines WHERE id = ?", (item["medicine_id"],))
        price = cursor.fetchone()[0]

        # Insert bill item
        cursor.execute("""
        INSERT INTO bill_items (bill_id, medicine_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """, (bill_id, item["medicine_id"], item["quantity"], price))

        # Update inventory
        cursor.execute("""
        UPDATE medicines
        SET quantity = quantity - ?
        WHERE id = ?
        """, (item["quantity"], item["medicine_id"]))

    conn.commit()
    conn.close()

    return bill_id


def get_user_bills(user_id, limit=50):
    """Get bills created by a specific user"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, customer_id, total_amount, created_at
    FROM bills
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT ?
    """, (user_id, limit))
    
    bills = cursor.fetchall()
    conn.close()
    
    return bills