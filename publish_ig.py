import os
import time
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
GRAPH_URL = "https://graph.instagram.com/v25.0"


def upload_video_to_cloudinary(video_path: str) -> str:
    """Uploads the video and returns a public URL Instagram can fetch from."""
    print("Uploading video to Cloudinary...")
    result = cloudinary.uploader.upload(
        video_path,
        resource_type="video",
    )
    url = result["secure_url"]
    print(f"Public video URL: {url}")
    return url


def create_reel_container(video_url: str, caption: str) -> str:
    """Step 1: create the media container."""
    response = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media",
        params={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": IG_ACCESS_TOKEN,
        },
    )
    data = response.json()
    if "id" not in data:
        raise RuntimeError(f"Failed to create container: {data}")
    print(f"Container created: {data['id']}")
    return data["id"]


def wait_for_container_ready(container_id: str, max_wait_seconds: int = 300):
    """Step 2: poll until Instagram finishes processing the video."""
    waited = 0
    interval = 10

    while waited < max_wait_seconds:
        response = requests.get(
            f"{GRAPH_URL}/{container_id}",
            params={"fields": "status_code", "access_token": IG_ACCESS_TOKEN},
        )
        status = response.json().get("status_code")
        print(f"Status: {status} (waited {waited}s)")

        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError("Instagram failed to process the video (check format/spec).")

        time.sleep(interval)
        waited += interval
        interval = min(interval * 2, 60)  # back off up to 60s between checks

    raise TimeoutError("Video processing took too long.")


def publish_container(container_id: str) -> str:
    """Step 3: publish the finished container."""
    response = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media_publish",
        params={"creation_id": container_id, "access_token": IG_ACCESS_TOKEN},
    )
    data = response.json()
    if "id" not in data:
        raise RuntimeError(f"Failed to publish: {data}")
    print(f"Published! Media ID: {data['id']}")
    return data["id"]


def publish_video_to_instagram(video_path: str, caption: str):
    video_url = upload_video_to_cloudinary(video_path)
    container_id = create_reel_container(video_url, caption)
    wait_for_container_ready(container_id)
    media_id = publish_container(container_id)
    return media_id


# Quick test — run this only when you're actually ready to post something live
if __name__ == "__main__":
    publish_video_to_instagram(
        "output/final_video.mp4",
        "A short story about patience 🦊 #shortstory #storyloop"
    )