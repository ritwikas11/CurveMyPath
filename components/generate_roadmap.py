import json
from components.llm_engine import generate_roadmap

goals = [
    "Product Owner",
    "Data Scientist",
    "AI Engineer",
    "UX Designer"
]

roadmaps = {}
for goal in goals:
    print(f"Generating roadmap for: {goal}")
    result = generate_roadmap(goal)
    print(result)
    roadmaps[goal] = result

with open("data/roadmap_ai_output.json", "w") as f:
    json.dump(roadmaps, f, indent=2)
