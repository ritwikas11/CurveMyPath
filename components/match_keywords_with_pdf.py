import json
from rapidfuzz import fuzz

# Load cleaned roadmap with refined keywords
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_cleaned_keywords.json", "r") as f:
    goal_keywords = json.load(f)

# Load parsed OVGU course catalog
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/pdf_ovgucourses.json", "r") as f:
    course_catalog = json.load(f)

# Filter: English-only subjects
english_courses = [
    c for c in course_catalog
    if c.get("language", "").lower().startswith("english")
]

results_by_goal = {}

for goal, data in goal_keywords.items():
    keywords = [kw.lower().strip() for kw in data.get("course_keywords", [])]
    goal_matches = []

    for course in english_courses:
        course_title = course["module_title"].strip()
        english_title = course.get("english_title", "").strip()
        learning_outcomes = course.get("learning_outcomes", "").lower()
        contents = course.get("contents", "").lower()
        language = course.get("language", "").split()[0]  # Extract "English"

        matched_keywords = []
        matched_fields = []
        match_scores = []

        for keyword in keywords:
            for field_name, field_text in {
                "learning_outcomes": learning_outcomes,
                "contents": contents,
            }.items():
                if not field_text:
                    continue
                score = fuzz.token_set_ratio(keyword, field_text)
                if score >= 50:  # optional threshold to avoid noise
                    matched_keywords.append(keyword)
                    matched_fields.append(field_name)
                    match_scores.append(round(score, 1))

        if matched_keywords:
            goal_matches.append({
                "goal": goal,
                "course_title": course_title,
                "english_title": english_title,
                "matched_keywords": matched_keywords,
                "matched_fields": matched_fields,
                "match_scores": match_scores,
                "max_score": max(match_scores),
                "language": language,
                "description_snippet": course.get("learning_outcomes", "")[:160] + "..."
            })

    if goal_matches:
        results_by_goal[goal] = sorted(goal_matches, key=lambda x: -x["max_score"])[:20]

# Save outputs
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/scored_courses_by_goal.json", "w") as f:
    json.dump(results_by_goal, f, indent=2)

print("✅ Matching and scoring complete.")
print("→ Saved to: data/scored_courses_by_goal.json")
