import sqlite3

DB_NAME = "pharmacy.db"


def add_medicine(name, category, price, quantity, expiry_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO medicines (name, category, price, quantity, expiry_date)
    VALUES (?, ?, ?, ?, ?)
    """, (name, category, price, quantity, expiry_date))

    conn.commit()
    conn.close()


def get_all_medicines():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()

    conn.close()
    return data