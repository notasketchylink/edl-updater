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
logging.basicConfig(filename=f'{logs_path}/domain_handler.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)d %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

# regular expression to match domain names and ignore IP addresses
#this regex works well with some threat feeds but not others
domain_regex = re.compile(r"(https?:\/\/)?((?!\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})([\da-z\.-]+))\.([a-z\.]{2,6})([\/\w \.-]*)*\/?")

# regular expression to match domain names and ignore IP addresses
#this regex works well with some threat feeds but not others
#domain_regex = re.compile(r"(https?:\/\/(([a-zA-Z0-9-]+\.){1,})([a-zA-Z]{2,}))")

# Create a defaultdict to store the FQDNS
domain_dict = defaultdict(list)

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
                # check if line is an IP address
                match_ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if match_ip:
                    continue
                # Search for FQDNs in the line
                matches = domain_regex.findall(line)
                # Add the matches to the domain_dict
                for match in matches:
# This line works with the first fqdn regex
                    domain = match[2]+'.'+match[3]
# This line works with the second fqdn regex
#                   domain = match[1]+match[3]
# this line is for testing output of the list after the regex has been changed
#                    domain = '_match0_'+match[0]+'_match1_'+match[1]+'_match2_'+match[2]+'_match3_'+match[3] #+'_match4_'+match[4]
                    domain_dict[domain].append(file_name)
    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")

# Write the lists to a file in the output folder
with open(os.path.join(output_path, "FQDNs.txt"), 'w') as file:
    for domain, files in domain_dict.items():
        file.write(f"{domain}\n")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
with open(os.path.join(logs_path, f"{timestamp}-Annotated_FQDNs.txt"), 'w') as file:
    for domain, files in domain_dict.items():
        file.write(f"{domain} # from file(s): {', '.join(files)}\n")
