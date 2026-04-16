import requests
from bs4 import BeautifulSoup
import json
import argparse
import sys

BASE_URL = "https://bgp.he.net/search?search%5Bsearch%5D={query}&commit=Search"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def scrape(company: str):
    url = BASE_URL.format(query=requests.utils.quote(company))
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[-] Failed to fetch data. HTTP {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    table = soup.find("table")
    if not table:
        print(f"[-] No results found for '{company}'.")
        return results

    rows = table.find_all("tr")[1:]  # skip header

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            results.append({
                "result": cols[0].text.strip(),
                "type": cols[1].text.strip(),
                "description": cols[2].text.strip()
            })

    return results


def save_json(data, company: str):
    filename = f"bgp_{company.replace(' ', '_')}_results.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] JSON saved to {filename}")


def save_txt(data, company: str):
    filename = f"bgp_{company.replace(' ', '_')}_results.txt"
    with open(filename, "w") as f:
        for item in data:
            f.write(f"{item['result']} | {item['type']} | {item['description']}\n")
    print(f"[+] TXT  saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="BGP.he.net scraper — look up ASN / prefix info for any company."
    )
    parser.add_argument(
        "-c", "--company",
        type=str,
        default=None,
        help="Company / organisation name to search for (e.g. 'google', 'cloudflare')."
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Skip saving the JSON output file."
    )
    parser.add_argument(
        "--no-txt",
        action="store_true",
        help="Skip saving the TXT output file."
    )

    args = parser.parse_args()

    # Interactive prompt if no company supplied
    if args.company:
        company = args.company.strip()
    else:
        company = input("Enter company name to search: ").strip()

    if not company:
        print("[-] No company name provided. Exiting.")
        sys.exit(1)

    print(f"[*] Searching BGP.he.net for: {company}")
    data = scrape(company)

    if not data:
        print("[-] No entries to save.")
        sys.exit(0)

    print(f"[+] Scraped {len(data)} entries successfully!")

    if not args.no_json:
        save_json(data, company)
    if not args.no_txt:
        save_txt(data, company)


if __name__ == "__main__":
    main()
