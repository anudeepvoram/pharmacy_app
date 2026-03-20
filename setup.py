#!/usr/bin/env python3
"""
Pharmacy Management System - Setup and Initialization Script

This script sets up the database, creates a default admin user, and loads sample data.
Run this once before starting the application.
"""

import sqlite3
import sys
from pathlib import Path

from database.db import create_tables, add_default_admin, add_sample_data

DB_NAME = "pharmacy.db"


def create_indexes():
    """Create database indexes for better performance."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_medicines_name ON medicines(name)",
        "CREATE INDEX IF NOT EXISTS idx_medicines_category ON medicines(category)",
        "CREATE INDEX IF NOT EXISTS idx_bills_customer ON bills(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_bills_user ON bills(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_bills_date ON bills(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_bill_items_bill ON bill_items(bill_id)",
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
    ]

    for stmt in index_statements:
        try:
            cursor.execute(stmt)
        except Exception:
            # Ignore missing columns/tables; schema migration handled by database/db.py
            pass

    conn.commit()
    conn.close()
    print("✅ Database indexes created!")


def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("💊 Pharmacy Management System - Setup Wizard")
    print("=" * 60 + "\n")

    if Path(DB_NAME).exists():
        print(f"ℹ️  Database '{DB_NAME}' already exists.\n")

    print("Starting setup...\n")

    # Ensure schema exists (will also migrate any missing columns)
    create_tables()

    # Ensure default admin exists
    add_default_admin()

    # Add demo data
    add_sample_data()

    # Create helpful indexes
    create_indexes()

    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Login with: admin / 1234")
    print("3. Change credentials after first login")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
