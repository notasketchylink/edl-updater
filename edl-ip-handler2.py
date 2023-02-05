import os
import re
import logging
from collections import defaultdict
import time
import datetime
import zipfile

# Set the output paths
sanitized_path = '/scripts/python3/edl-updater/sanitized'
output_path = '/scripts/python3/edl-updater/output'
logs_path = '/scripts/python3/edl-updater/logs'

# Configure logging
logging.basicConfig(filename=f'{logs_path}/ip_handler.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)d %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

# Create a regular expression to match IP addresses and IP subnets in CIDR format
ip_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b')

# Create a defaultdict to store the IP addresses and IP subnets
ip_dict = defaultdict(list)

# Create the "log", "sanitized", and "output" directories if they don't exist
os.makedirs(sanitized_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
os.makedirs(logs_path, exist_ok=True)

# Iterate through the files in the sanitized folder
for file_name in os.listdir(sanitized_path):
    try:
        # Open the file for reading
        with open(os.path.join(sanitized_path, file_name), 'r') as file:
            # Iterate through the lines in the file
            for line in file:
                # Ignore lines that start with '#' or whitespace
                if line.startswith('#') or line.startswith(' '):
                    continue
                # Search for IP addresses and IP subnets in the line
                matches = ip_regex.findall(line)
                # Add the matches to the ip_dict
                for match in matches:
                    ip_dict[match].append(file_name)
    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")

# Write the lists to a file in the output folder
with open(os.path.join(output_path, "IPs.txt"), 'w') as file:
    for ip, files in ip_dict.items():
        file.write(f"{ip}\n")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
with open(os.path.join(logs_path, f"{timestamp}-Annotated_IPs.txt"), 'w') as file:
    for ip, files in ip_dict.items():
        file.write(f"{ip} # from file(s): {', '.join(files)}\n")
