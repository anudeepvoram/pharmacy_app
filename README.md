# 💊 Pharmacy Management System - Production Ready

## Overview

A **production-grade pharmacy management system** built with **Streamlit**, featuring enterprise-grade security with user authentication, professional styling, and comprehensive inventory management.

---

## ✨ Key Features

### 1. **User Authentication & Security** 🔐
- **Secure Registration System**: Users can create accounts with encrypted passwords
- **Login Authentication**: SHA256 password hashing for security
- **Role-Based Access**: Admin, Pharmacist, and other roles (expandable)
- **Session Management**: Persistent user sessions across the application
- **User Tracking**: All bills and transactions tracked by user

### 2. **Dashboard** 📊
- Real-time KPIs (Total Medicines, Sales, Stock Alerts, Expiry Warnings)
- Top-selling medicines analysis with interactive visualizations
- Low stock alerts with actionable insights
- Expiry date tracking (30-day window)
- User-specific activity tracking
- Professional charts using Plotly

### 3. **Medicine Management** 💊
- Add medicines with detailed information (name, category, price, quantity, expiry, manufacturer, batch)
- Search and filter by name or category
- Sort by price, quantity, or expiry date
- Real-time inventory tracking
- Update stock quantities and prices
- Delete obsolete entries
- Category management (Painkillers, Antibiotics, Vitamins, etc.)

### 4. **Customer Management** 👥
- Register new customers with complete contact details
- Search and filter customer database
- View transaction history per customer
- Edit customer information
- Customer transaction analytics
- Address and contact management

### 5. **Professional Billing System** 🧾
- Shopping cart interface with real-time updates
- Medicine search and selection
- Real-time stock validation
- Discount application
- Multiple payment methods (Cash, Card, UPI, Net Banking)
- Professional PDF bill generation
- Bill tracking and history
- User-specific bill tracking

### 6. **Advanced Reports & Analytics** 📈
- Sales reports with date range filtering
- Revenue breakdown by period
- Top-performing products analysis
- Inventory valuation and status
- Sales trends and forecasting
- Daily sales metrics
- Exportable reports (CSV format)
- Payment method analysis

---

## 🏗️ Architecture

### Project Structure
```
pharmacy_app/
├── app.py                    # Main application entry point
├── auth.py                   # Authentication & user management
├── config.py                 # Global configuration & constants
├── styles.py                 # Professional styling & UI components
├── setup.py                  # Database initialization script
├── database/
│   └── db.py                 # Database schema & initialization
├── pages/
│   ├── dashboard.py          # Analytics dashboard
│   ├── medicines.py          # Medicine inventory management
│   ├── customers.py          # Customer relationship management
│   ├── billing.py            # Billing & invoicing system
│   └── reports.py            # Reports & analytics
├── services/
│   ├── billing_service.py    # Billing logic & bill creation
│   ├── medicine_service.py   # Medicine operations
│   └── pdf_service.py        # Professional PDF generation
├── pharmacy.db               # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── DEPLOYMENT.md            # Production deployment guide
```

### Technology Stack
- **Frontend**: Streamlit (Modern, responsive UI)
- **Backend**: Python 3.10+
- **Database**: SQLite3 (with optimization)
- **Visualization**: Plotly (interactive charts)
- **PDF Generation**: ReportLab (professional invoices)
- **Data Processing**: Pandas (data manipulation)
- **Security**: SHA256 hashing, SQL parameterized queries

### Database Schema
```
users
├── id (PRIMARY KEY)
├── username (UNIQUE)
├── email (UNIQUE)
├── password (hashed)
├── full_name
├── role (admin/pharmacist)
├── is_active
└── created_at

medicines
├── id (PRIMARY KEY)
├── name
├── category
├── price
├── quantity
├── expiry_date
├── manufacturer
├── batch_number
└── created_at

customers
├── id (PRIMARY KEY)
├── name
├── phone
├── email
├── address
├── city
└── created_at

bills
├── id (PRIMARY KEY)
├── customer_id (FOREIGN KEY)
├── user_id (FOREIGN KEY)
├── total_amount
├── discount
├── payment_method
└── created_at

bill_items
├── id (PRIMARY KEY)
├── bill_id (FOREIGN KEY)
├── medicine_id (FOREIGN KEY)
├── quantity
└── price
```

---

## 🛠️ How We Made the Project

### Development Process
1. **Planning & Design** (1 week)
   - Requirements gathering for pharmacy operations
   - Database schema design with normalization
   - UI/UX wireframing for professional look
   - Security architecture planning

