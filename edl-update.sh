#!/bin/bash

# Execute the first python script
/bin/python3 /scripts/edl-updater/edl-downloader2.py

# Execute the second python script
/bin/python3 /scripts/edl-updater/edl-sanitizer.py

# Execute the third python script
/bin/python3 /scripts/edl-updater/edl-ip-handler2.py

# Execute the fourth python script
/bin/python3 /scripts/edl-updater/edl-domain-handler2.py