import gradio as gr
from transformers import pipeline
import pandas as pd
import io
import tempfile
import os

# Load the sentiment analysis model from Hugging Face
sentiment_model = pipeline("sentiment-analysis")

# Function to analyze sentiment and return results
def analyze(text):
    # Get sentiment analysis results
    results = sentiment_model(text)
    
    # Prepare results for display
    scores = [{"label": res['label'], "score": res['score']} for res in results]
    
    # Convert results to DataFrame for CSV export
    df = pd.DataFrame(scores)
    
    # Create temporary file for CSV
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    df.to_csv(temp_file.name, index=False)
    temp_file.close()
    
    return scores, temp_file.name

# Create the Gradio interface
iface = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(lines=5, placeholder="Enter text here..."),
    outputs=[
        gr.Textbox(label="Sentiment Scores"),
        gr.File(label="Download CSV")
    ],
    live=False,
    title="Sentiment Analysis with Hugging Face",
    description="Enter some text and get the sentiment analysis results. You can also download the results as a CSV file."
)

# Launch the interface
iface.launch()
