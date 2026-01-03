🟢 Wildcard CNAME Detector

Author: Shahwar Shah
Version: 1.0
Language: Python 3

🧠 Overview

Wildcard CNAME Detector is a professional tool for security researchers and bug bounty hunters to identify wildcard CNAME records in domains and subdomains.

It resolves DNS CNAMEs, follows HTTP/HTTPS redirects (ignoring SSL errors), and clearly reports which domains are configured with wildcard CNAMEs, helping uncover potential subdomain takeover risks.

Only domains with wildcard CNAMEs are displayed, keeping output concise and professional.

🔍 Key Features

✅ Detect wildcard CNAME records reliably

✅ Resolve DNS CNAME targets

✅ Follow HTTPS & HTTP redirects automatically

✅ Handle SSL/TLS certificate errors

✅ Show final landing URL(s) with color-coded output

✅ Ctrl+C safe for graceful termination

✅ Only prints domains/subdomains with wildcard CNAMEs

✅ Designed for bug bounty and penetration testing reports

⚡ Installation

Clone the repository or download the script:

git clone <repo-url>
cd wildcard-cname-detector


Install dependencies:

pip install dnspython requests colorama


Prepare a text file with domains/subdomains, one per line.

▶️ Usage
python wildcard_cname_detector.py -l domains.txt

Optional Arguments

-s, --server → Specify a custom DNS resolver (example: 8.8.8.8):

python wildcard_cname_detector.py -l domains.txt -s 8.8.8.8

✅ Example Output
[+] Wildcard CNAME: event-bridge.covid19.twilio.com -> er-cell0.edge.prod.twilio.com -> https://twilio.com
[+] Wildcard CNAME: frontline.stage.twilio.com -> twilio.netlifyglobalcdn.com -> no redirect
[+] Wildcard CNAME: api.twilio.com -> er-cell0.edge.prod.twilio.com -> no redirect


Green: Domain + CNAME

Yellow: Redirect URL(s)

💡 Notes

Only domains with wildcard CNAME are displayed

SSL errors are ignored to detect redirects even on private/test certificates

Ideal for DNS misconfiguration checks and subdomain takeover reconnaissance

Compatible with large domain lists for professional bug bounty scanning

⚙️ Author

Shahwar Shah
Cybersecurity researcher & bug bounty hunter
