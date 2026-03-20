# 📋 Installation & Testing Guide

## System Requirements

- **Python**: 3.10 or higher
- **OS**: macOS, Linux, or Windows
- **Disk Space**: 50MB minimum
- **RAM**: 1GB minimum
- **Internet**: Required for initial pip install

## Installation Steps

### 1. Clone/Navigate to Project
```bash
cd /Users/anudeep/Desktop/pharmacy_app
```

### 2. Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -m pip list | grep -E "streamlit|pandas|plotly|reportlab"
```

**Output should show:**
- streamlit==1.28.0
- pandas==2.0.0
- plotly==5.15.0
- reportlab==4.0.7

### 4. Initialize Database
```bash
# Create database with sample data
python database/db.py

# Expected output:
# Database tables created!
# Default admin user created!
# Added 15 sample medicines!
# Added 10 sample customers!
# Added 15 sample bills!
# Added 27 sample bill items!
# Added 5 sample suppliers!
# Added 7 sample coupons!
# Added 5 sample offers!
# Database setup completed!
```

### 5. Run Application
```bash
streamlit run app.py
```

**Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## ✅ Testing Checklist

### Login (2 min)
- [ ] Open http://localhost:8501
- [ ] Username: `admin`
- [ ] Password: `1234`
- [ ] Click "Login"
- [ ] See "Welcome, Administrator" in sidebar

### Dashboard (1 min)
- [ ] Navigate to Dashboard
- [ ] See 4 KPI cards
  - Total Medicines: 15
  - Today's Sales
  - Low Stock Count
  - Expiring Count
- [ ] Check links work

### Medicines - View (2 min)
- [ ] Go to Medicines → Tab 1
- [ ] Search "Aspirin"
- [ ] See columns: Name, Category, Price, Stock, Expiry
- [ ] Click "View Details" to see pricing tiers
- [ ] Verify profit calculation (₹20 for Aspirin)

### Medicines - Add (3 min)
- [ ] Go to Medicines → Tab 2: Add Medicine
- [ ] Fill form:
  - Name: Ibuprofen
  - Category: Painkillers
  - Price: 75
  - Cost Price: 45
  - Wholesale: 40
  - Quantity: 200
  - Expiry: 2025-12-31
- [ ] Submit
- [ ] Verify "Profit: ₹30 (40%)" displays
- [ ] Confirm medicine appears in Tab 1

### Medicines - Expired (2 min)
- [ ] Go to Medicines → Tab 4: Expired Medicines
- [ ] Check for expired items
- [ ] See 30-day upcoming expiry warnings
- [ ] Test individual delete
- [ ] Test bulk delete (if any expired exist)

### Customers (2 min)
- [ ] Go to Customers
- [ ] Click "View Customers"
- [ ] See 10 customers with details
- [ ] Click "Add Customer"
- [ ] Fill form and submit
- [ ] Verify new customer appears

### Billing - Create (5 min)
**THIS IS THE KEY TEST - Shows profit tracking and coupons!**

1. [ ] Go to Billing
2. [ ] Select customer "Rajesh Kumar"
3. [ ] Search and add:
   - Aspirin (₹50) × 2
   - Vitamin D3 (₹200) × 1
4. [ ] See cart summary:
   - Items: 2
   - Total: ₹300
5. [ ] Apply coupon "SAVE10" (10%)
6. [ ] See billing summary with:
   - Subtotal: ₹300
   - Manual Discount: ₹0
   - Coupon Discount: ₹30
   - **Total to Pay: ₹270**
   - **Cost Price: ₹185**
   - **Estimated Profit: ₹85 (31.5%)**
7. [ ] Select payment method "UPI"
8. [ ] Click "Create Bill"
9. [ ] See success message
10. [ ] Download PDF bill
11. [ ] Verify PDF contains all items and discounts

### Billing - Coupon (2 min)
- [ ] In Billing page, scroll to "Apply Coupon"
- [ ] Dropdown shows:
  - SAVE10 (percentage: 10.0)
  - SAVE50 (fixed: 50.0)
  - FLAT20 (percentage: 20.0)
  - WELCOME (fixed: 100.0)
  - SUMMER25 (percentage: 25.0)
- [ ] Select each and verify calculation updates
- [ ] Test with no discount vs discount

### Financial Analysis - Profit (3 min)
**NEW PAGE - Tests profit tracking!**

1. [ ] Go to Financial Analysis
2. [ ] Tab 1: Profit & Revenue
3. [ ] See metrics:
   - Total Sales (sum of all bills)
   - Total Cost (sum of cost prices)
   - Gross Profit (Sales - Cost)
   - Profit Margin %
4. [ ] See "Daily Profit Trend" chart
5. [ ] See category breakdown pie charts
6. [ ] Verify Paracetamol profit > Aspirin profit

### Financial Analysis - Payments (2 min)
1. [ ] Tab 2: Payment Methods
2. [ ] See payment breakdown:
   - Cash, Card, UPI, others
3. [ ] Pie chart shows distribution
4. [ ] Table shows counts and amounts

### Financial Analysis - Trends (2 min)
1. [ ] Tab 3: Sales Trends
2. [ ] Select "Month" period
3. [ ] See metrics:
   - Current month sales
   - % change from previous month
   - 📈 INCREASED or 📉 DECREASED
4. [ ] Tab shows Top 10 products

### Financial Analysis - Report (2 min)
1. [ ] Tab 4: Detailed Report
2. [ ] Select date range
3. [ ] See daily breakdown:
   - Date, Bills, Sales, Discount, Cost, Profit
4. [ ] Click "Download Report"
5. [ ] CSV file downloads successfully

### Suppliers (3 min)
1. [ ] Go to Suppliers
2. [ ] Tab 1: View 5 suppliers
   - Pharma Direct Ltd (Mumbai)
   - Global Medicines Co (Delhi)
   - HealthCare Suppliers (Bangalore)
   - Medical Distributors (Pune)
   - Premium Pharma Group (Chennai)
3. [ ] Tab 2: Try adding supplier
   - Fill form and submit
4. [ ] Tab 3: Create purchase order
   - Select supplier
   - Add medicines with quantity/cost
   - Submit

### Promotions - Coupons (2 min)
1. [ ] Go to Promotions
2. [ ] Tab 1: See 5 active + 2 expired coupons
   - SAVE10, SAVE50, FLAT20, WELCOME, SUMMER25
3. [ ] See columns: Code, Type, Value, Usage, Valid Until
4. [ ] Test creating new coupon

### Promotions - Offers (2 min)
1. [ ] Tab 2: See 5 offers
   - Painkillers (10%)
   - Vitamins (15%)
   - Antibiotics (₹50)
   - Cardiac (20%)
   - Respiratory (12%)
2. [ ] Test creating new offer

### Promotions - Statistics (2 min)
1. [ ] Tab 3: Usage Statistics
2. [ ] See coupon performance metrics
3. [ ] View most/least used coupons

### Promotions - Cleanup (1 min)
1. [ ] Tab 4: Expired Promotions
2. [ ] See expired coupons listed
3. [ ] Test bulk delete

### Reports (3 min)
1. [ ] Go to Reports
2. [ ] Tab 1: Top Medicines
   - Shows units sold and revenue
   - Table with sorting
3. [ ] Tab 2: Top Customers
   - Shows customers by purchase value
4. [ ] Tab 3: Sales by Category
   - Pie chart showing category distribution
5. [ ] Tab 4: Low Stock
   - Shows items below 10 units

---

## 🔍 Verification Commands

### Check Installation
```bash
# Verify Python version
python --version
# Should be 3.10+

