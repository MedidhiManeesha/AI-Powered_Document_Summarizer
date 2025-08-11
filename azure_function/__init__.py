import logging
import os
import azure.functions as func
from blob_helper import BlobHelper
from openai_helper import summarize_text
import fitz  # PyMuPDF
import docx

def extract_text(file_path, file_type):
    if file_type == '.pdf':
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)
    elif file_type == '.docx':
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_type == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError('Unsupported file type')

def main(blob: func.InputStream):
    logging.info(f"Processing blob: {blob.name}, Size: {blob.length} bytes")
    file_name = os.path.basename(blob.name)
    file_type = os.path.splitext(file_name)[1].lower()
    temp_path = f"/tmp/{file_name}"
    with open(temp_path, 'wb') as f:
        f.write(blob.read())
    try:
        text = extract_text(temp_path, file_type)
        short_summary, detailed_summary = summarize_text(text)
        result = {
            'short_summary': short_summary,
            'detailed_summary': detailed_summary
        }
        # Optionally, write summaries back to Blob Storage
        blob_helper = BlobHelper()
        summary_blob = file_name + '.summary.txt'
        with open(f"/tmp/{summary_blob}", 'w', encoding='utf-8') as f:
            f.write(f"Short Summary:\n{short_summary}\n\nDetailed Summary:\n{detailed_summary}")
        blob_helper.upload_file(f"/tmp/{summary_blob}", summary_blob)
        logging.info('Summaries written to blob storage')
        return result
    except Exception as e:
        logging.error(f"Error processing document: {e}")
        raise
