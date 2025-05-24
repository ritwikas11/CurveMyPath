import streamlit as st
import json
import os

# Load the cleaned roadmap data
@st.cache_data
def load_cleaned_roadmap():
    json_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_cleaned_keywords.json"
    if not os.path.exists(json_path):
        st.warning("Cleaned roadmap file not found.")
        return {}
    with open(json_path, "r") as f:
        return json.load(f)

def display_ai_roadmap(goal):
    #if not goal:
        #st.info("Please select and save a goal first.")
        #return

    roadmaps = load_cleaned_roadmap()
    goal_data = roadmaps.get(goal)

    if not goal_data:
        st.warning("No roadmap available for this goal.")
        return

    st.markdown("#### 🔍 Recommended Keywords, Skills & Tools")
    st.markdown(f"##### 🎓 Academic Subjects for {goal}:")
    for kw in goal_data.get("course_keywords", []):
        st.checkbox(kw, key=f"{goal}_kw_{kw}")

    st.markdown(f"##### 🧠 External Skills / Certifications:")
    if goal_data.get("external_skills"):
        for skill in goal_data.get("external_skills", []):
            st.checkbox(skill, key=f"{goal}_skill_{skill}")
    else:
        st.caption("No external skills listed.")

    st.markdown(f"##### 🛠️ Recommended Tools:")
    for tool in goal_data.get("tools", []):
        st.checkbox(tool, key=f"{goal}_tool_{tool}")
