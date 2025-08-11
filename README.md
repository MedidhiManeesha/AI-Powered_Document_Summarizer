# AI-Powered Document Summarizer (Azure OpenAI)

An intelligent document summarization tool built with **Azure OpenAI Service** that extracts key points from long documents, making it easier for users to quickly grasp the core information.

## Features
- Upload PDF, DOCX, or TXT files.
- Extracts text using `PyMuPDF` (PDF) and `python-docx` (DOCX).
- Sends extracted content to **Azure OpenAI GPT model** for concise summarization.
- Simple **Streamlit web interface** for easy interaction.
- Download summarized text as a `.txt` file.
- Session history of previous uploads and summaries.

## Architecture
1. **Frontend**: Streamlit interface for file upload and results display.
2. **Backend**: Python with Azure OpenAI API for summarization.
3. **Text Extraction**: PyMuPDF, python-docx for reading documents.
4. **Azure Function**: Processes uploaded docs, extracts text, calls OpenAI, returns summaries.
5. **Blob Storage**: Stores uploaded documents and summaries.

## Tech Stack
- Python
- Streamlit
- Azure OpenAI
- Azure Functions
- Azure Blob Storage
- PyMuPDF / python-docx

## Azure Setup
1. **Azure Blob Storage**: Create a storage account and container (e.g., `documents`).
2. **Azure OpenAI**: Deploy a GPT model (e.g., `gpt-35-turbo`).
3. **Azure Functions**: Deploy the function in `azure_function/` (Python v3.9+).
4. Set environment variables (see `.env.example`).

## Local Development
1. Clone the repo and install dependencies:
   ```bash
   git clone <repo-url>
   cd AI-Powered_Document_Summarizer
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your Azure credentials.
3. Start the Azure Function locally:
   ```bash
   cd azure_function
   func start
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Upload a PDF, DOCX, or TXT file.
- Wait for processing and view summaries.
- Download summaries as `.txt`.
- View session history in the sidebar.

## File Structure
```
/document-summarizer
  ├── app.py                  # Streamlit UI  
  ├── azure_function/         # Azure Function code  
  │   ├── __init__.py         # Main function handler  
  │   ├── requirements.txt    # Azure Function deps  
  ├── blob_helper.py          # Upload/download to Blob Storage  
  ├── openai_helper.py        # Summarization logic with Azure OpenAI  
  ├── requirements.txt        # App dependencies  
  ├── .env.example            # Example env vars file  
  ├── README.md               # Setup & usage  
  └── sample_data/            # Sample docs for testing  
```