2. **Core Development** (2 weeks)
   - Database layer with SQLite3 and schema migrations
   - Authentication system with SHA256 hashing
   - Streamlit UI components and navigation
   - Business logic for inventory, billing, and reports

3. **Feature Implementation** (2 weeks)
   - Medicine management with CRUD operations
   - Customer management system
   - Professional billing with PDF generation
   - Analytics dashboard with Plotly charts
   - Advanced reporting and filtering

4. **Testing & Refinement** (1 week)
   - Unit testing for database operations
   - Integration testing for workflows
   - UI/UX polishing and responsive design
   - Performance optimization

5. **Production Ready** (1 week)
   - Error handling and validation
   - Security hardening
   - Documentation and deployment guides
   - Sample data and setup scripts

### Development Principles
- **Modular Architecture**: Separated concerns into database, services, pages, and UI
- **Security First**: All inputs validated, passwords hashed, SQL injection prevention
- **User Experience**: Professional styling, intuitive navigation, real-time feedback
- **Scalability**: Efficient queries, indexed database, expandable features
- **Maintainability**: Clean code, comprehensive documentation, reusable components

---

## 📦 Libraries Installed & Installation

### Core Dependencies
```txt
streamlit>=1.28.0          # Web framework
pandas>=2.0.0              # Data manipulation
plotly>=5.15.0             # Interactive charts
reportlab>=4.0.0           # PDF generation
sqlite3                    # Database (built-in Python)
hashlib                    # Password hashing (built-in)
datetime                   # Date/time handling (built-in)
pathlib                    # File paths (built-in)
```

### Installation Steps

#### 1. Prerequisites
- Python 3.10 or higher
- pip package manager
- Git (optional, for cloning)

#### 2. Clone or Download
```bash
git clone <repository-url>
cd pharmacy_app
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Verify Installation
```bash
python3 -c "import streamlit, pandas, plotly, reportlab; print('All libraries installed successfully!')"
```

#### 6. Run Setup
```bash
python3 setup.py
```

#### 7. Start Application
```bash
streamlit run app.py
```

### Troubleshooting Installation
- **Permission Error**: Use `pip install --user` or run as administrator
- **Python Version**: Ensure Python 3.10+ is used
- **Virtual Environment**: Always activate venv before installing
- **Missing Libraries**: Run `pip install -r requirements.txt` again

---

## 📁 Project Files & Their Purpose

### Root Directory Files
- **`app.py`**: Main application entry point. Initializes database, applies global styles, handles authentication, and manages page navigation.
- **`auth.py`**: Handles user authentication including login, signup, password hashing, and session management.
- **`config.py`**: Contains global constants like app name, currency, database path, and configuration settings.
- **`styles.py`**: Defines professional CSS styling, sidebar components, and UI helper functions.
- **`setup.py`**: Database initialization script that creates tables, adds sample data, and sets up indexes.
- **`requirements.txt`**: Lists all Python dependencies with versions.
- **`README.md`**: This comprehensive documentation file.
- **`DEPLOYMENT.md`**: Production deployment and scaling guide.

### Database Layer (`database/`)
- **`db.py`**: Database schema definitions, table creation, migration helpers, and sample data insertion. Contains functions for creating tables with automatic column additions for backward compatibility.

### Pages (`pages/`)
- **`dashboard.py`**: Main analytics dashboard with KPIs, charts, alerts, and user activity tracking.
- **`medicines.py`**: Medicine inventory management with CRUD operations, search, filtering, and stock updates.
- **`customers.py`**: Customer relationship management with registration, search, editing, and transaction history.
- **`billing.py`**: Professional billing system with shopping cart, payment processing, and PDF generation.
- **`reports.py`**: Advanced reporting with sales analysis, inventory status, trends, and exportable data.

### Services (`services/`)
- **`billing_service.py`**: Business logic for bill creation, cart management, and transaction processing.
- **`medicine_service.py`**: Medicine-related operations like stock validation and inventory calculations.
- **`pdf_service.py`**: Professional PDF bill generation with formatting and layout.

### Generated Files
- **`pharmacy.db`**: SQLite database file (auto-created during setup).
- **`__pycache__/`**: Python bytecode cache (auto-generated).
- **`venv/`**: Virtual environment directory (created during installation).

---

## 🗄️ Database Design & Connection

### Database Architecture
The system uses **SQLite3** for simplicity and reliability. SQLite is file-based, requires no server setup, and is perfect for single-user or small-team applications.

### Connection Method
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Execute queries
cursor.execute("SELECT * FROM medicines")
results = cursor.fetchall()

# Close connection
conn.close()
```

