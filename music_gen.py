import subprocess

# Maps story moods to one of your two music buckets.
# Add more mood words here as you notice Gemini using them.
MOOD_MAP = {
    "happy": "upbeat.mp3",
    "adventurous": "upbeat.mp3",
    "exciting": "upbeat.mp3",
    "calm": "calm.mp3",
    "mysterious": "calm.mp3",
    "peaceful": "calm.mp3",
    "sad": "calm.mp3",
}

def pick_music_track(mood: str, music_folder: str = "music") -> str:
    filename = MOOD_MAP.get(mood.lower(), "calm.mp3")  # default fallback
    return f"{music_folder}/{filename}"

def add_background_music(video_path: str, music_path: str, output_path: str, music_volume: float = 0.15):
    """
    Mixes background music under the video's existing narration audio.
    music_volume is relative loudness (0.15 = 20% volume, quiet enough not to compete with narration).
    Music is looped and trimmed to match the video's length automatically.
    """
    filter_complex = (
        f"[1:a]volume={music_volume}[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-stream_loop", "-1",  # loop the music indefinitely
        "-i", music_path,
        "-filter_complex", filter_complex,
        "-map", "0:v",       # keep original video
        "-map", "[aout]",    # use the mixed audio
        "-c:v", "copy",      # don't re-encode video, just audio
        "-shortest",         # stop at the video's length (not the looped music's)
        output_path,
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:")
        print(result.stderr[-2000:])
        raise RuntimeError("Failed to add background music")

    print(f"Saved with music: {output_path}")

# Quick test
if __name__ == "__main__":
    add_background_music(
        "output/final_video.mp4",
        "music/calm.mp3",
        "output/final_video_with_music.mp4"
    )