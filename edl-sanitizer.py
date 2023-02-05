import os
import logging
import re
import html
import string
import concurrent.futures
import ipaddress

# Compile the regular expression pattern to match non-ASCII characters
non_ascii_pattern = re.compile(r"[^\x00-\x7F]+")

def sanitize_line(line):
    """
    This function cleans a single line from the input file.
    It removes leading and trailing whitespaces, unescapes any HTML entities, removes any HTML tags, removes any non-ASCII characters and converts the line to lowercase.
    If the line contains a comment symbol "#" or ";", everything after it is removed.
    """
    line = line.strip()
    comment_index = line.find("#")
    semicolon_index = line.find(";")
    if comment_index == -1 and semicolon_index == -1:
        line = html.unescape(line)
        line = re.sub(r"<[^<]+?>", "", line)
        line = re.sub(non_ascii_pattern, "", line)
        return line.lower()
    else:
        comment_index = min(filter(lambda x: x != -1, [comment_index, semicolon_index]))
        line = line[:comment_index].strip()
        if line:
            line = html.unescape(line)
            line = re.sub(r"<[^<]+?>", "", line)
            line = re.sub(non_ascii_pattern, "", line)
            return line.lower()
        else:
            return ""

def sanitize_file(file_path, output_file, whitelist_domains, whitelist_networks):
    """
    This function cleans a file and writes the output to another file.
    It sanitizes each line from the input file and writes it to the output file if it doesn't contain a domain or IP address from the whitelist.
    """
    try:
        with open(file_path, "r") as input_file, open(output_file, "w") as output:
            for line in input_file:
                line = sanitize_line(line)
                if line:
                    skip = False
                    for domain in whitelist_domains:
                        if domain in line:
                            skip = True
                            break
                    if skip:
                        continue
                    try:
                        ip = ipaddress.ip_address(line)
                        for network in whitelist_networks:
                            """
                            Is the IP within a subnet listed in the whitelist, if so the line is skipped
                            """
                            if ip in network or ipaddress.ip_network(line).subnet_of(network):
                                skip = True
                                break
                            """
                            Does the line match a subnet specified in the whitelist, if so the line is skipped
                            """
                            if ip in line:
                                skip = True
                                break
                        if not skip:
                            output.write(line + "\n")
                    except ValueError:
                        output.write(line + "\n")
    except Exception as e:
        logging.error("Error processing file {}: {}".format(file_path, e))

def load_whitelist_domains(file_path):
    """
    This function loads the domain whitelist into memory
    """
    with open(file_path, "r") as input_file:
        return set(line.strip().lower() for line in input_file)

def load_whitelist_networks(file_path):
    """
    This function loads the network whitelist into memory
    """
    networks = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                try:
                    networks.append(ipaddress.ip_network(line))
                except ValueError as e:
                    logging.error("Error parsing network: %s", e)
    return networks

def main():
    """
    This function does various things
    Set the paths for input and output directories and whitelist files
    Set up logging
    Verify paths exist
    Call N-1 workers to process through the files
    """
    raw_path = "/scripts/edl-updater/raw"
    sanitized_path = "/scripts/edl-updater/sanitized"
    logs_path = "/scripts/edl-updater/logs"
    whitelist_domains_file = "/scripts/edl-updater/whitelist_domains.txt"
    whitelist_networks_file = "/scripts/edl-updater/whitelist_networks.txt"

    os.makedirs(sanitized_path, exist_ok=True)
    os.makedirs(logs_path, exist_ok=True)
    os.makedirs(raw_path, exist_ok=True)

    logging.basicConfig(filename=os.path.join(logs_path, "sanitizer.log"),
                        level=logging.ERROR,
                        format="%(asctime)s %(levelname)s %(message)s")

    whitelist_domains = load_whitelist_domains(whitelist_domains_file)
    whitelist_networks = load_whitelist_networks(whitelist_networks_file)

    num_cpus = os.cpu_count()
    max_threads = num_cpus - 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for filename in os.listdir(raw_path):
            file_path = os.path.join(raw_path, filename)
            output_file = os.path.join(sanitized_path, filename)
            executor.submit(sanitize_file, file_path, output_file, whitelist_domains, whitelist_networks)

if __name__ == "__main__":
    main()
