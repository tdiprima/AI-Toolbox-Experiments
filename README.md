# AI Toolbox Experiments

A collection of practical AI experiments and tools exploring various frameworks and libraries for building intelligent applications.

## 🛠️ Projects

### AutoGen Multi-Agent Development
**[autogen-dev-team/](./autogen-dev-team/)**  
Simulates a mini development team using Microsoft's AutoGen framework. Two AI agents collaborate: one generates Python sorting algorithms while another tests and critiques the code through iterative conversations.

### FastAPI + OpenAI Code Refactoring
**[fastapi-openai-refactor/](./fastapi-openai-refactor/)**  
A REST API service that leverages OpenAI's models to automatically refactor code for better efficiency and readability. Submit code via `/refactor` endpoint and receive improved versions with explanations.

### Gradio Sentiment Analysis UI
**[gradio-sentiment-ui/](./gradio-sentiment-ui/)**  
A web-based sentiment analysis tool built with Gradio and Hugging Face transformers. Analyze text emotions through a simple interface with downloadable CSV results.

### Haystack Document Q&A
**[haystack-doc-qa/](./haystack-doc-qa/)**  
Intelligent document search using Haystack's NLP framework. Indexes technical blog PDFs and enables natural language queries with sourced answers from the documents.

### LangChain RAG Agent
**[langchain-rag-agent/](./langchain-rag-agent/)**  
Retrieval-Augmented Generation (RAG) implementation using LangChain for building context-aware AI agents.

### Pandas AI Data Analysis
**[pandas-ai-queries/](./pandas-ai-queries/)**  
Natural language data analysis using PandasAI. Query datasets in plain English and get automated insights and visualizations.

### Whisper Podcast Processor
**[whisper-pydub-summarizer/](./whisper-pydub-summarizer/)**  
Audio processing pipeline that segments podcasts, transcribes content using OpenAI Whisper, and generates summaries with action items using GPT models.

## Explaining READMEs
Courtesy of ChatGPT

## 🚀 Getting Started

Each project contains its own README with detailed setup instructions and usage examples. Most experiments require:

- Python 3.8+
- OpenAI API key (for GPT-powered features)
- Project-specific dependencies (see individual requirements.txt files)

## 📋 Requirements

Individual projects may require additional setup:

- **Audio processing**: FFmpeg installation
- **PDF processing**: PyPDF libraries
- **Web interfaces**: FastAPI, Gradio, or Streamlit
- **Vector databases**: FAISS, Elasticsearch (for advanced search)

## 🎯 Purpose

These experiments demonstrate practical applications of:

- Multi-agent AI systems
- Natural language processing
- Document intelligence
- Audio/video processing
- Web API development
- Interactive ML interfaces

<br>
