from pydub import AudioSegment
import whisper
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio = AudioSegment.from_file("podcast.mp3")
segment_length_ms = 5 * 60 * 1000  # 5 minutes in milliseconds

# Split the podcast into 5-minute chunks
segments = []
for i in range(0, len(audio), segment_length_ms):
    segment = audio[i:i+segment_length_ms]
    segment.export(f"segment_{i//segment_length_ms}.mp3", format="mp3")
    segments.append(f"segment_{i//segment_length_ms}.mp3")

#---

# Transcribe Each Segment with Whisper
model = whisper.load_model("base")  # or "small", "medium", "large"

transcripts = []
for segment_path in segments:
    result = model.transcribe(segment_path)
    transcripts.append(result['text'])

#---

# Summarize Transcripts into Task Lists with LLM
def summarize_action_items(transcript):
    prompt = (
        "Extract and summarize all key action items from the following transcript. "
        "Return them as a concise, bulleted task list. If there are no action items, say 'No action items.'\n\n"
        f"Transcript:\n{transcript}"
    )
    response = client.chat.completions.create(model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=300,
    temperature=0.2)
    return response.choices[0].message.content

all_action_items = []
for transcript in transcripts:
    action_items = summarize_action_items(transcript)
    all_action_items.append(action_items)

#---

# Output the Results
for idx, action_items in enumerate(all_action_items):
    print(f"Segment {idx+1} action items:\n{action_items}\n")
