import streamlit as st
from components.llm_engine import generate_roadmap

def display_ai_roadmap(goal):

    # Handle Generate Roadmap button
    if f"roadmap_output_{goal}" not in st.session_state:
        if st.button("🔍 Generate Roadmap"):
            with st.spinner("Generating roadmap using TinyLlama..."):
                output = generate_roadmap(goal)
                st.session_state[f"roadmap_output_{goal}"] = output
                st.rerun()  # 🔁 Immediately rerun to show output after saving

    # Show roadmap if available
    if f"roadmap_output_{goal}" in st.session_state:
        output = st.session_state[f"roadmap_output_{goal}"]
        st.markdown("#### Recommended Skills & Certifications:")

        for line in output.split("\n"):
            line = line.strip("-• ")
            if line:
                st.checkbox(line, key=f"skill_{hash(line)}")
