import subprocess

# Target vertical format for Instagram Reels/Stories (9:16)
WIDTH = 1080
HEIGHT = 1920

def _ffmpeg_safe_path(path: str) -> str:
    """
    FFmpeg's subtitles filter needs forward slashes and an escaped colon,
    even on Windows. This converts a normal Windows path into that format.
    e.g. C:\\Users\\me\\scene_1.srt -> C\\:/Users/me/scene_1.srt
    """
    path = path.replace("\\", "/")
    path = path.replace(":", "\\:")
    return path

def create_scene_clip(image_path: str, audio_path: str, srt_path: str, output_path: str):
    """
    Combines one scene's image + narration audio + captions into a single video clip.
    The clip's length matches the audio length exactly.
    """
    safe_srt = _ffmpeg_safe_path(srt_path)

    # Scale the image to fit the vertical frame, pad any empty space with black,
    # then burn the subtitles on top.
    vf_filter = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"subtitles='{safe_srt}':force_style='Fontsize=14,PrimaryColour=&HFFFFFF,"
        f"OutlineColour=&H000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=80'"
    )

    command = [
        "ffmpeg",
        "-y",  # overwrite output if it already exists
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",  # stop when the audio ends
        output_path,
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:")
        print(result.stderr[-2000:])  # last part of the error, usually the useful bit
        raise RuntimeError(f"Failed to create clip for {image_path}")

    print(f"Saved: {output_path}")

# Quick test — uses the test files you already generated
if __name__ == "__main__":
    create_scene_clip(
        "test_scene.png",
        "test_narration.mp3",
        "test_narration.srt",
        "test_clip.mp4"
    )

import os

def stitch_clips(clip_paths: list, output_path: str):
    """
    Joins multiple video clips into one final video, in the order given.
    """
    # FFmpeg's concat demuxer needs a text file listing the clips in order
    list_file = "clip_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for path in clip_paths:
            # Paths need forward slashes and to be wrapped in quotes here too
            safe_path = path.replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",  # just join the files, no re-encoding needed (fast)
        output_path,
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    os.remove(list_file)  # clean up the temporary list file

    if result.returncode != 0:
        print("FFmpeg error:")
        print(result.stderr[-2000:])
        raise RuntimeError("Failed to stitch clips")

    print(f"Final video saved: {output_path}")