### Schema Design

#### Tables Overview
1. **`users`** - User authentication and roles
2. **`medicines`** - Medicine inventory and details
3. **`customers`** - Customer information and contacts
4. **`bills`** - Transaction headers
5. **`bill_items`** - Transaction line items

#### Detailed Schema

**users table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'pharmacist',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**medicines table:**
```sql
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    expiry_date TEXT,
    manufacturer TEXT,
    batch_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**customers table:**
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**bills table:**
```sql
CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    user_id INTEGER,
    total_amount REAL,
    discount REAL DEFAULT 0,
    payment_method TEXT DEFAULT 'Cash',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

**bill_items table:**
```sql
CREATE TABLE bill_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    medicine_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(bill_id) REFERENCES bills(id),
    FOREIGN KEY(medicine_id) REFERENCES medicines(id)
);
```

### Database Relationships
- **One-to-Many**: Users → Bills, Customers → Bills, Bills → Bill_Items, Medicines → Bill_Items
- **Foreign Keys**: Enforce referential integrity
- **Indexes**: Optimized for common queries (name, category, dates)

### Schema Migration
The system includes automatic schema migration to handle updates:
```python
def ensure_column(conn, table_name, column_name, definition):
    """Add missing columns to existing tables"""
    cols = get_table_columns(conn, table_name)
    if column_name not in cols:
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
        conn.commit()
```

### Running the Database
1. **Initialization**: `python3 setup.py` creates tables and sample data
2. **Connection**: Automatic connection in each page using `sqlite3.connect(DB_NAME)`
3. **Transactions**: Proper commit/rollback for data integrity
4. **Backup**: Simple file copy for database backup
5. **Performance**: Indexed queries for fast searches and reports

### Sample Data
The setup script populates:
- 15 medicines across 6 categories
- 10 customers with contact details
- 15 bills with various payment methods
- 25+ bill items for transaction history

This provides realistic data for testing all features and analytics.

---

## 🎨 Professional Styling

### Color Scheme
- **Primary**: `#0066CC` (Professional Blue)
- **Secondary**: `#00A86B` (Medical Green)
- **Accent**: `#FF6B6B` (Alert Red)
- **Success**: `#27AE60` (Success Green)
- **Warning**: `#FFA500` (Warning Orange)
- **Light Background**: `#F8F9FA`

### UI/UX Features
- Modern card-based layouts
- Responsive grid system
- Interactive charts and visualizations
- Professional data tables with sorting
- Validated form inputs
- Status badges and alerts
- Smooth transitions and hover effects
- Accessibility-focused design

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10 or higher
pip (Python package manager)
```

### Step 1: Clone/Extract Project
```bash
cd pharmacy_app
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python setup.py
```

This will:
- ✅ Create database tables
- ✅ Add default admin user (admin/1234)
- ✅ Load 15 sample medicines
- ✅ Load 10 sample customers
- ✅ Create database indexes

### Step 5: Run Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## 📋 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `1234`

⚠️ **Change these credentials immediately in production!**

---

## 💡 Usage Guide

### 1. First-Time Login
1. Go to http://localhost:8501
2. Click "Sign Up" tab to create a new account, OR
3. Use demo credentials: `admin` / `1234`

### 2. Creating a New User Account
1. Click "Sign Up" tab on login page
2. Enter: Full Name, Email, Username, Password
3. Confirm password and submit
4. Login with your new credentials

### 3. Adding Medicines
1. Navigate to **💊 Medicines** from sidebar
2. Go to **➕ Add Medicine** tab
3. Fill in medicine details (name, category, price, stock, expiry)
4. Click **✅ Add Medicine**
5. Verify in **📋 Inventory** tab

### 4. Registering Customers
1. Navigate to **👥 Customers**
2. Go to **➕ Add Customer** tab
3. Enter customer details (name, phone, email, address)
4. Click **✅ Add Customer**

### 5. Creating a Bill
1. Navigate to **🧾 Billing**
2. Select customer from dropdown
3. Search for medicine and enter quantity
4. Click **➕ Add to Cart**
5. Review cart and enter discount (if any)
6. Select payment method
7. Click **✅ Create Bill**
8. Download PDF invoice

### 6. Viewing Reports
1. Navigate to **📈 Reports & Analytics**
2. Select date range
3. Choose report type (Sales, Inventory, Trends)
4. View charts and metrics
5. Export data as CSV

---

## 🔐 Security Features

### Implemented Security
- **Password Hashing**: SHA256 encryption for all passwords
- **SQL Injection Protection**: Parameterized database queries
- **Session Management**: Secure session handling
- **User Validation**: Input validation on all forms
- **Role-Based Access**: Different access levels per user role
- **CSRF Protection**: Streamlit built-in CSRF protection

### Production Security Checklist
- [ ] Change default admin credentials
- [ ] Enable HTTPS/SSL
- [ ] Set up environment variables for secrets
- [ ] Enable database backups
- [ ] Configure access logs
- [ ] Set up rate limiting
- [ ] Enable firewall rules
- [ ] Regular security audits

---

## 📊 Sample Data

The system comes with:
- **15 Medicines** across multiple categories
  - Painkillers (Aspirin, Ibuprofen, Paracetamol)
  - Antibiotics (Amoxicillin, Cephalexin)
  - Vitamins (D3, B12)
  - Cardiac (Atorvastatin, Lisinopril)
  - And more...

- **10 Sample Customers** from different cities
  - Includes phone, email, and address information
  - Ready for testing billing functionality

---

## 🛠️ Configuration

Edit `config.py` to customize:

```python
# Application
APP_NAME = "Pharmacy Management System"
CURRENCY = "₹"

