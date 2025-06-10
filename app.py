import streamlit as st
from components import auth, roadmap_builder, recommender
from components.ai_chatbox import ai_chatbox

st.set_page_config(page_title="CurveMyPath", layout="centered")

# Login or Welcome screen
auth.login_ui()

# Header
st.title("🎓 CurveMyPath")
st.write("A simple course recommender for OVGU students. A career planner powered by AI 🚀")
st.markdown("---")

#AI Chatbox
ai_chatbox()

# Recommendation section
recommender.select_goal()

# Conditionally show roadmap only if button was clicked
if st.session_state.get("show_roadmap") and st.session_state.get("current_goal"):
    roadmap_builder.display_ai_roadmap(st.session_state["current_goal"])

# Footer
st.markdown("---")
if st.button("💬 Give feedback"):
    st.write("Email us at: team@curvemypath.com")