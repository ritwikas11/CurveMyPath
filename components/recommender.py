import streamlit as st
import json

def select_goal():
    # Load data
    try:
        with open("data/courses.json", "r") as f:
            course_data = json.load(f)
    except FileNotFoundError:
        st.error("Course data not found.")
        return

    goal_options = list(course_data.keys())

    # Reset logic
    if st.session_state.get("reset_requested"):
        st.session_state["show_recommendation"] = False
        st.session_state["show_progress"] = False
        st.session_state["current_goal"] = None
        st.session_state["reset_requested"] = False

    # 🟢 Case: User has already saved path → Dashboard mode
    if st.session_state.get("show_progress"):
        current_goal = st.session_state["current_goal"]
        st.markdown(f"### ✅ You selected: **{current_goal}**")
        # Styled Reset button (Streamlit native)
        if st.button("Select a different goal"):
            st.session_state["reset_requested"] = True
            st.rerun()
        st.markdown("#### 🎯 Based on your goal, we recommend:")
        for course in course_data.get(current_goal, []):
            st.markdown(f"- {course}")
        return

    # 🟡 Case: Still in selection mode
    st.markdown("### 🎯 Choose your career goal:")

    cols = st.columns([3, 1])
    with cols[0]:
        selected_goal = st.selectbox("Select your career goal", goal_options, label_visibility="collapsed")

    with cols[1]:
        if st.button("🚀 Recommend Courses", use_container_width=True):
            if "goals_selected" not in st.session_state:
                st.session_state["goals_selected"] = []
            st.session_state["current_goal"] = selected_goal
            st.session_state["show_recommendation"] = True
            if selected_goal not in st.session_state["goals_selected"]:
                st.session_state["goals_selected"].append(selected_goal)
            st.rerun()

    # Clear output if dropdown changes
    if "current_goal" in st.session_state and selected_goal != st.session_state["current_goal"]:
        st.session_state["show_recommendation"] = False
        st.session_state["show_progress"] = False

    # Show recommendations if triggered
    if st.session_state.get("show_recommendation"):
        goal = st.session_state["current_goal"]
        st.markdown(f"#### Recommended for **{goal}**:")
        for course in course_data.get(goal, []):
            st.markdown(f"- {course}")
        st.info("Why? These courses align with your goal’s core skills.")

        # Save path button
        st.write("Like what you see? Click 'Save My Path' to build your personalized roadmap and track your progress ▼")
        if st.button("💾 Save My Path"):
            st.session_state["show_progress"] = True
            st.rerun()
