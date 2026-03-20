import sqlite3
import hashlib

DB_NAME = "pharmacy.db"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_table_columns(conn, table_name):
    """Return a set of column names for a given table."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def ensure_column(conn, table_name, column_name, definition):
    """Ensure a column exists in a table; if not, add it."""
    cols = get_table_columns(conn, table_name)
    if column_name not in cols:
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
        conn.commit()


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table for authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'pharmacist',
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Medicines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        cost_price REAL,
        wholesale_price REAL,
        quantity INTEGER NOT NULL,
        expiry_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Suppliers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        city TEXT,
        tax_id TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Purchase orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_id INTEGER,
        order_date TEXT,
        total_amount REAL,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
    )
    """)

    # Purchase order items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        unit_cost REAL,
        FOREIGN KEY(order_id) REFERENCES purchase_orders(id),
        FOREIGN KEY(medicine_id) REFERENCES medicines(id)
    )
    """)

    # Coupons table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        discount_type TEXT,
        discount_value REAL,
        max_usage INTEGER,
        current_usage INTEGER DEFAULT 0,
        valid_from TEXT,
        valid_until TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Offers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        medicine_id INTEGER,
        category TEXT,
        offer_type TEXT,
        discount_value REAL,
        valid_from TEXT,
        valid_until TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(medicine_id) REFERENCES medicines(id)
    )
    """)

    # Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Bills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        total_amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Bill items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        price REAL
    )
    """)

    conn.commit()

    # Migrate schema: add missing columns
    ensure_column(conn, "medicines", "manufacturer", "TEXT")
    ensure_column(conn, "medicines", "batch_number", "TEXT")
    ensure_column(conn, "medicines", "cost_price", "REAL")
    ensure_column(conn, "medicines", "wholesale_price", "REAL")
    
    ensure_column(conn, "customers", "address", "TEXT")
    ensure_column(conn, "customers", "city", "TEXT")
    ensure_column(conn, "customers", "created_at", "TIMESTAMP")

    ensure_column(conn, "bills", "user_id", "INTEGER")
    ensure_column(conn, "bills", "discount", "REAL DEFAULT 0")
    ensure_column(conn, "bills", "payment_method", "TEXT DEFAULT 'Cash'")
    ensure_column(conn, "bills", "coupon_id", "INTEGER")
    ensure_column(conn, "bills", "tax_amount", "REAL DEFAULT 0")
    ensure_column(conn, "bills", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    conn.close()

def add_default_admin():
    """Add default admin user if not exists"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Check if admin exists
        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO users (username, email, password, full_name, role)
            VALUES (?, ?, ?, ?, ?)
            """, (
                "admin",
                "admin@pharmacy.com",
                hash_password("1234"),
                "Administrator",
                "admin"
            ))
            conn.commit()
            print("Default admin user created!")
    except Exception as e:
        print(f"Error creating default admin: {e}")
    finally:
        conn.close()

def add_sample_data():
    """Add sample medicines, customers, bills, and bill items for demo"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Check if medicines already exist
        cursor.execute("SELECT COUNT(*) FROM medicines")
        if cursor.fetchone()[0] == 0:
            # Sample medicines data (15 items) - name, category, selling_price, cost_price, wholesale_price, quantity, expiry_date, manufacturer, batch_number
            medicines = [
                ("Aspirin", "Painkillers", 50.00, 30.00, 25.00, 150, "2025-12-31", "Bayer", "B001"),
                ("Ibuprofen", "Painkillers", 75.00, 45.00, 40.00, 200, "2025-11-30", "Pfizer", "B002"),
                ("Paracetamol", "Painkillers", 45.00, 25.00, 20.00, 250, "2026-01-15", "GSK", "B003"),
                ("Amoxicillin", "Antibiotics", 120.00, 70.00, 60.00, 100, "2025-09-30", "Apollo", "B004"),
                ("Cephalexin", "Antibiotics", 150.00, 85.00, 75.00, 80, "2025-10-15", "Cipla", "B005"),
                ("Vitamin D3", "Vitamins", 200.00, 120.00, 100.00, 300, "2026-06-30", "Nature", "B006"),
                ("Vitamin B12", "Vitamins", 180.00, 110.00, 90.00, 200, "2026-05-20", "Nature", "B007"),
                ("Omeprazole", "Digestive", 90.00, 50.00, 45.00, 120, "2025-08-31", "Sun Pharma", "B008"),
                ("Metformin", "Diabetes", 110.00, 65.00, 55.00, 150, "2025-12-31", "Lupin", "B009"),
                ("Atorvastatin", "Cardiac", 200.00, 120.00, 100.00, 100, "2026-02-28", "Mylan", "B010"),
                ("Cetirizine", "Antihistamine", 80.00, 45.00, 40.00, 180, "2025-09-15", "Ranbaxy", "B011"),
                ("Loratadine", "Antihistamine", 85.00, 50.00, 45.00, 160, "2025-10-20", "J&J", "B012"),
                ("Salbutamol", "Respiratory", 300.00, 180.00, 150.00, 70, "2025-07-31", "Cipla", "B013"),
                ("Fluticasone", "Respiratory", 350.00, 210.00, 180.00, 60, "2025-08-15", "GSK", "B014"),
                ("Lisinopril", "Cardiac", 95.00, 55.00, 45.00, 140, "2026-01-31", "Micro Labs", "B015"),
            ]
            
            for med in medicines:
                cursor.execute("""
                INSERT INTO medicines (name, category, price, cost_price, wholesale_price, quantity, expiry_date, manufacturer, batch_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, med)
            
            conn.commit()
            print(f"Added {len(medicines)} sample medicines!")
        
        # Check if customers already exist
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            # Sample customers data (10 items)
            customers = [
                ("Rajesh Kumar", "9876543210", "rajesh@email.com", "123 Main St", "Mumbai"),
                ("Priya Singh", "9876543211", "priya@email.com", "456 Oak Ave", "Delhi"),
                ("Amit Patel", "9876543212", "amit@email.com", "789 Pine Rd", "Bangalore"),
                ("Neha Sharma", "9876543213", "neha@email.com", "321 Elm St", "Pune"),
                ("Vikram Gupta", "9876543214", "vikram@email.com", "654 Maple Dr", "Chennai"),
                ("Anjali Verma", "9876543215", "anjali@email.com", "987 Cedar Ln", "Kolkata"),
                ("Rohit Desai", "9876543216", "rohit@email.com", "147 Birch Way", "Hyderabad"),
                ("Divya Menon", "9876543217", "divya@email.com", "258 Ash Court", "Pune"),
                ("Arjun Nair", "9876543218", "arjun@email.com", "369 Oak Street", "Kochi"),
                ("Sneha Reddy", "9876543219", "sneha@email.com", "741 Pine Avenue", "Bangalore"),
            ]
            
            for customer in customers:
                cursor.execute("""
                INSERT INTO customers (name, phone, email, address, city)
                VALUES (?, ?, ?, ?, ?)
                """, customer)
            
            conn.commit()
            print(f"Added {len(customers)} sample customers!")
        
        # Check if bills already exist
        cursor.execute("SELECT COUNT(*) FROM bills")
        if cursor.fetchone()[0] == 0:
            # Sample bills data (15 bills)
            bills = [
                (1, 1, 225.00, 0.0, "Cash"),  # customer 1, user 1
                (2, 1, 150.00, 10.0, "Card"),
                (3, 1, 320.00, 0.0, "Cash"),
                (4, 1, 200.00, 20.0, "UPI"),
                (5, 1, 180.00, 0.0, "Cash"),
                (6, 1, 400.00, 40.0, "Card"),
                (7, 1, 250.00, 0.0, "Cash"),
                (8, 1, 175.00, 15.0, "UPI"),
                (9, 1, 300.00, 0.0, "Cash"),
                (10, 1, 220.00, 20.0, "Card"),
                (1, 1, 190.00, 0.0, "Cash"),
                (2, 1, 350.00, 35.0, "UPI"),
                (3, 1, 280.00, 0.0, "Cash"),
                (4, 1, 160.00, 10.0, "Card"),
                (5, 1, 420.00, 42.0, "Cash"),
            ]
            
            bill_ids = []
            for bill in bills:
                cursor.execute("""
                INSERT INTO bills (customer_id, user_id, total_amount, discount, payment_method)
                VALUES (?, ?, ?, ?, ?)
                """, bill)
                bill_ids.append(cursor.lastrowid)
            
            conn.commit()
            print(f"Added {len(bills)} sample bills!")
            
            # Sample bill items (multiple items per bill)
            bill_items = [
                # Bill 1: Aspirin x2, Ibuprofen x1
                (bill_ids[0], 1, 2, 50.00),
                (bill_ids[0], 2, 1, 75.00),
                # Bill 2: Paracetamol x2, Vitamin D3 x1
                (bill_ids[1], 3, 2, 45.00),
                (bill_ids[1], 6, 1, 200.00),
                # Bill 3: Amoxicillin x1, Cephalexin x1
                (bill_ids[2], 4, 1, 120.00),
                (bill_ids[2], 5, 1, 150.00),
                # Bill 4: Vitamin B12 x1, Omeprazole x1
                (bill_ids[3], 7, 1, 180.00),
                (bill_ids[3], 8, 1, 90.00),
                # Bill 5: Metformin x1, Atorvastatin x1
                (bill_ids[4], 9, 1, 110.00),
                (bill_ids[4], 10, 1, 200.00),
                # Bill 6: Cetirizine x2, Loratadine x1
                (bill_ids[5], 11, 2, 80.00),
                (bill_ids[5], 12, 1, 85.00),
                # Bill 7: Salbutamol x1, Fluticasone x1
                (bill_ids[6], 13, 1, 300.00),
                (bill_ids[6], 14, 1, 350.00),
                # Bill 8: Lisinopril x2
                (bill_ids[7], 15, 2, 95.00),
                # Bill 9: Aspirin x3, Paracetamol x2
                (bill_ids[8], 1, 3, 50.00),
                (bill_ids[8], 3, 2, 45.00),
                # Bill 10: Vitamin D3 x1, Vitamin B12 x1
                (bill_ids[9], 6, 1, 200.00),
                (bill_ids[9], 7, 1, 180.00),
                # Bill 11: Ibuprofen x2
                (bill_ids[10], 2, 2, 75.00),
                # Bill 12: Amoxicillin x1, Metformin x1
                (bill_ids[11], 4, 1, 120.00),
                (bill_ids[11], 9, 1, 110.00),
                # Bill 13: Cetirizine x1, Loratadine x1
                (bill_ids[12], 11, 1, 80.00),
                (bill_ids[12], 12, 1, 85.00),
                # Bill 14: Atorvastatin x1
                (bill_ids[13], 10, 1, 200.00),
                # Bill 15: Salbutamol x1, Lisinopril x1
                (bill_ids[14], 13, 1, 300.00),
                (bill_ids[14], 15, 1, 95.00),
            ]
            
            for item in bill_items:
                cursor.execute("""
                INSERT INTO bill_items (bill_id, medicine_id, quantity, price)
                VALUES (?, ?, ?, ?)
                """, item)
            
            conn.commit()
            print(f"Added {len(bill_items)} sample bill items!")
        
        # Add sample suppliers (5 suppliers)
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            suppliers = [
                ("Pharma Direct Ltd", "John Smith", "9988776655", "contact@pharmadirect.com", "123 Industrial Ave", "Mumbai", "TAX123456"),
                ("Global Medicines Co", "Sarah Johnson", "9988776656", "sales@globalmeds.com", "456 Trade Park", "Delhi", "TAX123457"),
                ("HealthCare Suppliers", "Rajesh Kumar", "9988776657", "info@healthsupply.com", "789 Commerce Rd", "Bangalore", "TAX123458"),
                ("Medical Distributors", "Priya Sharma", "9988776658", "order@medsupply.com", "321 Logistics Way", "Pune", "TAX123459"),
                ("Premium Pharma Group", "Amit Verma", "9988776659", "admin@premiumpharma.com", "654 Business Complex", "Chennai", "TAX123460"),
            ]
            
            for supplier in suppliers:
                cursor.execute("""
                INSERT INTO suppliers (name, contact_person, phone, email, address, city, tax_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, supplier)
            
            conn.commit()
            print(f"Added {len(suppliers)} sample suppliers!")
        
        # Add sample coupons (5 active, 2 expired)
        cursor.execute("SELECT COUNT(*) FROM coupons")
        if cursor.fetchone()[0] == 0:
            coupons = [
                ("SAVE10", "percentage", 10.0, 50, 5, "2024-01-01", "2026-12-31", 1),  # 10% off
                ("SAVE50", "fixed", 50.0, 20, 3, "2024-01-01", "2026-12-31", 1),  # ₹50 off
                ("FLAT20", "percentage", 20.0, 30, 8, "2024-02-01", "2026-12-31", 1),  # 20% off
                ("WELCOME", "fixed", 100.0, 10, 2, "2024-03-01", "2026-12-31", 1),  # ₹100 off
                ("SUMMER25", "percentage", 25.0, 40, 12, "2024-04-01", "2026-12-31", 1),  # 25% off
                ("EXPIREDCOUP", "percentage", 15.0, 5, 5, "2023-01-01", "2023-12-31", 0),  # Expired
                ("LASTCHANCE", "fixed", 75.0, 3, 3, "2023-06-01", "2023-09-30", 0),  # Expired
            ]
            
            for coupon in coupons:
                cursor.execute("""
                INSERT INTO coupons (code, discount_type, discount_value, max_usage, current_usage, valid_from, valid_until, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, coupon)
            
            conn.commit()
            print(f"Added {len(coupons)} sample coupons!")
        
        # Add sample offers (category-wise)
        cursor.execute("SELECT COUNT(*) FROM offers")
        if cursor.fetchone()[0] == 0:
            offers = [
                ("Buy 2 Painkillers Get 10% Off", None, "Painkillers", "percentage", 10.0, "2024-01-01", "2026-12-31", 1),
                ("Vitamins Special Discount", None, "Vitamins", "percentage", 15.0, "2024-01-01", "2026-12-31", 1),
                ("Antibiotics Bundle Offer", None, "Antibiotics", "fixed", 50.0, "2024-01-01", "2026-12-31", 1),
                ("Seasonal Cardiac Meds Sale", None, "Cardiac", "percentage", 20.0, "2024-02-01", "2026-12-31", 1),
                ("Respiratory Health Promotion", None, "Respiratory", "percentage", 12.0, "2024-03-01", "2026-12-31", 1),
            ]
            
            for offer in offers:
                cursor.execute("""
                INSERT INTO offers (name, medicine_id, category, offer_type, discount_value, valid_from, valid_until, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, offer)
            
            conn.commit()
            print(f"Added {len(offers)} sample offers!")
    
    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database tables created!")
    add_default_admin()
    add_sample_data()
    print("Database setup completed!")