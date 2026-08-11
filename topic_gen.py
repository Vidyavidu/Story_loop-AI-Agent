import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

USED_TOPICS_FILE = "used_topics.json"

def _load_used_topics() -> list:
    if os.path.exists(USED_TOPICS_FILE):
        with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_used_topic(topic: str):
    used = _load_used_topics()
    used.append(topic)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)

def generate_topic() -> str:
    """
    Asks Gemini for a fresh children's story topic/theme,
    avoiding ones already used before.
    """
    used = _load_used_topics()
    recent = used[-15:]  # only show the last 15 so the prompt doesn't grow forever

    prompt = f"""
    Suggest ONE short children's story topic/theme (one sentence, e.g.
    "a turtle who is afraid of water" or "two friends who learn to share").

    It must teach a positive moral (patience, honesty, kindness, courage, sharing, etc).

    Do NOT repeat or closely resemble any of these already-used topics:
    {json.dumps(recent)}

    Reply with ONLY the topic sentence, nothing else — no quotes, no labels.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    topic = response.text.strip()
    _save_used_topic(topic)
    return topic

if __name__ == "__main__":
    topic = generate_topic()
    print(f"Generated topic: {topic}")