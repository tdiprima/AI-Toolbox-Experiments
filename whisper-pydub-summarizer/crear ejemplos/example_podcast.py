from gtts import gTTS

# Create a test "podcast" with action items
text = """
Welcome to our productivity podcast. Today we'll discuss three key action items.

First, we need to schedule a meeting with the marketing team next Tuesday to review the Q4 campaign strategy.

Second, everyone should complete the customer feedback survey by Friday. The link will be sent via email.

Third, please update your project status reports in the shared drive by end of day Thursday.

Let's dive deeper into each of these items...
"""

tts = gTTS(text=text, lang='en', slow=False)
tts.save("podcast.mp3")
