# 🚀 Quick Start Guide

Get your pharmacy management system up and running in 5 minutes!

## Installation (5 minutes)

### Step 1: Clone/Enter Project
```bash
cd /Users/anudeep/Desktop/pharmacy_app
```

### Step 2: Setup Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python database/db.py
```

This creates:
- Database file (pharmacy.db)
- All tables with schema
- 15 sample medicines
- 10 sample customers
- 15 sample bills
- 5 sample suppliers
- 7 sample coupons
- 5 sample offers

### Step 5: Run Application
```bash
streamlit run app.py
```

Opens automatically at: **http://localhost:8501**

---

## 🔐 Default Login

```
Username: admin
Password: 1234
```

---

## 🎯 First Steps (What to Try)

### 1. Explore Dashboard (2 min)
- Navigate to **Dashboard** (home page)
- See system overview with 4 KPIs
- Check low stock alerts
- View expiry warnings

### 2. Browse Medicines (2 min)
- Go to **Medicines**
- Click **Tab 1** to search and view medicines
- Try searching "Aspirin"
- See pricing tiers (Cost, Retail, Wholesale)

### 3. Create a Bill (5 min)
- Go to **Billing**
- Select customer "Rajesh Kumar"
- Search and add "Aspirin" (₹50)
- Add "Vitamin D3" (₹200)
- Apply coupon "SAVE10" (10% off)
- See profit calculation
- Choose payment method "UPI"
- Click "Create Bill"
- **Download PDF invoice!**

### 4. Check Analytics (3 min)
- Go to **Financial Analysis** (new page!)
- See daily profit trend
- Check category-wise profit breakdown
- View payment method distribution
- Switch to "Sales Trends" tab
- Download report as CSV

### 5. Manage Suppliers (2 min)
- Go to **Suppliers**
- View 5 sample suppliers
- Check Tab 2 to add supplier
- See Tab 3 for purchase orders

### 6. Review Coupons (2 min)
- Go to **Promotions**
- Click **Tab 1** to see active coupons
- Check **Tab 2** for offers
- View **Tab 3** for usage statistics

---

## 💡 Common Tasks

### How to Add a New Medicine
1. Go to **Medicines** → **Tab 2: Add Medicine**
2. Fill in:
   - Medicine Name: "Aspirin"
   - Category: "Painkillers"
   - Selling Price: ₹50
   - **Cost Price: ₹30** (NEW!)
   - **Wholesale Price: ₹25** (NEW!)
   - Quantity: 100
   - Expiry Date: 2025-12-31
3. Click "Add Medicine"
4. See instant profit calculation: ₹20 (40%)

### How to Create a Bill
1. Go to **Billing**
2. Select customer from dropdown
3. Search and add medicines to cart
4. Apply manual discount (optional)
5. Apply coupon (if available)
6. Select payment method
7. Review profit in summary
8. Click "Create Bill"
9. Download PDF automatically

### How to Apply a Coupon
1. When creating a bill, scroll to "Billing Details"
2. Find "Apply Coupon" dropdown in 3rd column
3. Select coupon (shows type and value)
4. Summary auto-updates with coupon discount
5. Total shows both manual + coupon discounts

### How to Track Profit
1. In **Billing**: See "Estimated Profit" in summary
2. In **Financial Analysis**: 
   - Tab 1: Daily profit trends and category breakdown
   - See profit margin percentage
3. In **Reports**: Top products by revenue

### How to Manage Expired Medicines
1. Go to **Medicines** → **Tab 4: Expired Medicines**
2. See all expired medicines
3. Click delete icon for individual delete
4. Use "Bulk Delete" for multiple items
5. Also see 30-day upcoming expiry warnings

---

## 📊 Key Dashboards

### Financial Analysis Page (NEW!)
**Best for:** Profit tracking and financial reporting

**4 Tabs:**
1. **Profit & Revenue**: Daily trends, category breakdown
2. **Payment Methods**: Payment type distribution
3. **Sales Trends**: Week/Month/Quarter comparison
4. **Detailed Report**: Downloadable CSV with all metrics

**Key Metrics:**
- Total Sales & Cost
- Gross Profit
- Profit Margin %
- Daily profit trend chart
- Category-wise breakdown

### Suppliers Page (NEW!)
**Best for:** Inventory replenishment

**3 Tabs:**
1. **Supplier Directory**: Search/filter 5 suppliers
2. **Add Supplier**: New supplier registration
3. **Purchase Orders**: Create and track POs

### Promotions Page (NEW!)
**Best for:** Coupon and offer management

**4 Tabs:**
1. **Manage Coupons**: Active and expired coupons
2. **Manage Offers**: Category-wise discounts
3. **Usage Statistics**: Coupon performance metrics
4. **Expired Promotions**: Cleanup and deletion

---

## 🎨 Interface Tips

### Navigation
- **Sidebar**: Click pages to navigate
- **Logo**: Click to go to Dashboard
- **Logout**: Top-right in sidebar

### Input Validation
- 🟢 Green = Success
- 🔴 Red = Error
- 🟡 Yellow = Warning
- 🔵 Blue = Info

### Charts
- Hover over charts for details
- Click legend items to hide/show
- Use dropdown filters for date ranges

---

## 💾 Sample Data Reference

### Medicines (15)
- Painkillers: Aspirin (₹50), Ibuprofen (₹75), Paracetamol (₹45)
- Antibiotics: Amoxicillin (₹120), Cephalexin (₹150)
- Vitamins: Vitamin D3 (₹200), Vitamin B12 (₹180)
- And 8 more across 5 categories

### Customers (10)
- Rajesh Kumar, Priya Singh, Amit Patel, Neha Sharma, Vikram Gupta
- Anjali Verma, Rohit Desai, Divya Menon, Arjun Nair, Sneha Reddy

### Coupons (7)
- **Active**: SAVE10, SAVE50, FLAT20, WELCOME, SUMMER25
- **Expired**: EXPIREDCOUP, LASTCHANCE

### Suppliers (5)
- Pharma Direct Ltd (Mumbai)
- Global Medicines Co (Delhi)
- HealthCare Suppliers (Bangalore)
- Medical Distributors (Pune)
- Premium Pharma Group (Chennai)

### Offers (5)
- Painkillers 10% off
- Vitamins 15% off
- Antibiotics ₹50 off
- Cardiac Meds 20% off
- Respiratory 12% off

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
# Reactivate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Reinitialize database (deletes old data)
rm pharmacy.db
python database/db.py
```

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Slow performance
- Close other applications
- Clear browser cache
- Restart Streamlit

