#!/usr/bin/env python3
import argparse
import dns.resolver
import requests
import random
import string
import sys
import signal
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = r"""
 __        ___ _     _      _                _   ____ _   _    _    __  __ _____
 \ \      / (_) | __| | ___| |__   ___  ___ | | / ___| \ | |  / \  |  \/  | ____|
  \ \ /\ / /| | |/ _` |/ __| '_ \ / _ \/ _ \| | | |   |  \| | / _ \ | |\/| |  _|
   \ V  V / | | | (_| | (__| | | |  __/ (_) | | | |___| |\  |/ ___ \| |  | | |___
    \_/\_/  |_|_|\__,_|\___|_| |_|\___|\___/|_|  \____|_| \_/_/   \_\_|  |_|_____|

        Wildcard CNAME Detector
        DNS Wildcard Analysis
        Author: shahwarshah
"""

def ctrl_c_handler(sig, frame):
    print(f"\n{Fore.YELLOW}[!] Scan interrupted by user. Exiting cleanly.")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

def random_sub():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

def resolve_cname(domain, resolver):
    try:
        answers = resolver.resolve(domain, "CNAME")
        for rdata in answers:
            return str(rdata.target).rstrip(".")
    except:
        return None

def get_final_redirect(url):
    try:
        r = requests.get(url, timeout=8, allow_redirects=True, verify=False)
        final = r.url

        parsed = urlparse(final)
        clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # remove :443 noise
        clean = clean.replace(":443", "")
        return clean
    except:
        return None

def scan(file_path, resolver):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File not found: {file_path}")
        print(f"{Fore.YELLOW}[*] Please check the path and try again.")
        sys.exit(1)

    for domain in domains:
        wildcard = f"{random_sub()}.{domain}"

        base_cname = resolve_cname(domain, resolver)
        wildcard_cname = resolve_cname(wildcard, resolver)

        if base_cname and wildcard_cname and base_cname == wildcard_cname:
            print(f"{Fore.GREEN}[+] Wildcard CNAME: {domain} -> {base_cname}")

            redirect = get_final_redirect(f"https://{domain}")
            if redirect:
                print(f"    {Fore.CYAN}Redirects to:{Style.BRIGHT} {Fore.MAGENTA}{redirect}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", required=True, help="File containing domains")
    args = parser.parse_args()

    print(BANNER)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

    scan(args.list, resolver)

if __name__ == "__main__":
    main()
