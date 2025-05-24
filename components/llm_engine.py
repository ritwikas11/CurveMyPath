from tinydb import TinyDB, Query

def generate_roadmap(goal):
    db_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json"
    db = TinyDB(db_path)
    Goal = Query()
    
    result = db.search(Goal.goal == goal)
    
    if result and "outputs" in result[0]:
        return "\n".join(result[0]["outputs"])
    else:
        return "No roadmap available for this goal."
