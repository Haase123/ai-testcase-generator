import json
import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None
AI_GENERATOR_MODE = "unknown"

def generate_ai_test_cases(title: str, description: str):
    global AI_GENERATOR_MODE

    if not client:
        AI_GENERATOR_MODE = "fallback"
        return None, "rule-based"
    
    prompt = f"""
You are a senior QA engineer.
Return ONLY valid JSON.

Requirement title: {title}
Requirement description: {description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert QA architect."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content
        AI_GENERATOR_MODE = "openai"
        return json.loads(content), "openai"

    except (RateLimitError, json.JSONDecodeError, Exception):
        AI_GENERATOR_MODE = "fallback"
        return None, "rule-based"

def get_ai_generator_status():
    return AI_GENERATOR_MODE