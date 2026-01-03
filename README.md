Wildcard CNAME Detector

Author: Shahwar Shah
Version: 1.0
Language: Python 3

🧠 Description

Wildcard CNAME Detector is a professional tool designed for bug bounty researchers and security testers to:

Detect wildcard CNAMEs on domains/subdomains

Show DNS CNAME target

Follow HTTP and HTTPS redirects

Display the final landing URL (even with SSL certificate warnings)

Print only domains/subdomains with wildcard CNAME

Color-highlight redirects for clear reporting

This tool is useful for identifying potential subdomain takeover risks or analyzing DNS behavior for security assessments.

🔍 Features

Detects wildcard CNAMEs automatically

Resolves DNS to show CNAME target

Follows HTTPS first, then HTTP

Ignores SSL/TLS certificate warnings (like browser “proceed anyway”)

Shows full redirect chain

Clean colorized output

Only prints domains/subdomains with wildcard CNAME

Ctrl+C safe

⚡ Installation

Clone the repository or download the script:

git clone <repo-url>
cd wildcard-cname-detector


Install required Python modules:

pip install dnspython requests colorama


Prepare a text file with domains/subdomains, one per line.

▶️ Usage
python wildcard_cname_detector.py -l domains.txt

Optional Arguments

-s, --server → Use a custom DNS resolver (example: 8.8.8.8)

python wildcard_cname_detector.py -l domains.txt -s 8.8.8.8
