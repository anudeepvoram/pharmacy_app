#!/bin/bash
# Quick Start Script for Pharmacy Management System
# Run this script to set up and start the application

set -e  # Exit on error

echo "======================================"
echo "💊 Pharmacy Management System Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "🗄️  Initializing database..."
python3 setup.py

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo "======================================"
echo ""
echo "To start the application, run:"
echo "  streamlit run app.py"
echo ""
echo "Default login:"
echo "  Username: admin"
echo "  Password: 1234"
echo ""
echo "======================================"
