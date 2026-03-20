import streamlit as st
import sqlite3
import hashlib
from styles import apply_global_styles, success_message, error_message, warning_message
from config import APP_NAME, APP_ICON, DB_NAME


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored_hash, provided_password):
    """Verify password against stored hash"""
    return stored_hash == hashlib.sha256(provided_password.encode()).hexdigest()


def user_exists(username):
    """Check if username exists"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def email_exists(email):
    """Check if email exists"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def register_user(username, email, password, full_name):
    """Register new user"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, full_name, role)
        VALUES (?, ?, ?, ?, ?)
        """, (username, email, hash_password(password), full_name, 'pharmacist'))
        
        conn.commit()
        return True, "Registration successful! You can now login."
    except sqlite3.IntegrityError as e:
        return False, "Username or email already exists."
    except Exception as e:
        return False, f"Registration error: {str(e)}"
    finally:
        conn.close()


def authenticate_user(username, password):
    """Authenticate user and return user info"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, username, email, full_name, role FROM users WHERE username = ? AND is_active = 1",
            (username,)
        )
        user = cursor.fetchone()
        
        if user:
            user_id, uname, uemail, ufull_name, urole = user
            # Get password hash
            cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
            stored_hash = cursor.fetchone()[0]
            
            if verify_password(stored_hash, password):
                return True, {
                    'id': user_id,
                    'username': uname,
                    'email': uemail,
                    'full_name': ufull_name,
                    'role': urole
                }
        
        return False, None
    except Exception as e:
        return False, None
    finally:
        conn.close()


def login():
    """Professional login/signup interface"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if not st.session_state.logged_in:
        apply_global_styles()
        
        # Create centered login container
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            login_html = f"""
            <style>
            .login-container {{
                background: linear-gradient(135deg, #0066CC 0%, #00A86B 100%);
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
            }}
            .login-title {{
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                color: white;
            }}
            .login-subtitle {{
                font-size: 1rem;
                margin: 0.5rem 0 0 0;
                opacity: 0.95;
            }}
            </style>
            <div class="login-container">
                <div class="login-title">💊 {APP_NAME}</div>
                <div class="login-subtitle">Professional Pharmacy Management System</div>
            </div>
            """
            st.markdown(login_html, unsafe_allow_html=True)
            
            # Tab selection
            tab1, tab2 = st.tabs(["🔓 Login", "✍️ Sign Up"])
            
            with tab1:
                st.markdown("### Login to Your Account")
                
                with st.form("login_form", clear_on_submit=True):
                    username = st.text_input(
                        "👤 Username",
                        placeholder="Enter your username",
                        key="login_username"
                    )
                    password = st.text_input(
                        "🔐 Password",
                        type="password",
                        placeholder="Enter your password",
                        key="login_password"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        login_btn = st.form_submit_button(
                            "🔓 Login",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.form_submit_button(
                            "🔄 Clear",
                            use_container_width=True,
                            disabled=True
                        )
                    
                    if login_btn:
                        if not username or not password:
                            error_message("Please enter both username and password.")
                        else:
                            success, user_info = authenticate_user(username, password)
                            if success:
                                st.session_state.logged_in = True
                                st.session_state.user_info = user_info
                                success_message(f"✅ Welcome back, {user_info['full_name']}!")
                                st.rerun()
                            else:
                                error_message("❌ Invalid username or password. Please try again.")
                
                st.markdown("---")
                st.info("📋 Demo Login: **Username:** admin | **Password:** 1234")
                st.markdown("Don't have an account? Sign up using the **Sign Up** tab →")
            
            with tab2:
                st.markdown("### Create New Account")
                
                with st.form("signup_form", clear_on_submit=True):
                    full_name = st.text_input(
                        "👤 Full Name",
                        placeholder="e.g., John Doe",
                        key="signup_name"
                    )
                    
                    email = st.text_input(
                        "📧 Email Address",
                        placeholder="e.g., john@example.com",
                        key="signup_email"
                    )
                    
                    username = st.text_input(
                        "👤 Username",
                        placeholder="Choose a username",
                        key="signup_username"
                    )
                    
                    password = st.text_input(
                        "🔐 Password",
                        type="password",
                        placeholder="Create a strong password (min 6 chars)",
                        key="signup_password"
                    )
                    
                    confirm_password = st.text_input(
                        "🔐 Confirm Password",
                        type="password",
                        placeholder="Re-enter your password",
                        key="signup_confirm"
                    )
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        signup_btn = st.form_submit_button(
                            "✍️ Create Account",
                            use_container_width=True
                        )
                    with col2:
                        st.form_submit_button(
                            "🔄 Clear",
                            use_container_width=True,
                            disabled=True
                        )
                    
                    if signup_btn:
                        # Validation
                        if not all([full_name, email, username, password, confirm_password]):
                            error_message("⚠️ Please fill all fields.")
                        
                        elif len(full_name.strip()) < 2:
                            error_message("⚠️ Full name must be at least 2 characters.")
                        
                        elif len(username.strip()) < 3:
                            error_message("⚠️ Username must be at least 3 characters.")
                        
                        elif len(password) < 6:
                            error_message("⚠️ Password must be at least 6 characters.")
                        
                        elif password != confirm_password:
                            error_message("⚠️ Passwords do not match.")
                        
                        elif "@" not in email or "." not in email:
                            error_message("⚠️ Please enter a valid email address.")
                        
                        elif user_exists(username):
                            error_message("⚠️ Username already exists. Try a different one.")
                        
                        elif email_exists(email):
                            error_message("⚠️ Email already registered. Use login instead.")
                        
                        else:
                            # Register user
                            success, message = register_user(
                                username.strip(),
                                email.strip(),
                                password,
                                full_name.strip()
                            )
                            
                            if success:
                                success_message(f"✅ {message}")
                                st.info("👉 Please switch to the **Login** tab to login with your credentials.")
                            else:
                                error_message(f"❌ {message}")
        
        st.stop()