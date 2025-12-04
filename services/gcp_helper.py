import os
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError, NotFound
from dotenv import load_dotenv
import logging

# ==============================================================
# Load environment variables
# ==============================================================
load_dotenv()

bucket_name = os.getenv("GCP_BUCKET_NAME")

if not bucket_name:
    raise ValueError("❌ GCP_BUCKET_NAME not set in .env file")

# ==============================================================
# GCS Client Helper
# ==============================================================
def get_gcs_client() -> storage.Client:
    """
    Creates and returns a Google Cloud Storage client.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable must point to your JSON key.
    """
    try:
        client = storage.Client()
        return client
    except Exception as e:
        logging.error(f"❌ Failed to initialize GCS client: {e}")
        raise

# ==============================================================
# Upload File
# ==============================================================
def upload_to_gcp_bucket(local_path: str, bucket_path: str) -> str:
    """
    Uploads a file from local path to the specified path in GCS.
    Makes the file public and returns its public URL.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(bucket_path)

        blob.upload_from_filename(local_path)
        #blob.make_public()

        public_url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"
        logging.info(f"✅ Uploaded {local_path} → {public_url}")
        return public_url

    except GoogleAPICallError as e:
        logging.error(f"❌ GCS API error while uploading: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error uploading to GCS: {e}")
        raise

# ==============================================================
# Download File
# ==============================================================
def download_from_gcp_bucket(bucket_path: str, local_path: str) -> None:
    """
    Downloads a file from GCS to local path.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(bucket_path)

        if not blob.exists():
            raise FileNotFoundError(f"File {bucket_path} not found in GCS bucket {bucket_name}")

        blob.download_to_filename(local_path)
        logging.info(f"✅ Downloaded gs://{bucket_name}/{bucket_path} → {local_path}")

    except NotFound:
        logging.error(f"❌ File not found: {bucket_path}")
        raise
    except GoogleAPICallError as e:
        logging.error(f"❌ GCS API error while downloading: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error downloading from GCS: {e}")
        raise

# ==============================================================
# Read Text File
# ==============================================================
def read_text_from_gcp_bucket(bucket_path: str) -> str:
    """
    Reads a text file directly from GCS and returns its content as a string.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(bucket_path)

        if not blob.exists():
            raise FileNotFoundError(f"File {bucket_path} not found in GCS bucket {bucket_name}")

        text_data = blob.download_as_text()
        logging.info(f"✅ Read text from gs://{bucket_name}/{bucket_path}")
        return text_data

    except NotFound:
        logging.error(f"❌ File not found: {bucket_path}")
        raise
    except GoogleAPICallError as e:
        logging.error(f"❌ GCS API error while reading text: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error reading text from GCS: {e}")
        raise

# ==============================================================
# Delete File (Optional)
# ==============================================================
def delete_from_gcp_bucket(bucket_path: str) -> bool:
    """
    Deletes a file from GCS bucket.
    Returns True if deleted successfully.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(bucket_path)

        if not blob.exists():
            logging.warning(f"⚠️ File not found in bucket: {bucket_path}")
            return False

        blob.delete()
        logging.info(f"🗑️ Deleted gs://{bucket_name}/{bucket_path}")
        return True

    except Exception as e:
        logging.error(f"❌ Failed to delete file from GCS: {e}")
        raise
