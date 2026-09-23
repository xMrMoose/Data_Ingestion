# ICE 5.2 — Part D: Validate the Extracted Data

## Known-Answer Check

Source: Microsoft Investor Relations, FY26 Q4 press release (microsoft.com/en-us/investor/earnings/fy-2026-q4).

- **Quarter covered:** Q4 FY2026 — three months ended June 30, 2026
- **Revenue (official source):** $90.0 billion | **Revenue (script):** $90.0 billion | **Match?** Yes
- **Diluted EPS (official):** $4.81 (GAAP) | **EPS (script):** $4.81 | **Match?** Yes

Net income also matches: $35.8 billion (GAAP) both from the official release and the script.

## Business-Reasonableness Check

1. **Is the figure plausible?** The ICE handout's reference range for Microsoft ("roughly $60-70 billion" per quarter) is out of date — that range reflects Microsoft's revenue a couple of years ago. At $90.0 billion for the quarter, this is a genuine, large company continuing double-digit revenue growth (18% YoY per the release, driven by Microsoft Cloud reaching $59.3 billion, up 27% YoY), not an extraction error. The lesson: a "plausibility range" is only as good as when it was written — always sanity-check the range itself against how much time has passed, not just the number against the range.

2. **Is the guidance excerpt actually forward-looking?** No — the regex picked up a **historical comparison**, not real guidance. The extracted excerpt is one long run-on block containing GAAP/non-GAAP reconciliation figures and a comparison against guidance issued back on April 29, 2026 ("...compared to our forward-looking guidance provided on April 29, 2026, resulting in a benefit of $0.27..."). It is not a statement about what Microsoft expects *next* quarter. The failure has a specific, traceable cause: the press release separates clauses with `•` bullet characters instead of periods, so the sentence-splitting regex (which only breaks on `.`, `!`, `?`) never found a sentence boundary until much later in the paragraph — merging several unrelated bullet points into one giant "sentence."

## Takeaway

The core financial extraction (revenue, EPS, net income) is accurate and validated against an independent source. The guidance-excerpt extraction is not reliable as written — it needs sentence-splitting logic that also treats `•` (and likely other list markers) as a boundary, or a more targeted search that looks specifically for phrases like "guidance for" or "expects revenue of" rather than any sentence containing "guidance"/"outlook"/"expects".
