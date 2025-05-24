from tinydb import TinyDB
import re
import json
import os

# === Load TinyDB data ===
db_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json"
db = TinyDB(db_path)

# === Output dictionary ===
cleaned_data = {}

# === Cleaning function ===
def clean_list(raw_list):
    cleaned = set()
    for item in raw_list:
        # Split multiline text into lines
        lines = item.split("\n")
        for line in lines:
            # Strip bullets, numbers, and extra characters
            line = line.strip("-•*0123456789. \t")
            line = re.sub(r"\(.*?\)", "", line)  # Remove content in brackets
            line = re.sub(r"\*\*", "", line)     # Remove markdown bold
            line = line.strip()
            # Keep only short phrases
            if 1 <= len(line.split()) <= 6:
                cleaned.add(line.title())
    return sorted(cleaned)[:7]  # Limit to top 7 per category

# === Process each goal ===
for entry in db.all():
    goal = entry.get("goal")
    keywords = clean_list(entry.get("course_keywords", []))
    skills = clean_list(entry.get("external_skills", []))
    tools = clean_list(entry.get("tools", []))

    cleaned_data[goal] = {
        "course_keywords": keywords,
        "external_skills": skills,
        "tools": tools
    }

# === Save cleaned data ===
output_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_cleaned_keywords.json"
os.makedirs("data", exist_ok=True)

with open(output_path, "w") as f:
    json.dump(cleaned_data, f, indent=2)

print(f"✅ Cleaned data saved to: {output_path}")
