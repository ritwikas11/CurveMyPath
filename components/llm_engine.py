import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

@st.cache_resource
def load_llm():
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to("cpu")  # Force CPU
    return pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # device=-1 = CPU

def generate_roadmap(goal):
    prompt = f"""
As a career advisor, list top 5 skills, certifications, and tools someone should learn to become a successful {goal} in tech. Write them as bullet points:
- 
"""
    llm = load_llm()
    output = llm(
        prompt,
        max_length=150,
        temperature=0.6,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        repetition_penalty=1.2
    )[0]["generated_text"]

    roadmap = output.replace(prompt.strip(), "").strip()
    return roadmap