# Verify venv activated
which python
# Should show path with /venv/

# Verify packages
pip list | grep streamlit
pip list | grep pandas
pip list | grep plotly
```

### Check Database
```bash
# Count records
python -c "
import sqlite3
conn = sqlite3.connect('pharmacy.db')
c = conn.cursor()
tables = ['users', 'medicines', 'customers', 'suppliers', 'bills', 'coupons', 'offers']
for table in tables:
    c.execute(f'SELECT COUNT(*) FROM {table}')
    count = c.fetchone()[0]
    print(f'{table}: {count}')
conn.close()
"

# Should show:
# users: 1
# medicines: 15
# customers: 10
# suppliers: 5
# bills: 15
# coupons: 7
# offers: 5
```

### Check File Structure
```bash
# Verify all pages exist
ls -la pages/

# Should show:
# billing.py
# customers.py
# dashboard.py
# financials.py (NEW!)
# medicines.py
# promotions.py (NEW!)
# reports.py
# suppliers.py (NEW!)
```

---

## 📊 Expected Test Results

### Database Verification
✅ **Users**: 1 (admin)
✅ **Medicines**: 15 with cost/wholesale pricing
✅ **Customers**: 10 with contact details
✅ **Bills**: 15 transactions
✅ **Suppliers**: 5 suppliers
✅ **Coupons**: 7 (5 active, 2 expired)
✅ **Offers**: 5 category-wise
✅ **Bill Items**: 27 line items

### Financial Verification
✅ **Profit Calculation**: Selling - Cost
✅ **Margins**: 38-44% on sample medicines
✅ **Coupons**: All discounts apply correctly
✅ **Payment Methods**: All 5 types tracked
✅ **Sales Trends**: Daily/weekly/monthly comparison

### UI Verification
✅ **Login**: Works with admin/1234
✅ **Navigation**: All pages accessible
✅ **Charts**: Plotly visualizations load
✅ **Forms**: Validation works
✅ **PDF**: Downloads successfully

---

## 🐛 Troubleshooting

### Issue: Module not found
```bash
# Solution: Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database errors
```bash
# Solution: Reinitialize database
rm pharmacy.db
python database/db.py
```

