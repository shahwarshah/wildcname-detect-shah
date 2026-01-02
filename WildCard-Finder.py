#!/usr/bin/env python3

import random
import string
import dns.resolver
import argparse
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

def random_subdomain(length=8):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def resolve_cname(name, resolver, record):
    try:
        answers = resolver.resolve(name, record)
        return [str(r.target) if hasattr(r, 'target') else str(r) for r in answers]
    except Exception as e:
        return []

def test_wildcard(domain, tries, record, server):
    resolver = dns.resolver.Resolver()
    if server:
        resolver.nameservers = [server]

    results = {}
    console.print(f"\n[bold blue]Testing domain:[/bold blue] {domain}\n")
    for i in range(tries):
        sub = f"{random_subdomain()}.{domain}"
        cname = resolve_cname(sub, resolver, record)

        key = tuple(cname) if cname else ("<no record>",)
        results.setdefault(key, []).append(sub)

        console.print(f"[yellow]{sub}[/yellow] → [green]{', '.join(cname) if cname else '<no record>'}[/green]")

    return results

def main():
    parser = argparse.ArgumentParser(
        prog="WildCNAME",
        description="Wildcard CNAME checker by shahwarshah"
    )
    parser.add_argument("domain", help="Target domain")
    parser.add_argument("-t", "--tries", type=int, default=10, help="Random tests count")
    parser.add_argument("-r", "--record", default="CNAME", help="DNS record to test (default: CNAME)")
    parser.add_argument("-s", "--server", help="Custom DNS server (optional)")
    args = parser.parse_args()

    results = test_wildcard(args.domain, args.tries, args.record, args.server)

    table = Table(title="Summary")
    table.add_column("Resolved Value", style="cyan")
    table.add_column("Subdomains Found", style="magenta")

    for key, subs in results.items():
        table.add_row(", ".join(key), str(len(subs)))

    console.print("\n")
    console.print(table)
    console.print("\n[bold green]Done. Follow up with manual analysis if you see repeated CNAME targets.[/bold green]")

if __name__ == "__main__":
    main()
