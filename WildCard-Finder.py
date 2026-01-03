#!/usr/bin/env python3

import argparse
import dns.resolver
import signal
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# -------------------------
# Graceful Ctrl+C
# -------------------------
def handle_exit(sig, frame):
    print(Fore.RED + "\n[!] Scan interrupted by user. Exiting cleanly.\n")
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
        Author: shahwarshah
""" + Style.RESET_ALL)

# -------------------------
# Resolve CNAME
# -------------------------
def get_cname_target(domain, resolver):
    try:
        answers = resolver.resolve(domain, 'CNAME')
        return str(answers[0].target).rstrip('.')
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.exception.DNSException:
        return None

# -------------------------
# Detect wildcard CNAME
# -------------------------
def check_wildcard(domain, resolver, test_count=3):
    hits = set()
    for i in range(test_count):
        test_sub = f"test{i}.{domain}"
        target = get_cname_target(test_sub, resolver)
        if target:
            hits.add(target)
    if len(hits) == 1:
        return hits.pop()
    return None

# -------------------------
# Get HTTP/HTTPS redirects
# -------------------------
def get_redirect(domain):
    urls = [f"https://{domain}", f"http://{domain}"]
    for url in urls:
        try:
            r = requests.get(url, allow_redirects=True, timeout=6, verify=False)
            if r.history:
                # There was a redirect chain
                return " -> ".join([resp.url for resp in r.history] + [r.url])
            else:
                return r.url  # no redirect
        except requests.exceptions.RequestException:
            continue
    return "HTTP request failed"

# -------------------------
# Scan domains from file
# -------------------------
def scan_domains(file_path, resolver):
    with open(file_path, 'r') as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue

            cname_target = check_wildcard(domain, resolver)
            if cname_target:
                redirect = get_redirect(domain)
                # Green for domain + CNAME, Yellow for redirect
                print(Fore.GREEN + f"[+] Wildcard CNAME: {domain} -> {cname_target} -> " + Fore.YELLOW + f"{redirect}")

# -------------------------
# Main
# -------------------------
def main():
    banner()

    parser = argparse.ArgumentParser(description="Wildcard CNAME + HTTP/HTTPS redirect detector by shahwarshah")
    parser.add_argument("-l", "--list", help="File containing domains/subdomains to scan", required=True)
    parser.add_argument("-s", "--server", help="Custom DNS server (example: 8.8.8.8)")

    args = parser.parse_args()

    resolver = dns.resolver.Resolver()
    if args.server:
        resolver.nameservers = [args.server]

    scan_domains(args.list, resolver)

if __name__ == "__main__":
    main()
