import json
from components.llm_engine import generate_roadmap  # If you still have this method working

# Load course goals
with open("data/courses.json", "r") as f:
    course_data = json.load(f)

goals = list(course_data.keys())

roadmaps = {}

for goal in goals:
    print(f"Generating roadmap for: {goal}")
    result = generate_roadmap(goal)
    print(result)
    roadmaps[goal] = result

# Save to raw output (if needed again)
with open("data/roadmap_ai_output.json", "w") as f:
    json.dump(roadmaps, f, indent=2)

print("✅ Raw roadmap data saved to roadmap_ai_output.json")
