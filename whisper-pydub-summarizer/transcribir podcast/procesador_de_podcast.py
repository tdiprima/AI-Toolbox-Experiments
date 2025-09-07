#!/usr/bin/env python3
"""
Podcast Transcription and Action Item Extraction Script

This script:
1. Segments a podcast audio file into chunks
2. Transcribes each segment using OpenAI Whisper
3. Extracts action items from transcripts using OpenAI GPT

Requirements:
- pip install pydub openai-whisper openai
- ffmpeg installed on your system
"""

import os

import whisper
from openai import OpenAI
from pydub import AudioSegment

# Configuration
AUDIO_FILE = "podcast.mp3"  # Change this to your podcast file
SEGMENT_LENGTH_MINUTES = 5  # Length of each segment in minutes
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"
OPENAI_API_KEY = "sk-..."  # Set your OpenAI API key here or use environment variable
GPT_MODEL = "gpt-3.5-turbo"  # or "gpt-4", "gpt-4-turbo-preview", etc.


def segment_audio(audio_file, segment_length_minutes=5):
    """
    Split audio file into segments of specified length.

    Args:
        audio_file: Path to the audio file
        segment_length_minutes: Length of each segment in minutes

    Returns:
        List of segment file paths
    """
    print(f"Loading audio file: {audio_file}")
    audio = AudioSegment.from_file(audio_file)
    segment_length_ms = segment_length_minutes * 60 * 1000

    segments = []
    total_segments = (len(audio) + segment_length_ms - 1) // segment_length_ms

    print(
        f"Splitting into {total_segments} segments of {segment_length_minutes} minutes each..."
    )

    for i in range(0, len(audio), segment_length_ms):
        segment_num = i // segment_length_ms
        segment = audio[i : i + segment_length_ms]
        segment_path = f"segment_{segment_num:03d}.mp3"
        segment.export(segment_path, format="mp3")
        segments.append(segment_path)
        print(f"  Created segment {segment_num + 1}/{total_segments}: {segment_path}")

    return segments


def transcribe_segments(segment_paths, model_name="base"):
    """
    Transcribe audio segments using Whisper.

    Args:
        segment_paths: List of paths to audio segments
        model_name: Whisper model to use

    Returns:
        List of transcription texts
    """
    print(f"\nLoading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    transcripts = []
    for idx, segment_path in enumerate(segment_paths):
        print(f"Transcribing segment {idx + 1}/{len(segment_paths)}: {segment_path}")
        result = model.transcribe(segment_path)
        transcripts.append(result["text"])
        print(f"  Transcribed {len(result['text'].split())} words")

    return transcripts


def extract_action_items(transcript, client, model="gpt-3.5-turbo"):
    """
    Extract action items from a transcript using OpenAI GPT.

    Args:
        transcript: The transcript text
        client: OpenAI client instance
        model: GPT model to use

    Returns:
        Extracted action items as text
    """
    prompt = (
        "Extract and summarize all key action items from the following transcript. "
        "Return them as a concise, bulleted task list. If there are no action items, say 'No action items found.'\n\n"
        f"Transcript:\n{transcript}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting action items: {str(e)}"


def cleanup_segments(segment_paths):
    """Remove temporary segment files."""
    for segment_path in segment_paths:
        if os.path.exists(segment_path):
            os.remove(segment_path)
            print(f"Removed temporary file: {segment_path}")


def main():
    """Main function to process the podcast."""

    # Check if audio file exists
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: Audio file '{AUDIO_FILE}' not found!")
        return

    # Initialize OpenAI client
    api_key = (
        OPENAI_API_KEY if OPENAI_API_KEY != "sk-..." else os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        print("Error: Please set your OpenAI API key!")
        print(
            "Either update OPENAI_API_KEY in the script or set the OPENAI_API_KEY environment variable."
        )
        return

    client = OpenAI(api_key=api_key)

    try:
        # Step 1: Segment the audio
        print("=" * 50)
        print("STEP 1: Segmenting Audio")
        print("=" * 50)
        segment_paths = segment_audio(AUDIO_FILE, SEGMENT_LENGTH_MINUTES)

        # Step 2: Transcribe segments
        print("\n" + "=" * 50)
        print("STEP 2: Transcribing Segments")
        print("=" * 50)
        transcripts = transcribe_segments(segment_paths, WHISPER_MODEL)

        # Step 3: Extract action items
        print("\n" + "=" * 50)
        print("STEP 3: Extracting Action Items")
        print("=" * 50)

        all_action_items = []
        for idx, transcript in enumerate(transcripts):
            print(f"\nProcessing segment {idx + 1}/{len(transcripts)}...")
            action_items = extract_action_items(transcript, client, GPT_MODEL)
            all_action_items.append(action_items)

        # Step 4: Output results
        print("\n" + "=" * 50)
        print("RESULTS: Action Items by Segment")
        print("=" * 50)

        for idx, action_items in enumerate(all_action_items):
            print(
                f"\n--- Segment {idx + 1} (minutes {idx * SEGMENT_LENGTH_MINUTES}-{(idx + 1) * SEGMENT_LENGTH_MINUTES}) ---"
            )
            print(action_items)

        # Save results to file
        output_file = "action_items_summary.txt"
        with open(output_file, "w") as f:
            f.write("PODCAST ACTION ITEMS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            for idx, action_items in enumerate(all_action_items):
                f.write(
                    f"Segment {idx + 1} (minutes {idx * SEGMENT_LENGTH_MINUTES}-{(idx + 1) * SEGMENT_LENGTH_MINUTES}):\n"
                )
                f.write(action_items + "\n\n")

        print(f"\n✅ Action items saved to: {output_file}")

    finally:
        # Cleanup temporary files
        print("\n" + "=" * 50)
        print("CLEANUP: Removing Temporary Files")
        print("=" * 50)
        cleanup_segments(segment_paths)
        print("\n✅ Processing complete!")


if __name__ == "__main__":
    main()
