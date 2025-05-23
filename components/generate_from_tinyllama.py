import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from tinydb import TinyDB

# Load TinyLlama model
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to("cpu")
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# Load career goals
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/courses.json", "r") as f:
    course_data = json.load(f)

goals = list(course_data.keys())

# Prompt generator (single-line formatted to avoid newline issues)
def generate_prompt(goal):
    return f"""
    You are a career advisor.

Here is a skill roadmap for someone who wants to become a Data Scientist:
- Python
- SQL
- Machine Learning
- Jupyter Notebook
- IBM Data Science Certificate

Now give a similar list of top 5 keywords (tools, skills, certs) for someone who wants to become a {goal}. 

IMPORTANT: Only return a clean list of keywords. No instructions. No summaries. No titles.
"""

# Create TinyDB
db_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json"
db = TinyDB(db_path)
db.truncate()

# Generate output for each goal
for goal in goals:
    print(f"🎯 Generating for goal: {goal}")
    
    prompt = generate_prompt(goal)
    
    try:
        response = llm(
            prompt,
            max_new_tokens=80,
            temperature=0.2,
            top_k=40,
            top_p=0.85,
            do_sample=True
        )
        output = response[0]["generated_text"].replace(prompt, "").strip()
        db.insert({"goal": goal, "outputs": [output]})
        print(f"✅ Output saved for {goal}")

    except Exception as e:
        print(f"❌ Error for goal '{goal}': {e}")

print("✅ All roadmap outputs saved to TinyDB.")
