import os
import logging
import openai
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-35-turbo')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"

def summarize_text(text):
    """Summarize text using Azure OpenAI. Returns (short_summary, detailed_summary)."""
    if not AZURE_OPENAI_KEY or not AZURE_OPENAI_ENDPOINT:
        logger.error('Missing Azure OpenAI credentials')
        raise ValueError('Missing Azure OpenAI credentials')
    try:
        prompt_short = f"Summarize the following in 1-2 sentences:\n{text}"
        prompt_detailed = f"Summarize the following in 3-5 bullet points:\n{text}"
        short_resp = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt_short}],
            max_tokens=128,
            temperature=0.5
        )
        detailed_resp = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt_detailed}],
            max_tokens=256,
            temperature=0.5
        )
        short_summary = short_resp['choices'][0]['message']['content'].strip()
        detailed_summary = detailed_resp['choices'][0]['message']['content'].strip()
        logger.info('Summarization successful')
        return short_summary, detailed_summary
    except Exception as e:
        logger.error(f"OpenAI summarization failed: {e}")
        raise
