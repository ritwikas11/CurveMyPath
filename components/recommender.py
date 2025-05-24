import streamlit as st
import json

def select_goal():
    # Load course options
    try:
        with open("data/courses.json", "r") as f:
            course_data = json.load(f)
    except FileNotFoundError:
        st.error("Course data not found.")
        return

    goal_options = list(course_data.keys())

    # Initialize state if not set
    if "current_goal" not in st.session_state:
        st.session_state.current_goal = None
    if "goal_selected" not in st.session_state:
        st.session_state.goal_selected = None
    if "show_roadmap" not in st.session_state:
        st.session_state.show_roadmap = False

    # UI layout
    st.markdown("### 🎯 Choose your career goal:")
    cols = st.columns([3, 1])

    # Dropdown
    with cols[0]:
        selected = st.selectbox(
            "Select your career goal",
            goal_options,
            key="goal_dropdown",
            index=goal_options.index(st.session_state.goal_selected) if st.session_state.goal_selected in goal_options else 0
        )

    # Reset if selection changed
    if selected != st.session_state.goal_selected:
        st.session_state.goal_selected = selected
        st.session_state.show_roadmap = False

    # Button
    with cols[1]:
        if st.button("🚀 Generate Roadmap", use_container_width=True):
            st.session_state.current_goal = selected
            st.session_state.show_roadmap = True
            st.rerun()

    # Display reminder
    if not st.session_state.show_roadmap:
        st.info("Click 'Generate Roadmap' to view your personalized recommendations.")
