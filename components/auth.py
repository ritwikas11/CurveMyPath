import streamlit as st

def login_ui():
    if "user_id" not in st.session_state:
        st.title("🎓 CurveMyPath")
        st.write("A simple course recommender for OVGU students.")
        user_input = st.text_input("Enter your name to personalize your dashboard:")
        
        if user_input:
            st.session_state["user_id"] = user_input
            st.success(f"Welcome, {user_input}! Your session has started.")
            st.rerun()  # 🔁 force rerun to show dashboard immediately

        st.caption("🔐 This is just to personalize your dashboard. No data is stored permanently or shared.")
        st.stop()
