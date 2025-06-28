import os
import json
import streamlit as st
from datetime import datetime
from components import auth, roadmap_builder, recommender
from components.ai_chatbox import ai_chatbox

FEEDBACK_FILE = os.path.join("data", "feedback.json")

st.set_page_config(page_title="CurveMyPath", layout="centered")

# Login or Welcome screen
auth.login_ui()

# Header
st.title("🎓 CurveMyPath")
st.write("A simple course recommender for OVGU Masters' students. A career planner powered by AI 🚀")
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
st.markdown(
    """
    <div style="font-size:0.9em; color:gray; text-align:center; margin-top:2em;">
    CurveMyPath is an AI-powered course and career planner which provides personalized subject recommendations and career planning for students in major computer science and engineering programs at OVGU.<br>
    Recommendations are based on the official module catalog (covering Computer Science, Digital Engineering, Data and Knowledge Engineering, Visual Computing, and related degrees) and feedback from a student survey (primarily Digital Engineering and Data & Knowledge Engineering).<br>
    All the subjects that are recommended are taught in English. Subjects that are taught in German are not considered for this tool.<br>
    For transparency and reliability, the system only includes courses and programs represented in the catalog as of 2024.
    For the official OVGU module catalogue list, visit: <a href="https://www.inf.ovgu.de/en/Study/Being+a+student/Examination+Office/Study+Regulations/Module+Catalogue.html" target="_blank">Module Catalogue</a>.<br>
    For detailed course descriptions, see: <a href="https://www.fin.ovgu.de/Studium/W%C3%A4hrend+des+Studiums/Pr%C3%BCfungsamt/Studiendokumente.html" target="_blank">Study Documents</a>.<br>
    </div>
    """,
    unsafe_allow_html=True
)
#Feedback section

st.markdown("---")
if "show_feedback_box" not in st.session_state:
    st.session_state["show_feedback_box"] = False
if "reset_feedback" not in st.session_state:
    st.session_state["reset_feedback"] = False

if st.button("💬 Give feedback"):
    st.session_state["show_feedback_box"] = True

if st.session_state["show_feedback_box"]:
    # Handle reset before rendering the widget
    if st.session_state["reset_feedback"]:
        st.session_state["reset_feedback"] = False
        st.session_state["show_feedback_box"] = False
        st.rerun()

    feedback = st.text_area("Your feedback", key="feedback_text")
    if st.button("Send Feedback", key="send_feedback"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback
        }
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r") as f:
                feedback_list = json.load(f)
        else:
            feedback_list = []
        feedback_list.append(entry)
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedback_list, f, indent=2)
        st.success("Thank you for your feedback!")
        st.session_state["reset_feedback"] = True  # Triggers clearing and rerun