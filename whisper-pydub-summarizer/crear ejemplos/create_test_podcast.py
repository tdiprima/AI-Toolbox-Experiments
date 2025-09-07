#!/usr/bin/env python3
"""
Create a test podcast MP3 file with clear action items for testing the transcription script.
"""

try:
    pass

    from gtts import gTTS

    # Create a realistic podcast script with multiple segments and action items
    podcast_script = """
    Welcome to the Tech Leadership Podcast, episode 47. I'm your host, and today we're discussing 
    project management best practices and team productivity.

    Let's start with our first topic: sprint planning. One critical action item for all team leads is to 
    implement weekly sprint retrospectives. This means every Friday at 3 PM, gather your team for a 
    30-minute review session.

    Moving on to our second point about documentation. Here's what you need to do: create a shared wiki 
    page for your project by next Monday. Include sections for architecture decisions, API documentation, 
    and deployment procedures.

    Now, let's talk about code reviews. Action item number three: establish a code review checklist 
    and share it with your team by Wednesday. This checklist should include items like test coverage, 
    coding standards, and security considerations.

    Our fourth topic is about communication. Everyone needs to set up a daily standup meeting. 
    Keep it to 15 minutes maximum, and focus on blockers and daily goals.

    For our fifth and final topic today, let's discuss professional development. Your action item here 
    is to schedule one-on-one meetings with each team member to discuss their career goals. 
    These should happen within the next two weeks.

    Before we wrap up, remember to update your project roadmap in Jira, send out the meeting notes 
    from today's planning session, and review the new security guidelines posted on the company portal.

    That's all for today's episode. Thanks for listening, and we'll see you next week!
    """

    # Create the MP3 file
    print("Creating test podcast MP3 file...")
    tts = gTTS(text=podcast_script, lang="en", slow=False)
    tts.save("podcast.mp3")
    print("✅ Successfully created 'podcast.mp3'")
    print(
        "File contains a ~2 minute podcast with multiple clear action items for testing."
    )

except ImportError:
    print("❌ Error: gTTS not installed.")
    print("Please install it with: pip install gtts")
    print("\nAlternatively, you can download a real podcast episode from:")
    print("- NPR: https://www.npr.org/podcasts")
    print("- TED Talks: https://www.ted.com/talks")
    print("- Archive.org: https://archive.org/details/podcasts")
