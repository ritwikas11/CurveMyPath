import json
import os

def generate_roadmap(goal):
    json_path = "data/roadmap_ai_output.json"
    if not os.path.exists(json_path):
        return "Roadmap file not found."

    with open(json_path, "r") as f:
        roadmaps = json.load(f)

    return roadmaps.get(goal, "No roadmap available for this goal.")
