### 🔊 Transcribe + Summarize Podcast Audio using PyDub, Whisper, and GPT

This guide walks you through:

* Splitting a podcast into chunks with **PyDub**
* Transcribing each chunk using **Whisper**
* Summarizing transcripts into action items using an **LLM** (like GPT-4)

## 🧱 1. Install Dependencies

You’ll need the following:

* [`pydub`](https://github.com/jiaaro/pydub): for audio processing
* [`openai-whisper`](https://github.com/openai/whisper): for transcription
* [`openai`](https://github.com/openai/openai-python): to call GPT models
* **`ffmpeg`**: required by PyDub and Whisper to handle audio formats

Install everything with:

```bash
pip install pydub openai-whisper openai

# Plus ffmpeg (required for mp3 processing):
# macOS:   brew install ffmpeg
# Ubuntu:  sudo apt install ffmpeg
```

## ✂️ 2. Split the Podcast into Chunks (e.g. 5-minute segments)

```python
from pydub import AudioSegment

audio = AudioSegment.from_file("podcast.mp3")
segment_length_ms = 5 * 60 * 1000  # 5 minutes converted to milliseconds

segments = []

for i in range(0, len(audio), segment_length_ms):
    # Slice the audio: get a 5-minute chunk from position i
    segment = audio[i:i+segment_length_ms]

    # Export that chunk to a new MP3 file
    filename = f"segment_{i // segment_length_ms}.mp3"
    segment.export(filename, format="mp3")

    # Keep track of the filename so we can process it later
    segments.append(filename)
```

### 🧠 What’s going on?

* `audio[i:i+segment_length_ms]`: This slices the audio just like slicing a list or string. It grabs a chunk starting at millisecond `i`, ending at `i + segment_length_ms`.
* `segment.export(...)`: Saves the sliced chunk as its own `.mp3` file.
* `i // segment_length_ms`: This gives the segment number (e.g. 0, 1, 2...) by integer-dividing the current millisecond offset by the segment length. Used to name each chunk like `segment_0.mp3`, `segment_1.mp3`, etc.

## 🧾 3. Transcribe Each Segment with Whisper

```python
import whisper

model = whisper.load_model("base")  # you can also try "small", "medium", or "large"

transcripts = []

for segment_path in segments:
    result = model.transcribe(segment_path)
    transcripts.append(result['text'])
```

Each MP3 segment gets transcribed. Whisper gives back a dictionary, and `result['text']` contains the transcript string for that chunk.

## ✍️ 4. Summarize Transcripts into Action Items (with GPT)

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_action_items(text):
    prompt = (
        "Summarize the following meeting transcript into a list of key action items:\n\n"
        f"{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

summaries = [summarize_action_items(t) for t in transcripts]
```

### Notes:

* This assumes you’ve set your `OPENAI_API_KEY` in your environment variables.
* You can adjust the prompt or summarization style to match your needs (e.g., bullet points, formal write-up, TODO list, etc).

## ✅ Output

You’ll end up with a list of summary strings for each chunk of the podcast. From there, you can combine them, format into Markdown, or feed them into another system like Notion or Slack.

<br>
