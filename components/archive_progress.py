import streamlit as st

def show_progress():
    if not st.session_state.get("show_progress"):
        return  # do not show unless explicitly triggered

    st.markdown("### 📊 Your Progress This Session:")
    if "goals_selected" in st.session_state:
        st.write(f"Goals Selected: {len(st.session_state['goals_selected'])}")
        st.write("Goals:", st.session_state["goals_selected"])
    else:
        st.write("No goals selected yet.")

    st.caption("🛡️ Your data is stored only during this session for a better experience. You’re in control.")