---

## 📚 Learn More

- **README.md**: Full documentation
- **FEATURES.md**: Complete feature list
- **database/db.py**: Database schema and sample data
- **config.py**: Configuration settings
- **styles.py**: UI styling

---

## ✨ What's New in v2.0

### Financial Features
- ✅ Profit calculation (Retail - Cost)
- ✅ Profit margin tracking
- ✅ Wholesale pricing support
- ✅ Tax amount tracking

### New Pages
- ✅ **Financial Analysis**: Profit dashboards and trends
- ✅ **Suppliers**: Supplier management and POs
- ✅ **Promotions**: Coupon and offer management

### Billing Enhancements
- ✅ Multiple discount types (manual + coupon)
- ✅ Real-time profit display
- ✅ Coupon integration

### Medicine Features
- ✅ Expired medicine bulk delete
- ✅ Cost/wholesale pricing
- ✅ 30-day expiry warnings

### Analytics
- ✅ Daily profit trends
- ✅ Payment method breakdown
- ✅ Sales trend comparison
- ✅ CSV reports

---

## 🎓 Next Steps

1. **Customize Sample Data**
   - Edit medicines, customers in database/db.py
   - Run `python database/db.py` to regenerate

2. **Add Your Medicines**
   - Use Medicines page to add real inventory
   - Set accurate cost prices for profit tracking

3. **Register Real Customers**
   - Add your pharmacy's actual customers
   - Build transaction history

4. **Create Promotional Coupons**
   - Design seasonal offers
   - Track usage statistics

5. **Monitor Financials**
   - Check Financial Analysis daily
   - Identify top-selling medicines
   - Track payment trends

---

## 🔗 Quick Links

- **Dashboard**: Overview of system
- **Medicines**: Inventory management with 3 pricing tiers
- **Billing**: Create invoices with profit tracking
- **Financial Analysis**: Profit dashboards and trends
- **Suppliers**: Purchase order management
- **Promotions**: Coupon and offer management
- **Reports**: Sales analytics

---

## 📞 Support

Having issues? Check:
1. Terminal output for error messages
2. README.md for detailed info
3. FEATURES.md for feature details
4. Database logs in pharmacy.db

---

**Happy selling! 💊**

Version 2.0 - Production Ready  
Last Updated: March 2024
