<div align="center">
🔎 WILDCARD CNAME DETECTOR
Professional Wildcard DNS Analysis Tool for Bug Bounty & Security Research

Author: Shahwar Shah
Category: DNS Reconnaissance · Subdomain Takeover Analysis
Language: Python 3

</div>
📌 What This Tool Does

Wildcard CNAME Detector is a purpose‑built reconnaissance tool designed to identify wildcard CNAME configurations across large domain and subdomain lists.
It focuses on signal over noise by printing only confirmed wildcard CNAME hosts, along with:

The resolved CNAME target
The actual HTTP/HTTPS landing destination
Clean, color‑coded output suitable for reports

This makes it ideal for:

Subdomain takeover reconnaissance
DNS misconfiguration analysis
Bug bounty triage and validation

🧠 How It Works (High‑Level)

Takes a list of domains or subdomains
Tests controlled random subdomains per entry
Confirms wildcard behavior at the DNS CNAME level
Resolves the actual CNAME target
Performs HTTP + HTTPS requests
Follows redirects while ignoring SSL certificate errors
Prints only real wildcard CNAME hosts
No false positives. No spam output.

✨ Core Features

✔ Accurate wildcard CNAME detection
✔ DNS‑level CNAME target resolution
✔ HTTP and HTTPS redirect tracing
✔ SSL/TLS errors safely ignored
✔ Full redirect chain support
✔ Color‑coded output for clarity
✔ Graceful Ctrl+C termination
✔ Designed for large input lists
✔ Bug‑bounty‑ready output

📦 Installation
Requirements

Python 3.8+
pip

Install dependencies
pip install dnspython requests colorama

🚀 Usage
Basic scan
python wildcard_cname_detector.py -l domains.txt

Use a custom DNS resolver
python wildcard_cname_detector.py -l domains.txt -s 8.8.8.8




Legend

🟢 Domain + CNAME detection
🟡 Redirect destination
❌ Non‑wildcard domains are never printed

⚠️ Important Notes

This tool does not claim exploitability
A wildcard CNAME does not automatically mean takeover

Always verify:

Service ownership
Account control
Platform status

Designed for recon and validation, not exploitation

🧑‍💻 Author

Shahwar Shah
Security Researcher · Bug Bounty Hunter

GitHub: https://github.com/shahwarshah

LinkedIn: https://www.linkedin.com/in/syed-shahwar-ahmad-51531a319
