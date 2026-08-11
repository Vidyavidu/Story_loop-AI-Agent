import asyncio
from datetime import timedelta
import edge_tts

VOICE = "en-US-AriaNeural"
WORDS_PER_CAPTION = 4  # how many words show on screen at once

def _format_srt_time(microseconds: int) -> str:
    td = timedelta(microseconds=microseconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"

def _build_srt(word_boundaries: list) -> str:
    """Groups individual words into short multi-word caption cues."""
    lines = []
    cue_index = 1

    for i in range(0, len(word_boundaries), WORDS_PER_CAPTION):
        group = word_boundaries[i:i + WORDS_PER_CAPTION]
        start_ticks = group[0]["offset"]
        end_ticks = group[-1]["offset"] + group[-1]["duration"]
        text = " ".join(w["text"] for w in group)

        start_srt = _format_srt_time(start_ticks / 10)
        end_srt = _format_srt_time(end_ticks / 10)

        lines.append(str(cue_index))
        lines.append(f"{start_srt} --> {end_srt}")
        lines.append(text)
        lines.append("")
        cue_index += 1

    return "\n".join(lines)

async def _generate(text: str, audio_path: str, srt_path: str):
    # boundary="WordBoundary" gives us per-word timing instead of per-sentence
    communicate = edge_tts.Communicate(text, VOICE, boundary="WordBoundary")
    word_boundaries = []

    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append(chunk)

    srt_content = _build_srt(word_boundaries)
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)

def generate_narration(text: str, audio_path: str, srt_path: str):
    """
    Generates narration audio AND a matching subtitle file with short,
    readable multi-word caption chunks (not one giant sentence).
    """
    asyncio.run(_generate(text, audio_path, srt_path))
    print(f"Saved: {audio_path} and {srt_path}")

# Quick test
if __name__ == "__main__":
    generate_narration(
        "Once upon a time, in a quiet forest, there lived a small orange fox who found it very hard to wait for anything.",
        "test_narration.mp3",
        "test_narration.srt"
    )