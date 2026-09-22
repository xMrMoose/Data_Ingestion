"""
ice05_stock_chart.py

ICE 5.1 - Live Stock Chart with Vibe Coding

Downloads one year of daily closing prices for JPM and MSFT from Yahoo
Finance (via yfinance), prints a summary for each ticker to the terminal,
and generates a self-contained HTML file (stock_chart.html) with a
Chart.js line chart. A dropdown lets the user switch between tickers.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "stock_chart.html"
CSV_PATH = REPO_ROOT / "02_Data" / "Raw" / "stock_prices.csv"

# ---------------------------------------------------------------------------
# Step 1: Make sure yfinance is installed
# ---------------------------------------------------------------------------
if importlib.util.find_spec("yfinance") is None:
    print("yfinance not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])

import yfinance as yf

# ---------------------------------------------------------------------------
# Step 2: Download 1 year of daily closing prices
# ---------------------------------------------------------------------------
TICKERS = ["JPM", "MSFT", "AAPL", "AMZN", "NVDA", "TSLA", "GOOGL", "META", "NFLX", "DIS", "HOG"]

chart_data = {}
csv_rows = []

for ticker in TICKERS:
    history = yf.Ticker(ticker).history(period="1y")

    dates = history.index.strftime("%Y-%m-%d").tolist()
    closes = [round(price, 2) for price in history["Close"].tolist()]

    chart_data[ticker] = {"dates": dates, "closes": closes}
    csv_rows.extend(
        {"ticker": ticker, "date": date, "close": close}
        for date, close in zip(dates, closes)
    )

    earliest_date = dates[0]
    latest_date = dates[-1]
    most_recent_close = closes[-1]

    print(
        f"{ticker}: {earliest_date} to {latest_date} | "
        f"most recent close: ${most_recent_close:.2f}"
    )

# ---------------------------------------------------------------------------
# Step 2b: Save the raw closing prices to CSV
# ---------------------------------------------------------------------------
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(csv_rows).to_csv(CSV_PATH, index=False)
print(f"{CSV_PATH.name} saved to {CSV_PATH}")

# ---------------------------------------------------------------------------
# Step 3: Generate the self-contained HTML chart
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stock Price Chart</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  :root {{
    color-scheme: light;
    --page:            #f9f9f7;
    --surface:         #fcfcfb;
    --ink-primary:     #0b0b0b;
    --ink-secondary:   #52514e;
    --ink-muted:       #898781;
    --gridline:        #e1e0d9;
    --baseline:        #c3c2b7;
    --border:          rgba(11,11,11,0.10);
    --good:            #006300;
    --critical:        #e34948;
    --series-jpm:       #2a78d6;
    --series-msft:      #eb6834;
    --dog-body:         #a0522d;
    --dog-body-outline:  #6b3410;
    --dog-ear:          #6b3410;
    --dog-nose:         #2b1a12;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:where(:not([data-theme="light"])) {{
      color-scheme: dark;
      --page:            #0d0d0d;
      --surface:         #1a1a19;
      --ink-primary:     #ffffff;
      --ink-secondary:   #c3c2b7;
      --ink-muted:       #898781;
      --gridline:        #2c2c2a;
      --baseline:        #383835;
      --border:          rgba(255,255,255,0.10);
      --good:            #0ca30c;
      --critical:        #e66767;
      --series-jpm:       #3987e5;
      --series-msft:      #d95926;
    }}
  }}
  :root[data-theme="dark"] {{
    color-scheme: dark;
    --page:            #0d0d0d;
    --surface:         #1a1a19;
    --ink-primary:     #ffffff;
    --ink-secondary:   #c3c2b7;
    --ink-muted:       #898781;
    --gridline:        #2c2c2a;
    --baseline:        #383835;
    --border:          rgba(255,255,255,0.10);
    --good:            #0ca30c;
    --critical:        #e66767;
    --series-jpm:       #3987e5;
    --series-msft:      #d95926;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page);
    color: var(--ink-primary);
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px 60px;
  }}

  .topbar {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 24px;
  }}

  .heading .eyebrow {{
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--ink-muted);
    margin: 0 0 4px;
  }}

  h1 {{
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .dot {{
    font-size: 1.1rem;
    line-height: 1;
    flex: none;
  }}

  .controls {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  select {{
    font: inherit;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--ink-primary);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 14px;
    cursor: pointer;
  }}

  .theme-toggle {{
    font: inherit;
    font-size: 0.85rem;
    color: var(--ink-secondary);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 12px;
    cursor: pointer;
  }}

  .stat-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }}

  .stat-tile {{
    flex: 1;
    min-width: 140px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--series-color, var(--series-jpm));
    border-radius: 10px;
    padding: 12px 16px;
  }}

  .stat-tile .label {{
    font-size: 0.75rem;
    color: var(--ink-muted);
    margin: 0 0 4px;
  }}

  .stat-tile .value {{
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--ink-primary);
    margin: 0;
  }}

  .stat-tile .value.delta.up {{ color: var(--good); }}
  .stat-tile .value.delta.down {{ color: var(--critical); }}

  .chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 20px 12px;
  }}

  .chart-container {{
    position: relative;
    height: 420px;
    width: 100%;
  }}

  .footnote {{
    font-size: 0.8rem;
    color: var(--ink-muted);
    margin-top: 14px;
  }}
</style>
</head>
<body>

<div class="topbar">
  <div class="heading">
    <p class="eyebrow">1-Year Daily Closing Price</p>
    <h1><span class="dot">🌭</span><span id="chart-title">Ticker</span></h1>
  </div>
  <div class="controls">
    <select id="ticker-select"></select>
    <button type="button" class="theme-toggle" id="theme-toggle">Dark mode</button>
  </div>
</div>

<div class="stat-row">
  <div class="stat-tile" id="stat-latest">
    <p class="label">Latest close</p>
    <p class="value" id="stat-latest-value">$0.00</p>
  </div>
  <div class="stat-tile" id="stat-change">
    <p class="label">1-Year change</p>
    <p class="value delta" id="stat-change-value">$0.00 (0.0%)</p>
  </div>
  <div class="stat-tile" id="stat-range">
    <p class="label">52-week range</p>
    <p class="value" id="stat-range-value">$0.00 &ndash; $0.00</p>
  </div>
</div>

<div class="chart-card">
  <div class="chart-container">
    <canvas id="priceChart"></canvas>
  </div>
</div>

<p class="footnote">Source: Yahoo Finance via yfinance &middot; hover the chart for daily values &middot; the whole year is one very long dog.</p>

<script>
const chartData = {chart_data_json};

const root = document.documentElement;
const select = document.getElementById("ticker-select");
const titleEl = document.getElementById("chart-title");
const themeToggle = document.getElementById("theme-toggle");
const latestValueEl = document.getElementById("stat-latest-value");
const changeValueEl = document.getElementById("stat-change-value");
const rangeValueEl = document.getElementById("stat-range-value");

const SERIES_COLOR_VAR = {{ JPM: "--series-jpm", MSFT: "--series-msft" }};

function cssVar(name) {{
  return getComputedStyle(root).getPropertyValue(name).trim();
}}

function formatUSD(value) {{
  return "$" + value.toLocaleString("en-US", {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
}}

function formatTickDate(iso) {{
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", {{ month: "short", year: "2-digit" }});
}}

function formatFullDate(iso) {{
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", {{ month: "short", day: "numeric", year: "numeric" }});
}}

Object.keys(chartData).forEach(function (ticker) {{
  const option = document.createElement("option");
  option.value = ticker;
  option.textContent = ticker;
  select.appendChild(option);
}});

function hexToRgba(hex, alpha) {{
  const h = hex.replace("#", "");
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
}}

function buildGradient(ctx, chartArea, colorVar) {{
  const color = cssVar(colorVar);
  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  gradient.addColorStop(0, hexToRgba(color, 0.18));
  gradient.addColorStop(1, hexToRgba(color, 0));
  return gradient;
}}

// vertical crosshair line tracking the hovered point
const crosshairPlugin = {{
  id: "crosshair",
  afterDatasetsDraw(chart) {{
    const active = chart.getActiveElements();
    if (!active || !active.length) return;
    const {{ ctx, chartArea }} = chart;
    const x = active[0].element.x;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x, chartArea.top);
    ctx.lineTo(x, chartArea.bottom);
    ctx.lineWidth = 1;
    ctx.strokeStyle = cssVar("--baseline");
    ctx.stroke();
    ctx.restore();
  }}
}};

// draws the price line as one very long wiener dog: a thick outlined body
// tube tracing the real path, short legs at each end, a curled (waggable)
// tail at the oldest date, and a head with ears + collar at today's close
let tailWag = 0;
const wienerDogPlugin = {{
  id: "wienerDog",
  afterDatasetsDraw(chart) {{
    const meta = chart.getDatasetMeta(0);
    const pts = meta.data;
    if (!pts || pts.length < 2) return;
    const {{ ctx }} = chart;
    const n = pts.length;
    const bodyColor = cssVar("--dog-body");
    const outlineColor = cssVar("--dog-body-outline");
    const earColor = cssVar("--dog-ear");
    const noseColor = cssVar("--dog-nose");
    const colorVar = SERIES_COLOR_VAR[currentTicker] || "--series-jpm";
    const collarColor = cssVar(colorVar);

    function tracePath() {{
      ctx.beginPath();
      ctx.moveTo(pts[0].x, pts[0].y);
      for (let i = 1; i < n; i++) ctx.lineTo(pts[i].x, pts[i].y);
    }}

    // body tube: dark outline stroked first, tan body on top (cartoon-outline effect)
    ctx.save();
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 17;
    ctx.strokeStyle = outlineColor;
    tracePath();
    ctx.stroke();
    ctx.lineWidth = 13;
    ctx.strokeStyle = bodyColor;
    tracePath();
    ctx.stroke();
    ctx.restore();

    // legs: two stubby pairs, one near the tail end, one near the head end
    function drawLegPair(anchor, outlineOnly) {{
      [-6, 6].forEach(function (dx) {{
        ctx.save();
        ctx.strokeStyle = outlineColor;
        ctx.lineWidth = 5;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(anchor.x + dx, anchor.y + 4);
        ctx.lineTo(anchor.x + dx, anchor.y + 13);
        ctx.stroke();
        ctx.strokeStyle = bodyColor;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(anchor.x + dx, anchor.y + 4);
        ctx.lineTo(anchor.x + dx, anchor.y + 13);
        ctx.stroke();
        ctx.fillStyle = outlineColor;
        ctx.beginPath();
        ctx.ellipse(anchor.x + dx, anchor.y + 14, 3, 2, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }});
    }}
    const tailLegIdx = Math.min(n - 1, Math.max(1, Math.round(n * 0.06)));
    const headLegIdx = Math.max(0, n - 1 - Math.max(1, Math.round(n * 0.06)));
    drawLegPair(pts[tailLegIdx]);
    drawLegPair(pts[headLegIdx]);

    // curled, gently wagging tail at the oldest date (start of the path)
    const tailBase = pts[0];
    const tailNext = pts[Math.min(n - 1, 3)];
    const tailDir = Math.atan2(tailBase.y - tailNext.y, tailBase.x - tailNext.x);
    const wagOffset = Math.sin(tailWag) * 0.35;
    ctx.save();
    ctx.translate(tailBase.x, tailBase.y);
    ctx.rotate(tailDir + wagOffset);
    ctx.lineCap = "round";
    ctx.strokeStyle = outlineColor;
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.quadraticCurveTo(14, -4, 14, -16);
    ctx.stroke();
    ctx.strokeStyle = bodyColor;
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.quadraticCurveTo(14, -4, 14, -16);
    ctx.stroke();
    ctx.restore();

    // head at today's close: snout, nose, eye, floppy ears, collar
    const head = pts[n - 1];
    const headPrev = pts[Math.max(0, n - 4)];
    const headDir = Math.atan2(head.y - headPrev.y, head.x - headPrev.x);
    ctx.save();
    ctx.translate(head.x, head.y);
    ctx.rotate(headDir);

    // ears (drawn first, so the head/snout sit on top)
    [-1, 1].forEach(function (side) {{
      ctx.save();
      ctx.scale(1, side);
      ctx.fillStyle = earColor;
      ctx.beginPath();
      ctx.moveTo(-4, 2);
      ctx.bezierCurveTo(-14, 6, -18, 20, -10, 24);
      ctx.bezierCurveTo(-4, 18, -2, 8, -4, 2);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }});

    // head + snout
    ctx.fillStyle = outlineColor;
    ctx.beginPath();
    ctx.ellipse(0, 0, 10.5, 8.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = bodyColor;
    ctx.beginPath();
    ctx.ellipse(0, 0, 8.5, 6.8, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = outlineColor;
    ctx.beginPath();
    ctx.ellipse(11, 1, 6.5, 4.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = bodyColor;
    ctx.beginPath();
    ctx.ellipse(11, 1, 5, 3.5, 0, 0, Math.PI * 2);
    ctx.fill();

    // nose + eye
    ctx.fillStyle = noseColor;
    ctx.beginPath();
    ctx.ellipse(16.5, 1, 2, 1.6, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(-2, -5, 1.3, 0, Math.PI * 2);
    ctx.fill();

    // collar, colored by the selected ticker
    ctx.strokeStyle = collarColor;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(-7, 0, 6, -Math.PI * 0.7, Math.PI * 0.7);
    ctx.stroke();
    ctx.fillStyle = collarColor;
    ctx.beginPath();
    ctx.arc(-7, 6, 1.6, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    // today's closing price, labeled in ink (never the series color)
    ctx.save();
    ctx.font = "600 12px system-ui, sans-serif";
    ctx.fillStyle = cssVar("--ink-primary");
    ctx.textBaseline = "middle";
    const value = chart.data.datasets[0].data[n - 1];
    const label = formatUSD(value);
    const textWidth = ctx.measureText(label).width;
    const x = Math.min(head.x + 26, chart.chartArea.right - textWidth);
    ctx.fillText(label, x, head.y - 24);
    ctx.restore();
  }}
}};

let currentTicker = null;

const ctx = document.getElementById("priceChart").getContext("2d");
let priceChart = new Chart(ctx, {{
  type: "line",
  data: {{
    labels: [],
    datasets: [{{
      data: [],
      borderColor: "transparent",
      backgroundColor: "transparent",
      borderWidth: 0,
      pointRadius: 0,
      pointHoverRadius: 0,
      tension: 0.15,
      fill: true
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    interaction: {{ mode: "index", intersect: false }},
    layout: {{ padding: {{ right: 56, top: 24 }} }},
    scales: {{
      x: {{
        grid: {{ color: cssVar("--gridline"), tickLength: 8 }},
        border: {{ color: cssVar("--baseline") }},
        ticks: {{
          color: cssVar("--ink-muted"),
          maxTicksLimit: 8,
          callback: function (value, index) {{
            const label = this.getLabelForValue(value);
            return formatTickDate(label);
          }}
        }}
      }},
      y: {{
        grid: {{ color: cssVar("--gridline") }},
        border: {{ display: false }},
        ticks: {{
          color: cssVar("--ink-muted"),
          callback: function (value) {{ return "$" + value.toLocaleString("en-US"); }}
        }}
      }}
    }},
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        backgroundColor: cssVar("--surface"),
        titleColor: cssVar("--ink-secondary"),
        bodyColor: cssVar("--ink-primary"),
        borderColor: cssVar("--border"),
        borderWidth: 1,
        padding: 10,
        cornerRadius: 8,
        displayColors: false,
        bodyFont: {{ weight: "700", size: 13 }},
        titleFont: {{ size: 11 }},
        callbacks: {{
          title: function (items) {{ return formatFullDate(items[0].label); }},
          label: function (item) {{ return formatUSD(item.parsed.y); }}
        }}
      }}
    }}
  }},
  plugins: [wienerDogPlugin, crosshairPlugin]
}});

function applyTheme(colorVar) {{
  const color = cssVar(colorVar);
  priceChart.data.datasets[0].backgroundColor = buildGradient(
    ctx, priceChart.chartArea || {{ top: 0, bottom: 400 }}, "--dog-body"
  );
  priceChart.options.scales.x.grid.color = cssVar("--gridline");
  priceChart.options.scales.x.border.color = cssVar("--baseline");
  priceChart.options.scales.x.ticks.color = cssVar("--ink-muted");
  priceChart.options.scales.y.grid.color = cssVar("--gridline");
  priceChart.options.scales.y.ticks.color = cssVar("--ink-muted");
  priceChart.options.plugins.tooltip.backgroundColor = cssVar("--surface");
  priceChart.options.plugins.tooltip.titleColor = cssVar("--ink-secondary");
  priceChart.options.plugins.tooltip.bodyColor = cssVar("--ink-primary");
  priceChart.options.plugins.tooltip.borderColor = cssVar("--border");
  document.getElementById("stat-latest").style.setProperty("--series-color", color);
  document.getElementById("stat-change").style.setProperty("--series-color", color);
  document.getElementById("stat-range").style.setProperty("--series-color", color);
}}

function updateChart(ticker) {{
  const data = chartData[ticker];
  const colorVar = SERIES_COLOR_VAR[ticker] || "--series-jpm";
  currentTicker = ticker;

  priceChart.data.labels = data.dates;
  priceChart.data.datasets[0].data = data.closes;
  applyTheme(colorVar);
  priceChart.update();

  titleEl.textContent = ticker + " — 1-Year Daily Closing Price";

  const first = data.closes[0];
  const last = data.closes[data.closes.length - 1];
  const change = last - first;
  const pct = (change / first) * 100;
  const min = Math.min(...data.closes);
  const max = Math.max(...data.closes);

  latestValueEl.textContent = formatUSD(last);
  changeValueEl.textContent = (change >= 0 ? "+" : "") + formatUSD(change) + " (" + (pct >= 0 ? "+" : "") + pct.toFixed(1) + "%)";
  changeValueEl.classList.toggle("up", change >= 0);
  changeValueEl.classList.toggle("down", change < 0);
  rangeValueEl.textContent = formatUSD(min) + " – " + formatUSD(max);
}}

select.addEventListener("change", function () {{
  updateChart(this.value);
}});

let isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
function syncThemeButtonLabel() {{
  themeToggle.textContent = isDark ? "Light mode" : "Dark mode";
}}
themeToggle.addEventListener("click", function () {{
  isDark = !isDark;
  root.setAttribute("data-theme", isDark ? "dark" : "light");
  syncThemeButtonLabel();
  updateChart(select.value);
}});
syncThemeButtonLabel();

// Initialize with the first ticker
updateChart(select.value);

// gentle tail-wag animation, throttled to ~24fps
let lastFrameTime = 0;
function animateTailWag(timestamp) {{
  if (timestamp - lastFrameTime > 40) {{
    tailWag += 0.12;
    priceChart.draw();
    lastFrameTime = timestamp;
  }}
  requestAnimationFrame(animateTailWag);
}}
requestAnimationFrame(animateTailWag);
</script>

</body>
</html>
"""

html_output = HTML_TEMPLATE.format(chart_data_json=json.dumps(chart_data))

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"{OUTPUT_PATH.name} saved to {OUTPUT_PATH}")
