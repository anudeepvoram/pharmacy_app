"""
Global configuration and constants for Pharmacy Management System
"""

# Color Palette - Professional Medical Theme
COLORS = {
    "primary": "#0066CC",           # Professional Blue
    "secondary": "#00A86B",         # Medical Green
    "accent": "#FF6B6B",            # Alert Red
    "warning": "#FFA500",           # Warning Orange
    "success": "#27AE60",           # Success Green
    "danger": "#E74C3C",            # Danger Red
    "light_bg": "#F8F9FA",          # Light Background
    "dark_text": "#2C3E50",         # Dark Text
    "border": "#E0E0E0",            # Border Gray
    "shadow": "rgba(0, 0, 0, 0.1)", # Shadow
}

# App Configuration
APP_NAME = "Pharmacy Management System"
APP_ICON = "💊"
APP_DESCRIPTION = "Professional pharmacy inventory and billing management system"

# Database
DB_NAME = "pharmacy.db"

# Default Credentials (Change in production!)
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "1234"

# Low Stock Threshold
LOW_STOCK_THRESHOLD = 10

# Expiry Alert Days
EXPIRY_ALERT_DAYS = 30

# Currency Symbol
CURRENCY = "₹"
