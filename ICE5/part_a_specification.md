# ICE 5.2 — Part A: Specification

**Company:** Microsoft Corporation (MSFT), CIK 0000789019

1. The script sets a `User-Agent` HTTP header of `"MIS3060 Villanova jonahkarst@gmail.com"` on a shared `requests.Session`, so every request the script makes to SEC EDGAR carries it automatically.
2. The script fetches the list of recent filings for MSFT from the EDGAR submissions API at `https://data.sec.gov/submissions/CIK0000789019.json`, filters for entries where the form type is `8-K` and the items field contains `2.02` (Results of Operations), and selects the most recent match.
3. The script builds that filing's document-folder URL from its accession number, fetches the folder's `index.json` listing, and identifies the earnings press release exhibit as the file whose name matches `ex-99` (case-insensitive) and ends in `.htm`.
4. The script downloads the press release HTML, strips it to plain text with BeautifulSoup, and searches for a dollar amount near the word "revenue", a dollar amount near "diluted earnings per share" (or "EPS"), and a dollar amount near "net income"; it also pulls up to two sentences containing "outlook", "guidance", or "expects" as a guidance excerpt.
5. The script prints the filing date, exhibit URL, a 3,000-character preview of the parsed text, and the four extracted values to the terminal, then appends one row to `02_Data/Raw/earnings_extract.csv` with columns `company`, `ticker`, `period`, `revenue`, `eps_diluted`, `net_income`, `guidance_excerpt`.