# Stock Management
LOW_STOCK_THRESHOLD = 10      # Alert when stock is below this
EXPIRY_ALERT_DAYS = 30        # Alert medicines expiring within this period

# Database
DB_NAME = "pharmacy.db"

# Color Scheme (Professional Medical Theme)
COLORS = {
    "primary": "#0066CC",
    "secondary": "#00A86B",
    "accent": "#FF6B6B",
    # ... more colors
}
```

---

## 📈 Performance Optimization

### Implemented Optimizations
- Database indexing on frequently queried columns
- Lazy loading of large datasets
- Efficient Pandas operations
- Plotly chart caching
- Session state management

### Database Optimization
```python
# Automatically created indexes:
- medicines.name
- medicines.category
- bills.customer_id
- bills.user_id
- bills.created_at
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution:**
```bash
# Reinitialize database
rm pharmacy.db
python setup.py
```

### Issue: Port already in use (8501)
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Changes not reflecting
**Solution:**
```bash
# Clear Streamlit cache
rm -r ~/.streamlit/cache
streamlit run app.py
```

---

## 📝 Advanced Configuration

### Environment Variables
Create `.env` file:
```
DATABASE_PATH=/path/to/pharmacy.db
LOG_LEVEL=INFO
SESSION_TIMEOUT=1800
MAX_UPLOAD_SIZE=10
```

### Custom Styling
Edit `styles.py` to customize colors, fonts, and layouts.

### Database Backup
```bash
# Backup database
cp pharmacy.db pharmacy.db.backup

# Restore from backup
cp pharmacy.db.backup pharmacy.db
```

---

## 🚀 Deployment Guide

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker containerization
- Cloud platform deployment (AWS, GCP, Azure)
- Nginx reverse proxy setup
- SSL/TLS configuration
- Database backups
- Monitoring and alerts

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Review low-stock alerts, verify expiry dates
2. **Monthly**: Backup database, review reports
3. **Quarterly**: Security audit, performance review
4. **Annually**: License renewal, system upgrade

### Useful SQL Queries
```python
# See pharmacy.db for direct database access:
sqlite3 pharmacy.db

# Check total sales:
SELECT SUM(total_amount) FROM bills;

# View low stock medicines:
SELECT name, quantity FROM medicines WHERE quantity < 10;

# User activity:
SELECT u.full_name, COUNT(b.id) as bills
FROM users u LEFT JOIN bills b ON u.id = b.user_id
GROUP BY u.id;
```

---

## 🎯 Roadmap

### v1.1 (Planned)
- [ ] Email notifications for alerts
- [ ] Barcode scanning integration
- [ ] Supplier management module
- [ ] Purchase orders

### v2.0 (Planned)
- [ ] REST API for mobile apps
- [ ] Advanced analytics & ML predictions
- [ ] Multi-branch support
- [ ] Real-time synchronization

---

## 📄 License

This project is proprietary. Unauthorized copying, modification, or distribution is prohibited.

---

## 👨‍💼 Business Model

This system is ideal for:
- Independent pharmacies
- Hospital pharmacies
- Chain pharmacy operations
- Retail medicine shops
- Healthcare clinics

**Key Business Benefits:**
- ✅ Inventory optimization
- ✅ Sales tracking and analytics
- ✅ Customer relationship management
- ✅ Professional invoicing
- ✅ Regulatory compliance ready
- ✅ Scalable architecture

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: March 2026