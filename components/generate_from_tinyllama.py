import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load TinyLlama model locally
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to("cpu")
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# Define your goals
goals = [
    "Data Scientist",
    "Product Management",
    "AI/ML Engineer",
]

# Prompt format
def generate_roadmap(goal):
    prompt = f"""
    Act as a senior career advisor. The student wants to become a {goal} in the tech industry.

    List a 12-month learning roadmap including:
        - Essential technical skills
        - Must-have certifications
        - Recommended tools
        - 1 project idea for each quarter
    
    Format as bullet points. No need for explanations or additional text. Just the roadmap, bullet points only.
    """
    output = llm(
        prompt,
        max_length=200,
        temperature=0.6,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        repetition_penalty=1.2
    )[0]["generated_text"]

    roadmap = output.replace(prompt.strip(), "").strip()
    return roadmap

# Generate all roadmaps
roadmaps = {}
for goal in goals:
    print(f"🔧 Generating for: {goal}")
    result = generate_roadmap(goal)
    print(result)
    roadmaps[goal] = result

# Ensure the directory exists
os.makedirs("data", exist_ok=True)

# Write the file
with open("/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/roadmap_ai_output.json", "w") as f:
    json.dump(roadmaps, f, indent=2)

print("✅ All roadmaps saved to data/roadmap_ai_output.json")
