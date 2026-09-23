"""
ice05_8k_extract.py

Finds Microsoft's (MSFT) most recent 8-K filing that reports earnings
(Item 2.02 - Results of Operations and Financial Condition), downloads the
earnings press release exhibit, and extracts revenue, diluted EPS, net
income, and a forward-looking guidance excerpt into a CSV row.

Data source: SEC EDGAR submissions API + filing archive
(https://www.sec.gov/edgar/sec-api-documentation).
"""

import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "02_Data" / "Raw"
FILING_DIR = RAW_DIR / "MSFT_8K"
CSV_PATH = RAW_DIR / "earnings_extract.csv"

COMPANY = "Microsoft Corporation"
TICKER = "MSFT"
CIK = "0000789019"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "MIS3060 Villanova jonahkarst@gmail.com",
    "Accept-Encoding": "gzip, deflate",
})

SUBMISSIONS_URL = f"https://data.sec.gov/submissions/CIK{CIK}.json"


def get_latest_earnings_8k() -> dict:
    """Query EDGAR's submissions API and return metadata for the most recent 8-K with Item 2.02."""
    resp = SESSION.get(SUBMISSIONS_URL, timeout=30)
    resp.raise_for_status()
    recent = resp.json()["filings"]["recent"]

    for i, form in enumerate(recent["form"]):
        if form == "8-K" and "2.02" in recent["items"][i]:
            return {
                "filingDate": recent["filingDate"][i],
                "reportDate": recent["reportDate"][i],
                "accessionNumber": recent["accessionNumber"][i],
                "items": recent["items"][i],
            }

    raise RuntimeError("No 8-K filing with Item 2.02 found in the most recent EDGAR submissions.")


def filing_folder_url(accession_number: str) -> str:
    acc_nodash = accession_number.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc_nodash}"


def find_press_release_exhibit(accession_number: str) -> str:
    """List the filing's documents and return the URL of the ex-99 press release exhibit."""
    folder_url = filing_folder_url(accession_number)
    resp = SESSION.get(f"{folder_url}/index.json", timeout=30)
    resp.raise_for_status()
    items = resp.json()["directory"]["item"]

    for item in items:
        name = item["name"].lower()
        if re.search(r"ex-?99", name) and name.endswith((".htm", ".html")):
            return f"{folder_url}/{item['name']}"

    raise RuntimeError(f"No ex-99 press release exhibit found in filing {accession_number}.")


def download_and_strip(doc_url: str) -> str:
    """Download the press release HTML and strip tags down to plain text."""
    resp = SESSION.get(doc_url, timeout=30)
    resp.raise_for_status()

    FILING_DIR.mkdir(parents=True, exist_ok=True)
    (FILING_DIR / doc_url.rsplit("/", 1)[-1]).write_bytes(resp.content)

    soup = BeautifulSoup(resp.content, "html.parser")
    text = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def extract_amount_near(text: str, keyword: str, window: int = 200) -> str | None:
    """Find a dollar amount within `window` characters after the first mention of `keyword`."""
    match = re.search(re.escape(keyword), text, re.IGNORECASE)
    if not match:
        return None
    snippet = text[match.end(): match.end() + window]
    amount = re.search(r"\$\s?[\d,]+\.?\d*\s?(?:billion|million)?", snippet, re.IGNORECASE)
    return amount.group(0).strip() if amount else None


def extract_eps(text: str) -> str | None:
    for keyword in ("diluted earnings per share", "diluted EPS", "EPS"):
        match = re.search(re.escape(keyword), text, re.IGNORECASE)
        if not match:
            continue
        snippet = text[match.end(): match.end() + 100]
        amount = re.search(r"\$\s?\d+\.\d+", snippet)
        if amount:
            return amount.group(0).strip()
    return None


def extract_guidance(text: str) -> str | None:
    """Return up to two sentences mentioning outlook, guidance, or expects."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    hits = [s for s in sentences if re.search(r"\boutlook\b|\bguidance\b|\bexpects\b", s, re.IGNORECASE)]
    return " ".join(hits[:2]) if hits else None


def save_csv_row(period: str, revenue: str | None, eps: str | None, net_income: str | None, guidance: str | None) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["company", "ticker", "period", "revenue", "eps_diluted", "net_income", "guidance_excerpt"])
        writer.writerow([COMPANY, TICKER, period, revenue, eps, net_income, guidance])


def main() -> None:
    print("Fetching Microsoft's filing history from SEC EDGAR...")
    filing = get_latest_earnings_8k()
    print(f"Most recent earnings 8-K: filed {filing['filingDate']} (report date {filing['reportDate']}), items: {filing['items']}")

    print("Locating press release exhibit...")
    doc_url = find_press_release_exhibit(filing["accessionNumber"])
    print(f"Press release exhibit: {doc_url}")

    print("Downloading and parsing press release...")
    text = download_and_strip(doc_url)

    print("\n--- First 3,000 characters of parsed text ---")
    print(text[:3000])
    print("--- end preview ---\n")

    revenue = extract_amount_near(text, "revenue")
    eps = extract_eps(text)
    net_income = extract_amount_near(text, "net income")
    guidance = extract_guidance(text)

    print(f"Revenue: {revenue}")
    print(f"Diluted EPS: {eps}")
    print(f"Net income: {net_income}")
    print(f"Guidance excerpt: {guidance}")

    save_csv_row(filing["reportDate"], revenue, eps, net_income, guidance)
    print(f"\nSaved row to {CSV_PATH}")


if __name__ == "__main__":
    main()
