import streamlit as st
import os
from groq import Groq
import sqlite3
from datetime import datetime
from config import DB_NAME, CURRENCY
from styles import apply_global_styles, sidebar_header, section_header, error_message

st.set_page_config(page_title="AI Assistant", layout="centered")
apply_global_styles()

# Try to load .env file if it exists globally
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                key, val = line.strip().split("=", 1)
                os.environ[key.strip()] = val.strip().strip("'\"")

# Put your hardcoded key here OR use environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_hardcoded_key_here")

# Define available models exactly as requested
AVAILABLE_MODELS = [
    "whisper-large-v3-turbo",
    "whisper-large-v3",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

with st.sidebar:
    sidebar_header()
    st.markdown("---")
    
    st.markdown("### Model Selection")
    # Default to openai/gpt-oss-120b (index 3)
    selected_model = st.selectbox("Choose AI Model", AVAILABLE_MODELS, index=3)

st.title("🤖 AI Pharmacy Assistant")
st.markdown(f"Powered by Groq Cloud (`{selected_model}`)")
section_header("Chat", "💬")

def get_db_context():
    try:
        conn = sqlite3.connect(DB_NAME)
        this_month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Monthly sales
        m_sales = conn.execute("SELECT SUM(total_amount), COUNT(id) FROM bills WHERE DATE(created_at) >= ?", (this_month_start,)).fetchone()
        
        # Today's sales
        t_sales = conn.execute("SELECT SUM(total_amount), COUNT(id) FROM bills WHERE DATE(created_at) = ?", (today,)).fetchone()
        
        # Top 3 products this month
        top_m = conn.execute("""
            SELECT m.name, SUM(bi.quantity) FROM bill_items bi 
            JOIN bills b ON bi.bill_id = b.id JOIN medicines m ON bi.medicine_id = m.id 
            WHERE DATE(b.created_at) >= ? GROUP BY m.id ORDER BY SUM(bi.quantity) DESC LIMIT 3
        """, (this_month_start,)).fetchall()
        
        # Out of stock
        oos = conn.execute("SELECT COUNT(id) FROM medicines WHERE quantity = 0").fetchone()[0]
        
        conn.close()
        
        ctx = f"System Context (Real-time DB):\n"
        ctx += f"- Current Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        ctx += f"- This Month's Sales (Since {this_month_start}): {m_sales[1]} transactions totaling {CURRENCY}{m_sales[0] or 0:.2f}.\n"
        ctx += f"- Today's Sales: {t_sales[1]} transactions totaling {CURRENCY}{t_sales[0] or 0:.2f}.\n"
        ctx += f"- Top 3 products this month: {', '.join([f'{r[0]} ({r[1]} units)' for r in top_m]) if top_m else 'None'}\n"
        ctx += f"- Out of stock medicines: {oos}\n"
        ctx += "Use this exact data when answering questions about sales, inventory, or pharmacy metrics!"
        return ctx
    except Exception as e:
        return f"System Context: [DB Unavailable - {str(e)}]"

persona = (
    "You are a friendly, conversational pharmacy assistant. "
    "Do NOT talk like a typical AI bot. Avoid overwhelming the user with massive bulleted lists, "
    "headers, or overly formal markdown tables unless absolutely necessary. Speak naturally, directly, "
    "and concisely like a real human manager. Use a warm tone. ALWAYS base your answers on the "
    "provided System Context."
)

if "messages" not in st.session_state:
    db_ctx = get_db_context()
    st.session_state.messages = [
        {
            "role": "system", 
            "content": f"{persona}\n\n{db_ctx}"
        }
    ]
else:
    # Always keep system prompt updated with the latest live data silently
    st.session_state.messages[0]["content"] = f"{persona}\n\n{get_db_context()}"

# Display chat messages (skip system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me about medicines, management, or health advice..."):
    if not GROQ_API_KEY or GROQ_API_KEY == "your_hardcoded_key_here":
        error_message("Please set your GROQ_API_KEY in the code (line 15) or environment variables before using the chat.")
    else:
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Call Groq API
        try:
            client = Groq(api_key=GROQ_API_KEY)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Check if it's a Whisper text-generation misuse (Whisper strictly is for audio).
                # But if requested, we'll pipe it normally. It might throw an error from Groq.
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True,
                )
                
                # Stream the response
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            # Add assistant response to state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message(f"API Error: {str(e)}")
