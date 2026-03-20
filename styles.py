"""
Professional styling module for Pharmacy Management System
Provides consistent theming and UI components across the application
"""

import streamlit as st
from config import COLORS


def apply_global_styles():
    """Apply professional CSS styling globally"""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --primary-color: {COLORS['primary']};
        --secondary-color: {COLORS['secondary']};
        --accent-color: {COLORS['accent']};
        --warning-color: {COLORS['warning']};
        --success-color: {COLORS['success']};
        --danger-color: {COLORS['danger']};
        --light-bg: {COLORS['light_bg']};
        --dark-text: {COLORS['dark_text']};
        --border-color: {COLORS['border']};
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}

    /* Overall styling */
    html, body, [class*="css"]  {{
        background-color: {COLORS['light_bg']};
        color: {COLORS['dark_text']};
        font-family: var(--font-family);
        font-weight: 500;
        -webkit-font-smoothing: antialiased;
    }}

    /* Main container */
    .main {{
        background-color: {COLORS['light_bg']};
        padding: 2rem;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary']} 0%, #004488 100%);
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: white;
    }}
    
    [data-testid="stSidebarNav"] span {{
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.3px;
        color: #f0f4f8;
    }}

    /* Title and Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['primary']};
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin-bottom: 1.5rem;
    }}

    h1 {{
        border-bottom: 4px solid {COLORS['secondary']};
        padding-bottom: 1rem;
        background: -webkit-linear-gradient(45deg, {COLORS['primary']}, {COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Cards */
    .card {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(224, 224, 224, 0.5);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }}

    .card:hover {{
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.1);
        transform: translateY(-4px);
    }}

    /* Metrics */
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 6px solid {COLORS['primary']};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }}

    [data-testid="metric-container"] {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 6px solid {COLORS['primary']};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    [data-testid="metric-container"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }}

    /* Streamlit Metric Overrides */
    [data-testid="stMetricValue"] {{
        font-weight: 800;
        color: {COLORS['primary']};
    }}
    [data-testid="stMetricLabel"] {{
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #005bb5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-transform: uppercase;
        font-size: 0.95rem;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, #005bb5 0%, #004488 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4);
    }}

    .stButton > button:active {{
        transform: translateY(1px);
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }}

    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        background-color: #fdfdfd;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.15);
        background-color: #ffffff;
    }}

    /* Form Labels */
    label, .stMarkdown p {{
        font-weight: 600 !important;
    }}

    /* Data table styling */
    [data-testid="dataframeContainer"] {{
        margin-bottom: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        border: 1px solid {COLORS['border']};
    }}

    /* AMAZING TAB BUTTONS STYLING */
    /* This transforms the default ugly Streamlit tabs into a professional segmented control/buttons */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-bottom: none;
        background-color: #eeeeee;
        padding: 0.5rem;
        border-radius: 12px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        flex-wrap: wrap;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 8px;
        color: {COLORS['dark_text']};
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(0, 0, 0, 0.05);
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #005bb5 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
        border-bottom: none !important;
        transform: translateY(-1px);
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}

    /* Form Containers */
    [data-testid="stForm"] {{
        background-color: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(224, 224, 224, 0.5);
    }}

    /* Divider */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS['border']}, transparent);
        margin: 2.5rem 0;
    }}

    /* Badge styling */
    .badge {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 0.25rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def sidebar_header():
    """Display professional sidebar header"""
    st.markdown("""
    <style>
    .sidebar-header {
        color: white;
        padding: 2rem 0 1.5rem 0;
        text-align: center;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    .sidebar-header h1 {
        color: white;
        border: none;
        margin: 0;
        font-size: 1.8rem;
    }
    .sidebar-header p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    </style>
    <div class="sidebar-header">
        <h1>💊 Pharmacy System</h1>
        <p>Professional Management</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "", change: str = ""):
    """Display professional metric card"""
    col = st.container()
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <p style="margin: 0; color: {COLORS['dark_text']}; font-size: 0.9rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">
                        {icon} {label}
                    </p>
                    <h2 style="margin: 0.5rem 0 0 0; color: {COLORS['primary']}; font-size: 2rem; font-weight: 700;">
                        {value}
                    </h2>
                </div>
                {f'<div style="color: {COLORS["success"]}; font-size: 0.85rem; font-weight: 600;">{change}</div>' if change else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)


def success_message(message: str):
    """Display professional success message"""
    st.success(f"✅ {message}")


def error_message(message: str):
    """Display professional error message"""
    st.error(f"❌ {message}")


def warning_message(message: str):
    """Display professional warning message"""
    st.warning(f"⚠️ {message}")


def info_message(message: str):
    """Display professional info message"""
    st.info(f"ℹ️ {message}")


def section_header(title: str, icon: str = ""):
    """Display professional section header"""
    st.markdown(f"### {icon} {title}")
    st.markdown("---")


def container_card():
    """Context manager for card container"""
    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)
