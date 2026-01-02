# WildCNAME

A professional wildcard CNAME discovery tool written in Python.

Created by: **shahwarshah**

This tool helps you detect whether a domain uses wildcard DNS/CNAME, by generating
random subdomains and resolving their DNS records.

---

## What it Does

WildCNAME will:

1. Generate random subdomain names.
2. Resolve them against the target DNS.
3. Print colorful results showing whether CNAME records are returned.
4. Summarize repeated patterns that may indicate wildcard DNS.

---

## Requirements

Install dependencies:

pip install dnspython rich

---

## Usage

./wildcname.py example.com

Options:

- `-t`, `--tries`: Number of random subdomains to test (default 10)
- `-r`, `--record`: DNS record type (default CNAME)
- `-s`, `--server`: Custom DNS server to query

Example:

./wildcname.py frontline.stage.twilio.com -t 25 -s 8.8.8.8

---

## Output

WildCNAME prints:

- Each random subdomain and its resolved value
- A summary table showing all unique responses
- This helps you see if the same target repeats (wildcard DNS)

---

## Notes

- Repeated CNAMEs for different random subdomains usually indicate a wildcard.
- If you see no records for most random names, wildcard may not be in place.
- Always verify with authoritative DNS records too.

---

## Author

**shahwarshah**
