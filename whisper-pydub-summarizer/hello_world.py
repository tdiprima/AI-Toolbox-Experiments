# Audio generation with PyDub and transcription setup with Whisper
import whisper
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile
import os


def main():
    print("Hello World - Whisper + PyDub Example")
    
    print("Creating a simple audio sample...")
    
    duration = 3000  # 3 seconds
    frequency = 440  # A4 note
    
    sine_wave = Sine(frequency).to_audio_segment(duration=duration)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        sine_wave.export(temp_path, format="wav")
        print(f"Generated audio file: {temp_path}")
        
        audio_info = AudioSegment.from_wav(temp_path)
        print(f"Audio duration: {len(audio_info) / 1000:.2f} seconds")
        print(f"Audio sample rate: {audio_info.frame_rate} Hz")
        print(f"Audio channels: {audio_info.channels}")
        
        try:
            model = whisper.load_model("base")
            result = model.transcribe(temp_path)
            print(f"\nWhisper transcription: {result['text']}")
        except Exception as e:
            print(f"Note: Whisper transcription failed (expected for sine wave): {e}")
            print("Whisper is typically used for speech, not pure tones.")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
            print("Cleaned up temporary audio file")


if __name__ == "__main__":
    main()
