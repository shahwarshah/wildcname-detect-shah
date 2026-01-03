#!/usr/bin/env python3

import argparse
import dns.resolver
import signal
import sys
import requests
from urllib.parse import urlparse
from colorama import Fore, Style, init
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Init
init(autoreset=True)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# -------------------------
# Ctrl+C handler
# -------------------------
def handle_exit(sig, frame):
    print(Fore.RED + "\n[!] Scan interrupted. Exiting cleanly.\n")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# -------------------------
# Banner
# -------------------------
def banner():
    print(Fore.CYAN + r"""
 __        ___ _     _      _                _   ____ _   _    _    __  __ _____
 \ \      / (_) | __| | ___| |__   ___  ___ | | / ___| \ | |  / \  |  \/  | ____|
  \ \ /\ / /| | |/ _` |/ __| '_ \ / _ \/ _ \| | | |   |  \| | / _ \ | |\/| |  _|
   \ V  V / | | | (_| | (__| | | |  __/ (_) | | | |___| |\  |/ ___ \| |  | | |___
    \_/\_/  |_|_|\__,_|\___|_| |_|\___|\___/|_|  \____|_| \_/_/   \_\_|  |_|_____|

        Wildcard CNAME Detector
        DNS Wildcard Analysis
        Author: shahwarshah
""" + Style.RESET_ALL)

# -------------------------
# Normalize URL
# -------------------------
def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme
    host = parsed.hostname
    path = parsed.path or ""
    return f"{scheme}://{host}{path}"

# -------------------------
# Get final redirect
# -------------------------
def get_final_redirect(domain):
    urls = [f"https://{domain}", f"http://{domain}"]

    for url in urls:
        try:
            r = requests.get(
                url,
                allow_redirects=True,
                timeout=6,
                verify=False
            )

            final_url = normalize_url(r.url)

            if domain in final_url:
                return "no external redirect"

            return final_url

        except requests.exceptions.RequestException:
            continue

    return "HTTP request failed"

# -------------------------
# Resolve CNAME
# -------------------------
def get_cname(domain, resolver):
    try:
        answers = resolver.resolve(domain, "CNAME")
        return str(answers[0].target).rstrip(".")
    except:
        return None

# -------------------------
# Detect wildcard
# -------------------------
def has_wildcard_cname(domain, resolver):
    targets = set()

    for i in range(3):
        test_sub = f"test{i}.{domain}"
        cname = get_cname(test_sub, resolver)
        if cname:
            targets.add(cname)

    if len(targets) == 1:
        return targets.pop()

    return None

# -------------------------
# Scan domains
# -------------------------
def scan(file_path, resolver):
    with open(file_path, "r") as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue

            cname_target = has_wildcard_cname(domain, resolver)
            if cname_target:
                redirect = get_final_redirect(domain)

                print(Fore.GREEN + f"[+] Wildcard CNAME: {domain}")
                print(Fore.GREEN + f"    ├─ CNAME Target : {cname_target}")
                print(Fore.YELLOW + f"    └─ Redirects   : {redirect}\n")

# -------------------------
# Main
# -------------------------
def main():
    banner()

    parser = argparse.ArgumentParser(
        description="Wildcard CNAME Detector by shahwarshah"
    )
    parser.add_argument(
        "-l", "--list",
        required=True,
        help="File containing domains/subdomains"
    )
    parser.add_argument(
        "-s", "--server",
        help="Custom DNS server (example: 8.8.8.8)"
    )

    args = parser.parse_args()

    resolver = dns.resolver.Resolver()
    if args.server:
        resolver.nameservers = [args.server]

    scan(args.list, resolver)

if __name__ == "__main__":
    main()
