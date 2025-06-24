import json
import os
import sys
from time import sleep
from tinydb import TinyDB

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from components.llm_engine import generate_response_together

# Load goals from goals.json
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/goals.json", "r") as f:
    course_data = json.load(f)

goals = list(course_data.keys())

# Prompt generators
def prompt_keywords(goal):
    return (
        f"You are an academic curriculum designer preparing students for a career as a {goal} in the German university context for the 2025 job market.\n"
        f"List exactly 5 highly relevant academic course topics (e.g., majors or university-taught domains) that specifically and practically contribute to becoming a {goal}.\n"
        f"Avoid generic fields like 'Computer Science' or 'Mathematics' unless they are core to the goal.\n"
        f"Do not include tools, certifications, or vague domains. Do not use synonyms or overlapping concepts.\n"
        f"Output only 5 concise bullet points — no explanation, headers, or additional comments."
    )

def prompt_skills(goal):
    return (
        f"You are a career path advisor guiding students toward a successful transition into the role of a {goal}.\n"
        f"List 5 essential non-academic skills or industry certifications that significantly improve employability in this role.\n"
        f"Include a mix of soft skills (e.g., stakeholder communication, leadership) and recognized certifications (e.g., AWS, PMP).\n"
        f"Exclude university subjects, programming languages, or general advice.\n"
        f"Return a clean bullet-point list only. No headings or elaboration."
    )

def prompt_tools(goal):
    return (
        f"As a digital career mentor, list 5 specific tools, platforms, or frameworks that a {goal} would typically use in their daily workflow.\n"
        f"Only include well-established or widely adopted industry tools. Do not include generic categories like 'databases' or 'IDEs'.\n"
        f"Focus on tools that would appear in job descriptions for this role.\n"
        f"Return exactly 5 bullet points — no headers, descriptions, or explanations."
    )

# TinyDB setup
db = TinyDB("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json")
db.truncate()

# Generate for each goal
for goal in goals:
    print(f"\n🎯 Generating for goal: {goal}")
    try:
        keywords = generate_response_together(prompt_keywords(goal))
        sleep(1)
        skills = generate_response_together(prompt_skills(goal))
        sleep(1)
        tools = generate_response_together(prompt_tools(goal))

        db.insert({
            "goal": goal,
            "course_keywords": [kw.strip("-• \t") for kw in keywords.split("\n") if kw.strip()],
            "external_skills": [sk.strip("-• \t") for sk in skills.split("\n") if sk.strip()],
            "tools": [tl.strip("-• \t") for tl in tools.split("\n") if tl.strip()]
        })

        print(f"✅ Saved all 3 outputs for: {goal}")

    except Exception as e:
        print(f"❌ Error for goal '{goal}': {e}")

print("\n✅ All roadmap outputs saved to TinyDB.")
