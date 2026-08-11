import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

def generate_image(prompt: str, save_path: str):
    """
    Generates an image from a prompt and saves it locally at save_path.
    e.g. generate_image("a fox in a forest", "scene_1.png")
    """
    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell",
    )
    image.save(save_path)
    print(f"Saved: {save_path}")

# Quick test
if __name__ == "__main__":
    generate_image(
        "a small orange fox sitting patiently by a river at sunset, storybook illustration style",
        "test_scene.png"
    )