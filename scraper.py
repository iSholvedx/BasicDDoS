import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
proxy_sources = [
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
]

output_file = "proxies.txt"
unique_proxies = set()

def fetch_proxies(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.strip().splitlines()
            print(f"[+] Fetched {len(proxies)} proxies from {url}")
            return proxies
    except Exception as e:
        print(f"[-] Failed to fetch from {url}: {e}")
    return []

def save_proxies(proxies, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    print(f"\n[✓] Saved {len(proxies):,} unique proxies to '{filename}'")


def main():
    start = time.time()
    print("[*] Starting proxy scraping...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_proxies, proxy_sources)

    for proxy_list in results:
        for proxy in proxy_list:
            if proxy and ":" in proxy:
                unique_proxies.add(proxy.strip())

    save_proxies(list(unique_proxies), output_file)
    print(f"[✓] Done in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
