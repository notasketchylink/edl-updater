import os
import logging
import re
import html
import string
import concurrent.futures
import ipaddress

# Compile the regular expression pattern to match non-ASCII characters
non_ascii_pattern = re.compile(r"[^\x00-\x7F]+")

# Compile a regular expression pattern to match HTML tags
html_tag_pattern = re.compile(r"<[^<]+?>")

# Compile a regular expression pattern to match comment symbols
comment_pattern = re.compile(r"[#;]")

def sanitize_line(line, non_ascii_pattern, html_tag_pattern):
    """
    This function cleans a single line from the input file.
    It removes leading and trailing whitespaces, unescapes any HTML entities, removes any HTML tags, removes any non-ASCII characters and converts the line to lowercase.
    If the line contains a comment symbol "#" or ";", everything after it is removed.
    """
    line = line.strip()
    line = html.unescape(line)
    line = re.sub(html_tag_pattern, "", line)
    line = re.sub(non_ascii_pattern, "", line)
    line = line.lower()
    line = re.sub(comment_pattern, "", line)
    return line.strip()

def sanitize_file(file_path, output_file, whitelist_domains, whitelist_networks):
    """
    This function cleans a file and writes the output to another file.
    It sanitizes each line from the input file and writes it to the output file if it doesn't contain a domain or IP address from the whitelist.
    """
    try:
        with open(file_path, "r") as input_file, open(output_file, "w") as output:
            for line in input_file:
                line = sanitize_line(line, non_ascii_pattern, html_tag_pattern)
                if not line:
                    continue
                if any(domain in line for domain in whitelist_domains):
                    continue
                try:
                    ip = ipaddress.ip_interface(line.strip())
                    if any(ip in network for network in whitelist_networks if ip.version == network.version):
                        continue
                except ValueError:
                    pass
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

    base_path = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_path, "raw")
    sanitized_path = os.path.join(base_path, "sanitized")
    logs_path = os.path.join(base_path, "logs")
    whitelist_domains_file = os.path.join(base_path, "whitelist_domains.txt")
    whitelist_networks_file = os.path.join(base_path, "whitelist_networks.txt")


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

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_threads) as executor:
        for filename in os.listdir(raw_path):
            file_path = os.path.join(raw_path, filename)
            output_file = os.path.join(sanitized_path, filename)
            executor.submit(sanitize_file, file_path, output_file, whitelist_domains, whitelist_networks)

if __name__ == "__main__":
    main()
