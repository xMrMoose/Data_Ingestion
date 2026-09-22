# In-Class Exercises — Week 5
## Data Acquisition and Ingestion
### MIS3060 Business Intelligence with AI | Villanova University

> **Format:** Ungraded | 25–30 minutes each | Individual
> **Tools:** Claude Cowork + VS Code terminal
> **Dataset:** Live market data via Yahoo Finance API (ICE 5.1)

---

## ICE 5.1 — Live Stock Chart with Vibe Coding (Monday)

### Background

Data does not only come from CSV files. One of the most common real-world ingestion tasks is pulling structured data from a web API — a server that returns data on demand. This exercise uses Yahoo Finance's free API to fetch one year of daily stock prices, then generates an interactive HTML chart in a single Vibe Coding cycle.

The workflow is the same as always: you write the specification, Claude Cowork writes the Python, you run it and validate. The difference is that the data source is live — every time you run the script, it fetches current market data.

> *Knowing how to pull data from an API with a single prompt is a genuine professional skill. By the end of this exercise you will have done it.*

### Pre-Flight Check

Confirm the following before starting:

- [ ] VS Code is open and you are in your course repository folder
- [ ] Your laptop is connected to WiFi (the script makes live requests to Yahoo Finance)
- [ ] You can open a browser on your laptop

**Tickers used in this exercise:** AAPL, MSFT, NVDA, JPM, WMT, AMZN

---

### Part A — Write Your Specification (5 min)

Before opening Claude Cowork, write a specification for your stock chart script. This is your instruction to Claude. The specification should describe a Python script that does the following — write it in your own words as complete sentences:

1. Checks whether the `yfinance` package is installed and installs it if not
2. Downloads 1 year of daily closing prices for these six tickers: AAPL, MSFT, NVDA, JPM, WMT, AMZN
3. For each ticker, prints the ticker name, earliest date, latest date, and most recent closing price to the terminal
4. Generates a self-contained HTML file called `stock_chart.html` in the current directory. The HTML file must:
   - Embed all price data directly in the file (no separate data file)
   - Use Chart.js (loaded from CDN) to draw a line chart
   - Include a dropdown menu listing all six tickers
   - Show the selected ticker's daily closing price as a line chart, with dates on the x-axis and price in USD on the y-axis
   - Update the chart automatically when the user changes the dropdown selection
   - Set the chart title to "[Ticker] — 1-Year Daily Closing Price"
5. Prints a confirmation message when `stock_chart.html` is saved

---

### Part B — Generate the Script with Claude Cowork (8 min)

Open Claude Cowork. Send your specification as your prompt. Copy the generated script into VS Code and save it as `scripts/ice05_stock_chart.py`.

**If Claude Cowork does not include the yfinance install check**, add this follow-up prompt:

> *"Please add a step at the top of the script that checks if yfinance is installed. If it is not installed, install it automatically using subprocess before running the rest of the script."*

Do not run the script yet — read through it first. Identify:
- Which line downloads the data for each ticker
- Where the HTML file is written
- Which part of the JavaScript handles the dropdown change

Write down one line from the script that you do not fully understand. You will ask Claude about it in Part D.

---

### Part C — Run the Script and Open the Chart (5 min)

Run the script from the VS Code terminal:

```bash
python scripts/ice05_stock_chart.py
```

**Expected terminal output** (you will compare against this in Part D):

- Six lines printed, one per ticker, each showing ticker name, date range, and last closing price
- A final confirmation line: `stock_chart.html saved` (or similar)

When the script finishes, open the HTML file in your browser. In VS Code's file explorer, right-click `stock_chart.html` → **Open with Live Server** (if installed), or navigate to the file in your file explorer and double-click it.

Test the dropdown: select each of the six tickers and confirm the chart updates. All six should produce a visible price line.

---

### Part D — Validate the Output (7 min)

Apply four of the five validation methods from Week 4 to your stock chart.

