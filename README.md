# Story_loop – AI Storytelling & Video Automation

An AI-powered storytelling pipeline that automatically creates short illustrated story videos for children, complete with narration, subtitles, background music, and optional Instagram Reels publishing.

## Project Overview

Story_loop transforms a simple story topic into a complete vertical video through multiple AI-powered steps. It is designed to simplify the process of creating short-form storytelling content.

## Key Features

- **AI Story Generation:** Generates children's stories with titles, morals, moods, and five individual scenes using Google Gemini.
- **Topic Generation:** Suggests fresh story ideas while tracking previously used topics.
- **AI Image Generation:** Creates scene illustrations using Hugging Face Inference API and FLUX.1-schnell.
- **Voice Narration:** Converts story text into speech using Edge TTS.
- **Automatic Captions:** Generates synchronized subtitle files using word-level timing.
- **Video Creation:** Combines illustrations, narration, and subtitles into vertical 9:16 videos using FFmpeg.
- **Background Music:** Selects music based on the story's mood and mixes it with narration.
- **Instagram Publishing:** Supports automated Reel publishing through the Instagram Graph API.
- **Run Dashboard:** Tracks execution history, generated stories, and publishing status.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Story generation | Google Gemini API |
| Image generation | Hugging Face Inference API, FLUX.1-schnell |
| Text-to-speech | Edge TTS |
| Video processing | FFmpeg |
| Video hosting | Cloudinary |
| Social media integration | Instagram Graph API |
| Data handling | JSON |
| Dashboard | HTML, CSS, JavaScript |

## How It Works

1. A new story topic is generated.
2. Gemini creates a structured story containing five scenes.
3. Each scene receives an AI-generated illustration.
4. Narration audio and synchronized captions are generated.
5. FFmpeg assembles the scenes into a vertical video.
6. Background music is selected based on the story mood.
7. The completed video can be uploaded and published as an Instagram Reel.
8. The dashboard records the run results.

## Project Structure

```text
Story_loop-AI-Agent/
│
├── story_gen.py       # Generates structured stories
├── topic_gen.py       # Suggests unique story topics
├── image_gen.py       # Generates scene illustrations
├── voice_gen.py       # Creates narration and captions
├── video_gen.py       # Assembles video scenes
├── music_gen.py       # Adds background music
├── pipeline.py        # Connects the generation workflow
├── publish_ig.py      # Instagram publishing integration
├── daily_run.py       # Runs the complete workflow
├── dashboard_gen.py   # Tracks execution history
├── dashboard.html     # Run monitoring dashboard
├── music/             # Background music files
└── output/            # Generated video files
```

## Setup and Configuration

### 1. Clone the repository

```bash
git clone https://github.com/Vidyavidu/Story_loop-AI-Agent.git
cd Story_loop-AI-Agent
```

### 2. Install dependencies

```bash
pip install google-genai python-dotenv pydantic huggingface-hub edge-tts requests cloudinary
```

### 3. Install FFmpeg

Install FFmpeg and ensure it is accessible from your system PATH.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

IG_USER_ID=your_instagram_user_id
IG_ACCESS_TOKEN=your_instagram_access_token
```

Keep `.env` out of Git. Never commit API keys or access tokens.

### 5. Run the pipeline

To generate a complete video from a story topic:

```bash
python pipeline.py
```

To run the daily topic-generation and publishing workflow:

```bash
python daily_run.py
```

Instagram publishing requires a properly configured Instagram professional account and valid API permissions.

## Learning Outcomes

- Working with multiple AI APIs in one application.
- Building modular Python automation pipelines.
- Generating structured content using LLMs.
- Integrating image generation and text-to-speech services.
- Processing audio, subtitles, and video programmatically.
- Connecting external APIs for social media automation.
- Tracking application execution through JSON and dashboards.

## Future Improvements

- Add a user-friendly interface for selecting story themes.
- Improve error handling and retry mechanisms.
- Add more narration voices and languages.
- Introduce scheduling and publishing controls.
- Improve dashboard analytics and monitoring.

---

**Story_loop** explores how AI can bring storytelling, content creation, and automation together in one workflow.
