import openai
import streamlit as st

# Create OpenAI-compatible client for Together
client = openai.OpenAI(
    api_key=st.secrets["TOGETHER_API_KEY"],
    base_url="https://api.together.xyz/v1"
)

def generate_response_together(prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"⚠️ Together.AI API error: {e}")
        return ""
