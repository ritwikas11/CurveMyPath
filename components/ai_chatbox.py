import streamlit as st
import requests
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def ask_ollama(prompt, model="llama3.2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120
    )
    return response.json()["response"].strip()

def ai_chatbox():
    st.sidebar.markdown("## 💬 Ask the AI Career Assistant")

    # Initialize state on first load
    if "ai_chatbox_answer" not in st.session_state:
        st.session_state["ai_chatbox_answer"] = ""
    if "reset_chatbox" not in st.session_state:
        st.session_state["reset_chatbox"] = False

    # If just reset, skip rendering the input (let rerun handle it)
    if st.session_state["reset_chatbox"]:
        st.session_state["ai_chatbox_question"] = ""
        st.session_state["ai_chatbox_answer"] = ""
        st.session_state["reset_chatbox"] = False
        st.rerun()

    # Now render the input widget
    user_question = st.sidebar.text_input(
        "Type any question about your career or university courses",
        key="ai_chatbox_question"
    )
    send_clicked = st.sidebar.button("Send", key="ai_chatbox_send")

    if send_clicked and user_question:
        with open(os.path.join(DATA_DIR, "explained_courses_by_goal.json")) as f:
            explained_courses = json.load(f)
        with open(os.path.join(DATA_DIR, "roadmap_cleaned_keywords.json")) as f:
            roadmap = json.load(f)

        all_courses = []
        for goal_courses in explained_courses.values():
            all_courses.extend(sorted(goal_courses, key=lambda x: -x["max_score"])[:3])
        course_context = "\n".join([
            f"- {c['course_title']} ({c.get('max_score','')}%): {c.get('explanation','')}" for c in all_courses
        ])
        all_skills = set()
        all_tools = set()
        for g in roadmap.values():
            all_skills.update(g.get("external_skills", []))
            all_tools.update(g.get("tools", []))
        skills_context = ", ".join(sorted(all_skills))
        tools_context = ", ".join(sorted(all_tools))
        prompt = (
            f"You are an expert career advisor. "
            f"Using only the following university courses and their explanations, and these skills and tools, "
            f"answer the user's question as helpfully as possible.\n"
            f"User question: {user_question}\n"
            f"Courses:\n{course_context}\n"
            f"Skills: {skills_context}\n"
            f"Tools: {tools_context}\n"
            f"Only use these sources; do not invent new courses or information."
        )
        st.sidebar.info("Generating answer...")
        try:
            llm_answer = ask_ollama(prompt)
            st.session_state["ai_chatbox_answer"] = llm_answer
            # Optionally clear question (but don't touch after widget is made in this run)
            # st.session_state["ai_chatbox_question"] = ""  # Only on reset!
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    # Show answer and the Reset button if there's an answer
    if st.session_state["ai_chatbox_answer"]:
        st.sidebar.success(st.session_state["ai_chatbox_answer"])
        if st.sidebar.button("Reset", key="ai_chatbox_reset"):
            st.session_state["reset_chatbox"] = True
            st.rerun()