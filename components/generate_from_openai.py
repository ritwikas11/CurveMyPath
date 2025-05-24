import json
import os
import sys
from time import sleep
from tinydb import TinyDB

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from components.llm_engine import generate_response_together

# Load goals from courses.json
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/courses.json", "r") as f:
    course_data = json.load(f)

goals = list(course_data.keys())

# Prompt generators
def prompt_keywords(goal):
    return f"You are a career mentor. List 5 academic keywords that match subjects a student should study at university to become a {goal}. Use bullet points. No extra explanation."

def prompt_skills(goal):
    return f"You are a career coach. What are 5 non-university skills or certifications a {goal} should learn? Include both soft skills and certifications. Use bullet points only."

def prompt_tools(goal):
    return f"As a career advisor, list 5 software tools or platforms a {goal} must become proficient with. Bullet points only. No extra explanation or titles."

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
