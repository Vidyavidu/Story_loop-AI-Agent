import json
import os
import re
from datetime import datetime

HISTORY_FILE = "run_history.json"
DASHBOARD_FILE = "dashboard.html"
TOTAL_DAYS = 10

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history: list):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def record_run(status: str, story=None, video_path=None, media_id=None, error=None):
    """Call this once per daily run to log the result."""
    history = load_history()
    entry = {
        "day": len(history) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%I:%M %p"),
        "status": status,  # "done" or "fail"
        "title": story.title if story else None,
        "moral": story.moral if story else None,
        "mood": story.mood if story else None,
        "scenes": len(story.scenes) if story else None,
        "video_path": video_path,
        "media_id": media_id,
        "error": error,
    }
    history.append(entry)
    save_history(history)
    generate_dashboard(history)
    return entry

def generate_dashboard(history: list):
    """Rewrites dashboard.html with the current run history baked in."""
    if not os.path.exists(DASHBOARD_FILE):
        print("dashboard.html template not found — skipping dashboard update.")
        return

    with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Build the chapter strip data (pad with "future" up to TOTAL_DAYS)
    chapters = [{"day": h["day"], "status": h["status"]} for h in history]
    while len(chapters) < TOTAL_DAYS:
        chapters.append({"day": len(chapters) + 1, "status": "future"})

    latest = history[-1] if history else None
    total_done = sum(1 for h in history if h["status"] == "done")
    total_runs = len(history)
    success_rate = f"{round((total_done / total_runs) * 100)}%" if total_runs else "—"

    # Replace the sample JS array with real data
    new_js = f"const runHistory = {json.dumps(chapters)};"
    html = re.sub(
        r"const runHistory = \[.*?\];",
        new_js,
        html,
        flags=re.DOTALL,
    )

    # Replace header status + date
    today_str = datetime.now().strftime("%A, %-d %B %Y") if os.name != "nt" else datetime.now().strftime("%A, %#d %B %Y")
    html = html.replace(
        '<div class="date-line" id="todayDate">Saturday, 9 August 2026</div>',
        f'<div class="date-line" id="todayDate">{today_str}</div>',
    )

    if latest and latest["status"] == "done":
        # Swap the placeholder div for an actual video element
        video_web_path = latest["video_path"].replace("\\", "/") if latest["video_path"] else ""
        video_html = (
            f'<video controls id="videoArea" src="{video_web_path}"></video>'
        )
        html = re.sub(
            r'<div class="video-fallback" id="videoArea">.*?</div>',
            video_html,
            html,
        )

        html = html.replace(
            '<div class="mood-tag" id="moodTag">calm</div>',)
    elif latest and latest["status"] == "fail":
        badge = '<div class="status-badge fail" id="todayStatus"><span class="pulse"></span>Failed today</div>'
    else:
        badge = '<div class="status-badge pending" id="todayStatus"><span class="pulse"></span>Not run yet</div>'

    html = re.sub(
        r'<div class="status-badge.*?</div>',
        badge,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Replace latest story spotlight
    if latest and latest["status"] == "done":
        html = html.replace(
            '<div class="mood-tag" id="moodTag">calm</div>',
            f'<div class="mood-tag" id="moodTag">{latest["mood"]}</div>',
        )
        html = html.replace(
            '<div class="story-title" id="storyTitle">The Fox Who Learned to Wait</div>',
            f'<div class="story-title" id="storyTitle">{latest["title"]}</div>',
        )
        html = re.sub(
            r'<div class="moral" id="storyMoral">.*?</div>',
            f'<div class="moral" id="storyMoral">"{latest["moral"]}"</div>',
            html,
        )
        html = html.replace(
            '<strong id="sceneCount">5</strong>',
            f'<strong id="sceneCount">{latest["scenes"]}</strong>',
        )
        html = html.replace(
            '<strong id="publishTime">9:04 AM</strong>',
            f'<strong id="publishTime">{latest["time"]}</strong>',
        )
        if latest.get("media_id"):
            html = html.replace(
                'href="#" target="_blank">View on Instagram',
                f'href="https://www.instagram.com/reel/{latest["media_id"]}" target="_blank">View on Instagram',
            )

    # Replace stats
    html = html.replace('<div class="value" id="statTotal">6</div>', f'<div class="value" id="statTotal">{total_done}</div>')
    html = html.replace('<div class="value" id="statRate">100%</div>', f'<div class="value" id="statRate">{success_rate}</div>')

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard updated: {DASHBOARD_FILE}")