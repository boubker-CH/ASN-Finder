# ASN-Finder
Python CLI tool to scrape ASN, prefix, and network data for any company from bgp.he.net (Hurricane Electric BGP Toolkit).

# BGP HE Scraper

A lightweight Python CLI tool to scrape ASN, prefix, and network information for any company from [bgp.he.net](https://bgp.he.net).

---

## Features

-  Search **any company** by name via CLI argument or interactive prompt
-  Exports results to both **JSON** and **TXT** files named after the queried company
-  Optional flags to skip JSON or TXT output
-  Graceful error handling for HTTP failures and missing results

---

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## Usage

### Basic — interactive prompt

```bash
python bgp_scraper.py
```

You will be prompted:

```
Enter company name to search: cloudflare
```

---

### CLI argument

```bash
python bgp_scraper.py -c amazon
python bgp_scraper.py --company "amazon"
```

---

### Skip output files

```bash
# Skip JSON output
python bgp_scraper.py -c microsoft --no-json

# Skip TXT output
python bgp_scraper.py -c google --no-txt

# Skip both (print only)
python bgp_scraper.py -c apple --no-json --no-txt
```

---

## Output

Results are saved as:

| File | Name pattern |
|------|-------------|
| JSON | `bgp_<company>_results.json` |
| TXT  | `bgp_<company>_results.txt`  |

### JSON example (`bgp_cloudflare_results.json`)

```json
[
    {
        "result": "AS13***",
        "type": "ASN",
        "description": "CLOUDFLARENET - Cloudflare, Inc."
    },
    ...
]
```

### TXT example (`bgp_cloudflare_results.txt`)

```
AS13335 | ASN | CLOUDFLARENET - Cloudflare, Inc.
104.16.0.0/12 | Prefix | CLOUDFLARENET - Cloudflare, Inc.
...
```

---

## Project Structure

```
.
├── bgp_scraper.py          # Main script
├── README.md               # This file
└── bgp_<company>_results.* # Generated output files (gitignored)
```

> **Tip:** Add `bgp_*_results.*` to your `.gitignore` to avoid committing output files.

---

## Disclaimer

This tool is intended for legitimate network research and reconnaissance purposes only. Respect [bgp.he.net](https://bgp.he.net)'s terms of service and avoid excessive automated requests.
