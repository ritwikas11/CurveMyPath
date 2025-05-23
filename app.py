import streamlit as st
from components import roadmap_builder, recommender
from components import auth, recommender, progress

st.set_page_config(page_title="CurveMyPath", layout="centered")

# Login or Welcome screen
auth.login_ui()

# Main dashboard
st.title("🎓 CurveMyPath")
st.write("A simple course recommender for OVGU students. A career planner powered by AI 🚀")
st.markdown("---")

# Recommendation section
recommender.select_goal()

# Progress tracker
#progress.show_progress()

# Get the current goal from session state BEFORE calling display
current_goal = st.session_state.get("current_goal")

# AI-generated Roadmap
roadmap_builder.display_ai_roadmap(current_goal)

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.warning("🚧 Dashboard is under construction: This is an MVP. We're actively working to improve it!")
with col2:
    if st.button("💬 Give feedback"):
        st.write("Email us at: team@curvemypath.com")