import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models list
MODELS = {
    "GPT-3.5": "openai/gpt-3.5-turbo",
    "Claude-3 Haiku": "anthropic/claude-3-haiku",
    "Gemini 2.5": "google/gemini-2.5-pro-preview",
    "Command-R": "cohere/command-r-plus",
    "LLaMA-3": "meta-llama/llama-3-70b-instruct"
}

# Function to get response from each model
def get_response(model_id, prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://your-app-name.com",  # optional
        "X-Title": "UV Assignment App"
    }

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800  # 👈 limit tokens to avoid credit issue
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Error: {response.status_code} - {response.json().get('error', {}).get('message', 'Unknown error')}"

# --- Streamlit UI ---
st.title("🧠 AI Model Comparison App")

prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Get Responses") and prompt.strip():
    for name, model in MODELS.items():
        with st.spinner(f"Getting response from {name}..."):
            answer = get_response(model, prompt)
            st.subheader(f"{name} says:")
            st.write(answer)















