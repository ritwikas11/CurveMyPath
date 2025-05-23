import streamlit as st
import json
import os

USER_DB = "data/users.json"

def login_ui():
    # Load users file or create one
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({"test@ovgu.de": {"password": "1234"}}, f)

    with open(USER_DB, "r") as f:
        users = json.load(f)

    if "user_id" not in st.session_state:
        st.title("🎓 CurveMyPath")
        st.write("A smart course recommender for OVGU students.")
        st.markdown("#### 🔐 Login to access your personalized dashboard:")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email in users and users[email]["password"] == password:
                st.session_state["user_id"] = email
                st.success(f"Welcome, {email}! Your session has started.")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

        st.caption("👤 New user? Contact admin to get access (for now, email/password check is manual).")
        st.stop()
