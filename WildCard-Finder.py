#!/usr/bin/env python3

import argparse
import random
import string
import dns.resolver
from colorama import Fore, Style, init

init(autoreset=True)

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

        Wildcard CNAME Detection Tool
        DNS Pattern & Subdomain Resolution Analysis
        Author: shahwarshah
""" + Style.RESET_ALL)


# -------------------------
# Helpers
# -------------------------
def random_subdomain(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def resolve_cname(domain, resolver):
    try:
        answers = resolver.resolve(domain, "CNAME")
        return str(answers[0].target).rstrip(".")
    except Exception:
        return None


# -------------------------
# Random Wildcard Scan
# -------------------------
def scan_random(domain, attempts, resolver):
    print(Fore.BLUE + f"\n[+] Random wildcard scan on: {domain}\n")

    results = {}

    for _ in range(attempts):
        sub = f"{random_subdomain()}.{domain}"
        cname = resolve_cname(sub, resolver)

        key = cname if cname else "NO_CNAME"
        results.setdefault(key, []).append(sub)

        if cname:
            print(Fore.YELLOW + sub + Fore.GREEN + f"  →  {cname}")
        else:
            print(Fore.YELLOW + sub + Fore.RED + "  →  NO CNAME")

    return results


# -------------------------
# Subdomain List Scan
# -------------------------
def scan_list(file_path, resolver):
    print(Fore.BLUE + f"\n[+] Scanning subdomain list: {file_path}\n")

    results = {}

    with open(file_path, "r") as f:
        for line in f:
            sub = line.strip()
            if not sub:
                continue

            cname = resolve_cname(sub, resolver)
            key = cname if cname else "NO_CNAME"
            results.setdefault(key, []).append(sub)

            if cname:
                print(Fore.YELLOW + sub + Fore.GREEN + f"  →  {cname}")
            else:
                print(Fore.YELLOW + sub + Fore.RED + "  →  NO CNAME")

    return results


# -------------------------
# Analysis & Summary
# -------------------------
def analyze(results):
    print(Fore.CYAN + "\n--- Scan Summary ---\n")

    wildcard_detected = False

    for cname, subs in results.items():
        print(Fore.WHITE + f"{cname}  ->  {len(subs)} subdomains")

        if cname != "NO_CNAME" and len(subs) >= 3:
            wildcard_detected = True
            print(
                Fore.RED
                + f"[!] Possible Wildcard CNAME detected: {cname}"
            )

    if wildcard_detected:
        print(
            Fore.RED
            + "\n[!] Wildcard CNAME behavior is very likely.\n"
        )
    else:
        print(
            Fore.GREEN
            + "\n[+] No clear wildcard CNAME behavior detected.\n"
        )


# -------------------------
# Main
# -------------------------
def main():
    banner()

    parser = argparse.ArgumentParser(
        description="Wildcard CNAME detection tool by shahwarshah"
    )

    parser.add_argument(
        "-d", "--domain",
        help="Base domain for random wildcard testing"
    )
    parser.add_argument(
        "-l", "--list",
        help="File containing subdomains to scan"
    )
    parser.add_argument(
        "-t", "--tries",
        type=int,
        default=15,
        help="Number of random subdomains to test"
    )
    parser.add_argument(
        "-s", "--server",
        help="Custom DNS server (example: 8.8.8.8)"
    )

    args = parser.parse_args()

    if not args.domain and not args.list:
        print(Fore.RED + "[-] You must provide --domain or --list")
        return

    resolver = dns.resolver.Resolver()
    if args.server:
        resolver.nameservers = [args.server]

    results = {}

    if args.domain:
        results = scan_random(args.domain, args.tries, resolver)

    if args.list:
        results = scan_list(args.list, resolver)

    analyze(results)


if __name__ == "__main__":
    main()
