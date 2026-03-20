import streamlit as st
from auth import login
from styles import apply_global_styles, sidebar_header, info_message
from config import APP_NAME, APP_ICON, APP_DESCRIPTION
from database.db import create_tables, add_default_admin

# Configure page
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure database schema exists before anything else
create_tables()
add_default_admin()

# Apply professional styling
apply_global_styles()

# Authenticate user
login()

# Sidebar header
with st.sidebar:
    sidebar_header()
    st.markdown("---")
    st.markdown("**Quick Navigation**")

# Main content
st.title(f"{APP_ICON} {APP_NAME}")
st.markdown(f"*{APP_DESCRIPTION}*")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Status", "Active", "System Healthy")
with col2:
    st.metric("👥 Users", "1", "You")
with col3:
    st.metric("🔐 Security", "Enabled", "Protected")

st.markdown("---")
info_message("Use the navigation menu in the sidebar to access different modules.")