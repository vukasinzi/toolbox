import socket
import time
import urllib.request
from urllib.error import HTTPError, URLError

from tools.network.network_result import NetworkResult, show_results




def dns_lookup(hostname):
    try:
        return NetworkResult("DNS lookup", socket.gethostbyname(hostname))
    except socket.gaierror:
        return NetworkResult("DNS lookup", "Host not found", success=False)


def check_url(hostname):
    url = "https://" + hostname
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return NetworkResult("URL status", f"{response.getcode()} {response.reason}")
    except HTTPError as e:
        return NetworkResult("URL status", f"{e.code} {e.reason}", success=False)
    except URLError:
        return NetworkResult("URL status", "Unreachable", success=False)


def ping(hostname):
    attempts = 4
    times = []

    for _ in range(attempts):
        start = time.perf_counter()
        try:
            with socket.create_connection((hostname, 80), timeout=2):
                pass
        except OSError:
            continue
        times.append((time.perf_counter() - start) * 1000)

    if not times:
        return NetworkResult("Ping", "Host unreachable", success=False)

    average = sum(times) / len(times)
    summary = f"min {min(times):.0f} / avg {average:.0f} / max {max(times):.0f} ms ({len(times)}/{attempts})"
    return NetworkResult("Ping", summary, success=len(times) == attempts)


sources = {
    "DNS": dns_lookup,
    "URL status": check_url,
    "Ping": ping,
}


def run():
    host = input("Enter host > ")

    results = []
    for get_result in sources.values():
        results.append(get_result(host))

    show_results(host, results)



