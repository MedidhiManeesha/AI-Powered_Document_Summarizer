import os
import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('AZURE_BLOB_CONTAINER', 'documents')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlobHelper:
    """Helper class for Azure Blob Storage operations."""
    def __init__(self):
        if not AZURE_STORAGE_CONNECTION_STRING:
            logger.error('Missing AZURE_STORAGE_CONNECTION_STRING')
            raise ValueError('Missing Azure Storage connection string')
        self.service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.service_client.get_container_client(CONTAINER_NAME)
        try:
            self.container_client.create_container()
        except Exception:
            pass  # Container may already exist

    def upload_file(self, file_path, blob_name):
        try:
            with open(file_path, 'rb') as data:
                self.container_client.upload_blob(name=blob_name, data=data, overwrite=True)
            logger.info(f"Uploaded {file_path} to blob {blob_name}")
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise

    def download_file(self, blob_name, download_path):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_path, 'wb') as file:
                file.write(blob_client.download_blob().readall())
            logger.info(f"Downloaded {blob_name} to {download_path}")
        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise
