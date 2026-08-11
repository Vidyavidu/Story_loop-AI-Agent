import os
from story_gen import generate_story
from image_gen import generate_image
from voice_gen import generate_narration
from video_gen import create_scene_clip, stitch_clips
from music_gen import pick_music_track, add_background_music

def create_full_video(topic: str, output_folder: str = "output"):
    """
    Full pipeline: story -> per-scene image/audio/captions -> per-scene clips -> final video.
    """
    os.makedirs(output_folder, exist_ok=True)

    print(f"Generating story for topic: {topic}")
    story = generate_story(topic)
    print(f"Title: {story.title}")
    print(f"Mood: {story.mood}")

    clip_paths = []

    for scene in story.scenes:
        n = scene.scene_number
        print(f"\n--- Scene {n} ---")

        image_path = os.path.join(output_folder, f"scene_{n}.png")
        audio_path = os.path.join(output_folder, f"scene_{n}.mp3")
        srt_path = os.path.join(output_folder, f"scene_{n}.srt")
        clip_path = os.path.join(output_folder, f"scene_{n}_clip.mp4")

        print("Generating image...")
        generate_image(scene.image_prompt, image_path)

        print("Generating narration + captions...")
        generate_narration(scene.narration, audio_path, srt_path)

        print("Assembling scene clip...")
        create_scene_clip(image_path, audio_path, srt_path, clip_path)

        clip_paths.append(clip_path)

    stitched_path = os.path.join(output_folder, "final_video_no_music.mp4")
    print("\nStitching all scenes together...")
    stitch_clips(clip_paths, stitched_path)

    print("Adding background music...")
    music_path = pick_music_track(story.mood)
    final_path = os.path.join(output_folder, "final_video.mp4")
    add_background_music(stitched_path, music_path, final_path)

    return story, final_path

    return story, final_path

if __name__ == "__main__":
    story, final_path = create_full_video("a fox who learns patience")
    print("\n--- DONE ---")
    print(f"Title: {story.title}")
    print(f"Moral: {story.moral}")
    print(f"Final video: {final_path}")