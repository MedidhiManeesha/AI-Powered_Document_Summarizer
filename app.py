import streamlit as st
import os
import tempfile
import logging
from blob_helper import BlobHelper
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv('AZURE_FUNCTION_API_URL', 'http://localhost:7071/api')

st.set_page_config(page_title="AI Document Summarizer (Azure)", layout="centered")
st.title("AI-Powered Document Summarizer")

if 'history' not in st.session_state:
    st.session_state['history'] = []

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        blob_helper = BlobHelper()
        blob_name = os.path.basename(tmp_path)
        blob_helper.upload_file(tmp_path, blob_name)
        st.info("File uploaded. Processing...")
        # Call Azure Function endpoint (simulate trigger)
        resp = requests.post(f"{API_BASE_URL}/summarize", json={"blob_name": blob_name})
        if resp.status_code == 200:
            result = resp.json()
            short_summary = result.get('short_summary', '')
            detailed_summary = result.get('detailed_summary', '')
            st.session_state['history'].append({
                'file': uploaded_file.name,
                'short': short_summary,
                'detailed': detailed_summary
            })
            st.success("Summarization complete!")
            st.subheader("Short Summary")
            st.write(short_summary)
            st.subheader("Detailed Summary")
            st.write(detailed_summary)
            # Download button
            summary_text = f"Short Summary:\n{short_summary}\n\nDetailed Summary:\n{detailed_summary}"
            st.download_button("Download Summary as .txt", summary_text, file_name=uploaded_file.name+".summary.txt")
        else:
            st.error(f"Summarization failed: {resp.text}")
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error(f"Error: {e}")

if st.session_state['history']:
    st.sidebar.header("Session History")
    for i, item in enumerate(reversed(st.session_state['history'])):
        st.sidebar.markdown(f"**{item['file']}**\n- Short: {item['short']}\n- Detailed: {item['detailed'][:100]}...")