**Known-Answer Check**

Open a browser tab and go to [finance.yahoo.com](https://finance.yahoo.com). Search for `AAPL`. Click on the chart and find the closing price for any specific trading day within the past year.

In your notes:
- Date you checked: ___________
- Price shown on Yahoo Finance: ___________
- Price shown in your chart on that date: ___________
- Do they match? ___________

If they do not match to within a few cents, return to Claude Cowork in a new session and ask: *"My AAPL closing prices from yfinance do not match Yahoo Finance. What could explain the discrepancy?"*

**Business-Reasonableness Check**

Answer in your notes without looking anything up first:

1. NVDA (NVIDIA) has been a major beneficiary of the AI infrastructure boom. Does your chart show NVDA's price significantly higher than it was a year ago? Is that consistent with what you know about the company?
2. JPM (JPMorgan Chase) is a large financial institution. Would you expect it to be more or less volatile than NVDA? Does the chart confirm your expectation?

**Examine the Raw Downloaded Data**

The chart shows prices visually, but you should also verify the underlying numbers directly. Open a **new** Claude Cowork session and ask it to generate a short inspection script:

> *"Write a Python script using yfinance that downloads 1 year of daily data for AAPL and prints: (1) the first 5 rows as a table, (2) the last 5 rows as a table, (3) the total row count, and (4) the minimum and maximum closing price over the period."*

Run the generated script. In your notes, record:

- Total trading days in the dataset: ___________  *(a full year has roughly 252 trading days)*
- Earliest closing price: ___________  on ___________
- Most recent closing price: ___________  on ___________
- Minimum closing price: ___________  on ___________
- Maximum closing price: ___________  on ___________

Confirm that the most recent closing price matches what your chart shows for AAPL when you hover over the rightmost point. Then confirm the minimum and maximum prices are visible as the lowest and highest points on the AAPL line in the chart.

> *The chart is a picture of the data. Examining the raw rows tells you what the picture is actually built from — and whether anything got dropped or distorted between the API response and the chart.*

**Ask Claude Cowork to Explain the Code**

Open a **new** Claude Cowork session. Paste your complete `ice05_stock_chart.py` script and ask:

> *"Walk me through this script section by section. What does each part do? What should I see in the terminal when I run it?"*

Ask Claude to explain the one line you wrote down in Part B that you did not understand. Paste Claude's explanation into your notes.

---

### Cross-Validation (bonus — if time permits)

Ask Claude Cowork to check AAPL's most recent closing price two independent ways:

- **Prompt A:** *"Write a Python one-liner using yfinance that prints AAPL's most recent daily closing price."*
- **Prompt B:** *"Write Python to download the last 5 days of AAPL data using yfinance and print the closing price from the most recent row."*

Run both. Do they agree with the price shown in your chart?

---

### Debrief Questions

Answer at least one before class discussion:

1. The Yahoo Finance API is free and requires no registration. What would you need to do differently if you were pulling market data in a professional setting, where API reliability and data licensing matter?
2. Your Python script fetches data and generates HTML in a single step. What are the advantages of this compared to downloading the data first, then building the chart separately?
3. Which of the six tickers showed the most dramatic price movement over the past year? Does that make sense given current events?

---

*Instructor note: yfinance occasionally returns adjusted closing prices rather than raw closing prices, which can cause small discrepancies against Yahoo Finance's displayed values. This is a good teaching moment about the difference between adjusted and unadjusted prices. If students see a discrepancy, prompt them to ask Claude Cowork to explain adjusted vs. unadjusted closing prices. Confirm classroom WiFi allows outbound HTTPS to `query1.finance.yahoo.com` before class.*

---

## ICE 5.2 — Extracting Unstructured Data from an Earnings Press Release (Wednesday)

### Background

Not all data arrives as a clean CSV. One of the most common unstructured data tasks in BI and finance is taking a company's earnings press release — a document written for human readers — and extracting specific financial figures into a structured row that can be loaded into a spreadsheet or database.

The SEC requires all public companies to file earnings results as an 8-K ("current report") through EDGAR, its public filing system. These filings are free, require no login, and are available the moment a company publishes results. In this exercise you will use Vibe Coding to write a Python script that navigates EDGAR, pulls an earnings press release, and extracts revenue, EPS, and net income into a CSV row.

> *The ability to pull a structured number out of a prose document is a skill that separates an analyst who can only work with pre-formatted data from one who can build their own feed.*

### Pre-Flight Check

- [ ] VS Code is open and you are in your course repository folder
- [ ] Your laptop is connected to WiFi (the script makes live requests to SEC EDGAR)
- [ ] `pip install requests beautifulsoup4` — run this in the VS Code terminal before starting

**Choose one company to work with:**

| Company | Ticker | SEC CIK | Earnings item in 8-K |
|---|---|---|---|
| Apple Inc. | AAPL | 0000320193 | Item 2.02 |
| Microsoft Corporation | MSFT | 0000789019 | Item 2.02 |
| JPMorgan Chase & Co. | JPM | 0000019617 | Item 2.02 |

Write your chosen company in your notes before starting.

---

### Part A — Write Your Specification (5 min)

Before opening Claude Cowork, write a specification in your own words describing the script's behavior. Your specification must cover the following five points — write each as a complete sentence:

1. The script must set a `User-Agent` HTTP header exactly as: `"MIS3060 Villanova youremail@villanova.edu"` — SEC EDGAR requires this on all requests or the server will reject them.
2. The script fetches the list of recent 8-K filings for your chosen company using the EDGAR submissions API at `https://data.sec.gov/submissions/CIK{cik}.json`, filters for filings where the form type is `8-K` and the items field contains `2.02` (Results of Operations), and selects the most recent one.
3. The script constructs the filing's index URL, fetches it, and identifies the earnings press release exhibit — typically the `.htm` file labeled `ex99` or `ex-99`.
4. The script downloads the press release HTML, strips the HTML tags to get plain text, and searches for these patterns: a dollar amount near the word "revenue", a dollar amount near "diluted earnings per share" or "EPS", and a dollar amount near "net income". It also extracts up to two sentences containing the word "outlook" or "guidance" or "expects".
5. The script prints all extracted values to the terminal and saves one CSV row to `data/earnings_extract.csv` with columns: `company`, `ticker`, `period`, `revenue`, `eps_diluted`, `net_income`, `guidance_excerpt`.

---

### Part B — Generate the Script with Claude Cowork (8 min)

Open Claude Cowork. Send your specification as your prompt. When Claude Cowork returns the script, read through it before copying it into VS Code. Look for:

- The line that sets the `User-Agent` header — confirm it is present on every `requests.get()` call, not just the first one. If Claude missed any request, note it.
- The regex or string-search pattern used to extract revenue. Write it in your notes.
- Where in the script the CSV file is written.

Save the script as `scripts/ice05_8k_extract.py`.

**If Claude Cowork does not include BeautifulSoup for HTML stripping**, add this follow-up:

> *"Please use BeautifulSoup to strip all HTML tags from the press release before running the regex extraction. Import bs4 and parse the downloaded HTML with BeautifulSoup before searching for the financial figures."*

---

### Part C — Run the Script and Examine the Raw Text (8 min)

Run the script:

```bash
python scripts/ice05_8k_extract.py
```

**Step 1 — Check terminal output.** The script should print:
- The company name and most recent 8-K filing date
- The URL of the press release exhibit it downloaded
- The extracted values (revenue, EPS, net income, guidance)
- A confirmation that `data/earnings_extract.csv` was saved

**Step 2 — Examine the raw press release text.** Before trusting the extracted numbers, you need to see what the script actually parsed. In a **new** Claude Cowork session, ask it to add a single inspection step:

> *"Add a step to `scripts/ice05_8k_extract.py` that prints the first 3,000 characters of the plain text (after HTML stripping) to the terminal, so I can read what the script is working with."*

Run the modified script. Read the printed text. In your notes, record:
- Is the text readable prose, or is it garbled/incomplete?
- Can you visually find the revenue figure in the raw text?
- Does the figure the regex extracted match what you read in the raw text?

This step — reading what the parser actually received before trusting what it extracted — is the unstructured-data equivalent of the benchmark table check.

---

### Part D — Validate the Extracted Data (7 min)

**Known-Answer Check**

Go to the company's investor relations page or search for "[company] [most recent quarter] earnings" in a browser. Find the officially reported revenue and diluted EPS for the quarter the 8-K covers.

In your notes:
- Quarter covered: ___________
- Revenue (official source): ___________  |  Revenue (your script): ___________  |  Match? ___________
- Diluted EPS (official): ___________  |  EPS (your script): ___________  |  Match? ___________

If a value does not match or shows `None`, open a new Claude Cowork session, paste the 3,000-character text excerpt from Part C, and ask:

> *"Here is the text of an earnings press release. What regex pattern would reliably extract the quarterly revenue figure from this text?"*

Apply the suggested pattern and rerun.

**Business-Reasonableness Check**

Answer in your notes without looking anything up:

1. Apple's quarterly revenue is typically in the range of $90–120 billion. Microsoft's is roughly $60–70 billion. JPMorgan's net revenue (net of interest expense) runs around $40–45 billion per quarter. Does your extracted figure fall in a plausible range for your chosen company?
2. Is the guidance excerpt you extracted a forward-looking statement (something about the *next* quarter or year)? Or did the regex accidentally pick up a historical comparison sentence?

---

### Cross-Validation (bonus — if time permits)

You already know how to pull financial data from Yahoo Finance using `yfinance` from ICE 5.1. Use it now as an independent second source to verify what your 8-K extraction script produced.

In a new Claude Cowork session, ask:

> *"Write a Python script using yfinance that retrieves the most recent quarterly revenue and net income for [your ticker — AAPL, MSFT, or JPM] and prints both values clearly labeled."*

Run the yfinance script. Compare its output against `data/earnings_extract.csv`:

| Metric | From 8-K press release (text parsing) | From Yahoo Finance (yfinance) | Match? |
|---|---|---|---|
| Revenue | | | |
| Net Income | | | |

If the two sources agree, your text extraction is validated by an independent structured feed. If they differ, answer in your notes: is the discrepancy a parsing error in your regex, a difference in how each source defines the metric (e.g., net revenue vs. gross revenue), or a quarter mismatch?

> *Two completely different data paths — unstructured prose and a structured financial API — arriving at the same number is the strongest validation you can do without an audit.*

---

### Debrief Questions

Answer at least one before class discussion:

1. Your regex extraction may have returned `None` for one or more fields. What does that tell you about the difference between "structured" data (a CSV column) and "semi-structured" data (a press release that follows a consistent format but is still written in prose)?
2. SEC EDGAR requires a `User-Agent` header. What happens if you omit it? Why do data providers use rate limiting and identification requirements?
3. If you were building this as a recurring data feed — running every quarter for 50 companies — what would break? List two things that could go wrong at scale.

---

*Instructor note: Extraction success varies by company and quarter. Apple's press releases are highly consistent and regex extraction usually succeeds. Microsoft's are similar. JPMorgan's format is more financial-statement-oriented and may require pattern tuning. If a student's regex returns `None`, direct them to Part D's recovery step — paste the raw text into Claude Cowork and ask for a corrected pattern. This is intentional: the failure mode is the lesson. Confirm classroom WiFi allows outbound HTTPS to `data.sec.gov` and `www.sec.gov` before class. The `beautifulsoup4` install takes ~10 seconds.*
