import json
from components.llm_engine import generate_roadmap

# Load career goals
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/courses.json", "r") as f:
    course_data = json.load(f)

goals = list(course_data.keys())

roadmaps = {}
for goal in goals:
    print(f"Generating roadmap for: {goal}")
    result = generate_roadmap(goal)
    print(result)
    roadmaps[goal] = result

with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json", "w") as f:
    json.dump(roadmaps, f, indent=2)
