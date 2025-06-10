import json
import requests

def ask_ollama(prompt, model="llama3.2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120
    )
    return response.json()["response"].strip()

# Load scored courses
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/scored_courses_by_goal.json") as f:
    scored_data = json.load(f)

with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/pdf_ovgucourses.json") as f:
    catalog = json.load(f)

# Create quick lookup for course details
catalog_by_title = {c["module_title"].strip(): c for c in catalog}

all_goal_explanations = {}

for goal, courses in scored_data.items():
    print(f"\nGenerating explanations for: {goal}")
    top_courses = sorted(courses, key=lambda x: -x["max_score"])[:15]
    explained_courses = []
    for course in top_courses:
        course_title = course["course_title"]
        cat_entry = catalog_by_title.get(course_title)
        learning_outcomes = cat_entry.get("learning_outcomes", "") if cat_entry else ""
        contents = cat_entry.get("contents", "") if cat_entry else ""

        prompt = (
            f"You are an expert career advisor. "
            f"Explain in 2-3 sentences why the course '{course_title}' is recommended for someone aspiring to be a {goal}. "
            f"Base your answer on the following:\n\n"
            f"Learning outcomes: {learning_outcomes}\n"
            f"Course contents: {contents}\n"
        )
        explanation = ask_ollama(prompt)
        print(f"\n{course_title}:\n{explanation}\n")
        explained_course = course.copy()
        explained_course["explanation"] = explanation
        explained_courses.append(explained_course)
    all_goal_explanations[goal] = explained_courses

# Save all explanations
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/explained_courses_by_goal.json", "w") as f:
    json.dump(all_goal_explanations, f, indent=2)

print("✅ All explanations generated and saved to data/explained_courses_by_goal.json")
