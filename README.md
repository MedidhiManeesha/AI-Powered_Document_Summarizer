# AI-Powered Document Summarizer (Azure OpenAI)

An intelligent document summarization tool built with **Azure OpenAI Service** that extracts key points from long documents, making it easier for users to quickly grasp the core information.

## Features
- Upload PDF, DOCX, or TXT files.
- Extracts text using `PyMuPDF` (PDF) and `python-docx` (DOCX).
- Sends extracted content to **Azure OpenAI GPT model** for concise summarization.
- Simple **Streamlit web interface** for easy interaction.
- Download summarized text as a `.txt` file.

## Architecture
1. **Frontend**: Streamlit interface for file upload and results display.
2. **Backend**: Python with Azure OpenAI API for summarization.
3. **Text Extraction**: PyMuPDF, python-docx for reading documents.
4. **Output**: Summarized text with option to save locally.

## Tech Stack
- Python
- Streamlit
- Azure OpenAI
- PyMuPDF / python-docx

## Installation
```bash
git clone https://github.com/username/AI-Document-Summarizer.git
cd AI-Document-Summarizer
pip install -r requirements.txt
