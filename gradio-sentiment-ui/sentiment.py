import gradio as gr
from transformers import pipeline
import pandas as pd
import tempfile
import os

# Load a pre-trained sentiment analysis model from Hugging Face
sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# Function to analyze sentiment and prepare results
def analyze(text):
    # Analyze the sentiment of the input text
    result = sentiment_model(text)
    
    # Extract the label and score
    label = result[0]['label']
    score = result[0]['score']
    
    # Prepare the results in a dictionary
    results = {
        "Text": text,
        "Sentiment": label,
        "Score": score
    }
    
    # Convert results to a DataFrame and save to temporary CSV file
    df = pd.DataFrame([results])
    
    # Create a temporary CSV file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    df.to_csv(temp_file.name, index=False)
    temp_file.close()
    
    return results, temp_file.name

# Gradio interface
iface = gr.Interface(
    fn=analyze,  # Function to wrap
    inputs=gr.Textbox(lines=2, placeholder="Enter text here..."),  # Text input
    outputs=[
        gr.JSON(label="Sentiment Analysis Result"),  # Display results as JSON
        gr.File(label="Download CSV")  # CSV download button
    ],
    live=False,
    title="Sentiment Analysis with CSV Export",
    description="Enter text to analyze sentiment and download results as CSV."
)

# Launch the interface
iface.launch(share=True)
