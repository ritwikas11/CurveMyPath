import streamlit as st
import requests
import json
import os
import datetime

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

            # ---- Audit begins here ----
            AUDIT_FILE = os.path.join("data", "llm_audits.json")
            os.makedirs("data", exist_ok=True)  # Ensure the folder exists
            audit_response = audit_llm_output(user_question, llm_answer, course_context)
            st.write(f"Saving audit to: {AUDIT_FILE}")  # Debug print
            # Save audit result to file (append mode)
            audit_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "question": user_question,
                "llm_answer": llm_answer,
                "audit_response": audit_response
            }
            # Load current audits (if any), append, and save
            try:
                with open(AUDIT_FILE, "r") as f:
                    audits = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                audits = []
            audits.append(audit_entry)
            with open(AUDIT_FILE, "w") as f:
                json.dump(audits, f, indent=2)
            st.write("Audit saved successfully.")  # Debug print
            # ---- Audit ends ----
            st.rerun()
        except requests.exceptions.ConnectionError:
            st.sidebar.error(
                "AI Career Assistant is only available in the local (offline) version of this app. "
            )
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    # Show answer and the Reset button if there's an answer
    if st.session_state["ai_chatbox_answer"]:
        st.sidebar.success(st.session_state["ai_chatbox_answer"])
        if st.sidebar.button("Reset", key="ai_chatbox_reset"):
            st.session_state["reset_chatbox"] = True
            st.rerun()

def audit_llm_output(question, answer, context, model="llama3.2"):
    audit_prompt = (
        f"Context (courses/skills/tools):\n{context}\n"
        f"Student's question:\n{question}\n"
        f"AI's answer:\n{answer}\n"
        "Is the answer factually accurate and relevant, based only on the provided context? "
        "Reply YES or NO. If NO, briefly explain why."
    )
    return ask_ollama(audit_prompt, model=model)