### Issue: Port 8501 already in use
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

### Issue: Permission denied
```bash
# Solution: Make script executable
chmod +x app.py
chmod +x database/db.py
```

### Issue: Slow performance
- Close other applications
- Clear browser cache (Ctrl+Shift+Delete)
- Restart terminal and Streamlit

---

## 📈 Performance Benchmarks

| Task | Expected Time | Threshold |
|------|---|---|
| Load Dashboard | < 2s | 5s |
| Create Bill | < 3s | 10s |
| Download PDF | < 1s | 5s |
| Generate Report | < 2s | 10s |
| Search Medicines | < 1s | 5s |
| Apply Coupon | < 1s | 5s |

---

## 🔐 Security Verification

- [ ] Passwords hashed (SHA256)
- [ ] SQL parameterized queries
- [ ] Session-based auth
- [ ] No sensitive data in logs
- [ ] Files have correct permissions

---

## 📝 Post-Installation Steps

1. **Backup Database**
   ```bash
   cp pharmacy.db pharmacy.db.backup
   ```

2. **Customize Sample Data**
   - Edit database/db.py
   - Modify medicines, customers, suppliers lists
   - Run `python database/db.py` to regenerate

3. **Update Configuration**
   - Edit config.py
   - Change CURRENCY if needed
   - Adjust LOW_STOCK_THRESHOLD

4. **Test Real Workflows**
   - Create actual customer records
   - Add real medicines
   - Process test transactions
   - Verify profit calculations

5. **Monitor Performance**
   - Check database size: `ls -lh pharmacy.db`
   - Monitor response times
   - Scale to PostgreSQL if needed

---

## 🎓 Learning Resources

- **database/db.py**: Database schema and sample data
- **config.py**: Configuration reference
- **styles.py**: CSS styling
- **services/*.py**: Business logic
- **pages/*.py**: Page-specific code

---

## 📞 Support Checklist

If issues persist:
1. [ ] Check Python version >= 3.10
2. [ ] Verify virtual environment activated
3. [ ] Confirm all packages installed
4. [ ] Reinitialize database
5. [ ] Check file permissions
6. [ ] Review terminal error messages
7. [ ] Try different port number
8. [ ] Clear cache and restart

---

## ✨ Success Indicators

✅ **Setup Successful When:**
- App starts without errors
- Login works with admin/1234
- All pages load and display correctly
- Database contains sample data
- Profit calculations are accurate
- Coupons apply correctly
- PDF downloads successfully
- Charts render properly
- No console errors

---

**Version**: 2.0  
**Last Updated**: March 2024  
**Status**: Production Ready ✅
