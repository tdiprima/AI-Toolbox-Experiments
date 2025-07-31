import gradio as gr
from transformers import pipeline
import pandas as pd
import tempfile
import os

# Load a pre-trained sentiment analysis model from Hugging Face
sentiment_model = None
try:
    print("Loading sentiment analysis model...")
    sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading specific model: {e}")
    try:
        print("Trying default sentiment analysis model...")
        sentiment_model = pipeline("sentiment-analysis")
        print("Default model loaded successfully")
    except Exception as e2:
        print(f"Error loading default model: {e2}")
        sentiment_model = None

# Function to analyze sentiment and prepare results
def analyze(text):
    try:
        # Check if model is loaded
        if sentiment_model is None:
            return {"Error": "Model failed to load"}, None
        
        # Validate input - handle boolean inputs properly
        print(f"Input received: {repr(text)} (type: {type(text)})")
        
        if text is None or text is False or text == "":
            return {"Error": "Please enter some text to analyze"}, None
        
        # Convert to string safely
        if isinstance(text, bool):
            return {"Error": "Invalid input type received"}, None
        
        
        # Convert text to string and validate it's not empty
        try:
            text_str = str(text).strip()
            if text_str == "" or text_str == "False" or text_str == "True":
                return {"Error": "Please enter some text to analyze"}, None
        except Exception as str_error:
            print(f"Error converting text to string: {str_error}")
            return {"Error": "Invalid text input"}, None
        
        # Analyze the sentiment of the input text
        print(f"Analyzing text: {text_str[:50]}...")  # Log first 50 chars
        result = sentiment_model(text_str)
        print(f"Analysis result: {result}")  # Log the raw result
        
        # Validate result format
        if not result or not isinstance(result, list) or len(result) == 0:
            return {"Error": "Invalid response from sentiment model"}, None
        
        # Extract the label and score
        label = result[0].get('label', 'UNKNOWN')
        score = result[0].get('score', 0.0)
        
        # Prepare the results in a dictionary
        results = {
            "Text": text_str,
            "Sentiment": label,
            "Score": float(score)
        }
        
        # Convert results to a DataFrame and save to temporary CSV file
        df = pd.DataFrame([results])
        
        # Create a temporary CSV file with proper permissions
        temp_dir = tempfile.gettempdir()
        temp_filename = f"sentiment_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        temp_filepath = os.path.join(temp_dir, temp_filename)
        
        df.to_csv(temp_filepath, index=False)
        print(f"CSV file created at: {temp_filepath}")
        
        return results, temp_filepath
        
    except Exception as e:
        error_message = f"Error during analysis: {str(e)}"
        print(error_message)
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return {"Error": error_message}, None

# Gradio interface
try:
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
    iface.launch()
    # iface.launch(share=True)
    
except Exception as e:
    print(f"Error creating or launching Gradio interface: {e}")
