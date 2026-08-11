import os
import traceback
from datetime import datetime

from topic_gen import generate_topic
from pipeline import create_full_video
from publish_ig import publish_video_to_instagram
from dashboard_gen import record_run

LOG_FILE = "daily_run_log.txt"

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_daily():
    log("=== Daily run started ===")
    try:
        topic = generate_topic()
        log(f"Topic: {topic}")

        story, video_path = create_full_video(topic)
        log(f"Video created: {video_path}")
        log(f"Title: {story.title} | Moral: {story.moral}")

        caption = f"{story.title}\n\n{story.moral} 🦊\n\n#shortstory #storyloop #kidsstories"
        media_id = publish_video_to_instagram(video_path, caption)
        log(f"Published successfully. Media ID: {media_id}")

        record_run("done", story=story, video_path=video_path, media_id=media_id)

    except Exception as e:
        log(f"FAILED: {str(e)}")
        log(traceback.format_exc())
        record_run("fail", error=str(e))

    log("=== Daily run finished ===\n")

if __name__ == "__main__":
    run_daily()