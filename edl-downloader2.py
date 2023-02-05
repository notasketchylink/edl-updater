import os
import datetime
import time
import urllib.request
import zipfile
import logging
from urllib.parse import urlparse

# URLs of threat intel feeds to download
urls = [
    "URL1",
    "URL2",
    "URL3",
    "URL4",
    "URl5"
]

#Set the output paths, use the full path
raw_path = '/scripts/python3/edl-updater/raw'
raw_archived_path = '/scripts/python3/edl-updater/raw_archived'
output_path = '/scripts/python3/edl-updater/output'
logs_path = '/scripts/python3/edl-updater/logs'
logs_archived_path = '/scripts/python3/edl-updater/logs/archived'
sanitized_path = '/scripts/python3/edl-updater/sanitzed'

# Create the "raw", "raw_archived", and "output" directories if they don't exist
os.makedirs(raw_path, exist_ok=True)
os.makedirs(raw_archived_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
os.makedirs(logs_path, exist_ok=True)
os.makedirs(logs_archived_path, exist_ok=True)
os.makedirs(sanitized_path, exist_ok=True)

# Configure logging
logging.basicConfig(filename=f'{logs_path}/edl_updater.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)d %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

# Download the files and save them in the "raw" directory with timestamps
for url in urls:
    try:
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
        # Get the file name from the URL
        file_name = os.path.basename(url)
        # Get the FQDN from the URL
        fqdn = urlparse(url).netloc.replace(".","_")
        # Append the timestamp, FQDN and url to the file name
        if not file_name.endswith(".txt"):
            file_name = f"{file_name}.txt"
        file_name = f"{timestamp}_{fqdn}_{file_name}"
        # Download the file
        urllib.request.urlretrieve(url, f"{raw_path}/{file_name}")
        logging.info(f"Successfully downloaded {file_name} from {url}")
    except Exception as e:
        logging.error(f"Failed to download {file_name} from {url}: {str(e)}")

# Compress and archive any file 60 minutes or older in the raw folder
for file in os.listdir(raw_path):
    filepath = os.path.join(raw_path, file)
    if os.path.isfile(filepath):
        current_time = time.time()
        file_time = os.path.getmtime(filepath)
        if current_time - file_time > 3600:  # 60 minutes or older
            try:
                with zipfile.ZipFile(f'{raw_archived_path}/{file}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(filepath, arcname=file)
                os.remove(filepath)
                logging.info(f"File {file} archived successfully.")
            except Exception as e:
                logging.error(f"Error compressing and archiving file {file}: {e}")

# Compress and archive any file 1 day or older in the log folder
for file in os.listdir(logs_path):
    filepath = os.path.join(logs_path, file)
    if os.path.isfile(filepath):
        current_time = time.time()
        file_time = os.path.getmtime(filepath)
        if current_time - file_time > 86400:  # 1 day or older
            try:
                with zipfile.ZipFile(f'{logs_archived_path}/{file}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(filepath, arcname=file)
                os.remove(filepath)
                logging.info(f"File {file} archived successfully.")
            except Exception as e:
                logging.error(f"Error compressing and archiving file {file}: {e}")

# Delete any file 59 minutes or older in the sanitized folder
for file in os.listdir(sanitized_path):
    filepath = os.path.join(sanitized_path, file)
    if os.path.isfile(filepath):
        current_time = time.time()
        file_creation_time = os.path.getctime(filepath)
        # calculate the difference between current time and file creation time
        time_diff = current_time - file_creation_time
        # check if the difference is greater than 59 minutes (in seconds)
        if time_diff >= 59 * 60:
            try:
                os.remove(filepath)
                logging.info(f"File {file} deleted successfully.")
            except Exception as e:
                logging.error(f"Error deleting file {file}: {e}")
