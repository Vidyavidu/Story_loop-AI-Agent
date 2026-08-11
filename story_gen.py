import os
import json
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel

# Load the API key from .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Scene(BaseModel):
    scene_number: int
    narration: str
    image_prompt: str

class Story(BaseModel):
    title: str
    moral: str
    mood: str
    scenes: list[Scene]

def generate_story(topic: str) -> Story:
    prompt = f"""
    Write a short children's story about: {topic}

    Return ONLY valid JSON, no markdown formatting, no backticks, in this exact shape:
    {{
      "title": "string",
      "moral": "string",
      "mood": "one word, e.g. happy, calm, adventurous, mysterious",
      "scenes": [
        {{
          "scene_number": 1,
          "narration": "1-2 sentences of story narration for this scene",
          "image_prompt": "a detailed visual description for an image generator"
        }}
      ]
    }}

    Generate exactly 5 scenes.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    raw_text = response.text.strip()

    # Gemini sometimes wraps JSON in ```json ... ``` even when told not to — strip it if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    data = json.loads(raw_text)
    story = Story(**data)  # validates the shape
    return story

if __name__ == "__main__":
    story = generate_story("a fox who learns patience")
    print(story.model_dump_json(indent=2))