import streamlit as st
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@st.cache_data
def load_scored_courses():
    with open(os.path.join(DATA_DIR, "scored_courses_by_goal.json"), "r") as f:
        return json.load(f)

@st.cache_data
def load_cleaned_roadmap():
    with open(os.path.join(DATA_DIR, "roadmap_cleaned_keywords.json"), "r") as f:
        return json.load(f)

def display_ai_roadmap(goal):
    st.markdown(f"### 🚀 Generating Roadmap for: `{goal}`")

    all_matches = load_scored_courses()
    roadmap = load_cleaned_roadmap()

    goal_courses = all_matches.get(goal, [])
    top_courses = sorted(goal_courses, key=lambda x: -x["max_score"])[:8]
    more_courses = sorted(goal_courses, key=lambda x: -x["max_score"])[8:13]

    if not top_courses:
        st.warning("No matching English courses found for this goal.")
        return

    # OVGU COURSES
    st.markdown("#### 📚 Top 8 OVGU Courses")
    for i, course in enumerate(top_courses, start=1):
        keywords = ", ".join(course.get("matched_keywords", []))
        st.markdown(f"**{i}. {course['course_title']}**  \n"
                    f"*Match Score:* `{course['max_score']}%`  \n"
                    f"*Matched Keywords:* `{keywords}`")
        st.markdown("---")

    # EXPLORE MORE
    if more_courses:
        with st.expander("🔍 Click to view 5 additional relevant subjects (optional)"):
            st.markdown("#### 🧭 Additional Relevant Courses")
            for i, course in enumerate(more_courses, start=9):
                keywords = ", ".join(course.get("matched_keywords", []))
                st.markdown(f"**{i}. {course['course_title']}**  \n"
                            f"*Match Score:* `{course['max_score']}%`  \n"
                            f"*Matched Keywords:* `{keywords}`  ")
                st.markdown("---")


    # SKILLS + TOOLS
    goal_data = roadmap.get(goal)
    if goal_data:
        if goal_data.get("external_skills"):
            st.markdown("#### 🧠 External Skills / Certifications")
            for sk in goal_data["external_skills"]:
                st.checkbox(sk, key=f"{goal}_skill_{sk}")

        if goal_data.get("tools"):
            st.markdown("#### 🛠️ Tools / Platforms")
            for tool in goal_data["tools"]:
                st.checkbox(tool, key=f"{goal}_tool_{tool}")
    else:
        st.warning("No additional skills/tools found for this goal.")
