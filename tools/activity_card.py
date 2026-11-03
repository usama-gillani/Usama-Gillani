"""Builds a neon 'git log'-style SVG of recent public GitHub activity.

Usage: GITHUB_TOKEN=... python3 activity_card.py <username> <out.svg>
Stdlib only.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from html import escape

USER, OUT = sys.argv[1], sys.argv[2]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
MAX_ROWS = 6
PINK, CYAN, PURPLE, GREEN, TEXT, DIM, YELLOW = "#ff2bd6", "#00f0ff", "#7b2ff7", "#39ff88", "#e6dcff", "#7b6bb5", "#ffd319"


def fetch(url):
    h = {"User-Agent": "neon-activity-card", "Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return json.load(r)


def ago(ts):
    t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    s = (dt.datetime.now(dt.timezone.utc) - t).total_seconds()
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if s >= n:
            return f"{int(s // n)}{unit} ago"
    return "just now"


def describe(e):
    """-> (icon, verb, repo, color) or None to skip."""
    p, repo = e.get("payload", {}), e["repo"]["name"]
    t = e["type"]
    if t == "PushEvent":
        n = p.get("size") or len(p.get("commits") or []) or None
        return "⬆", f"pushed {n} commit{'s' if n != 1 else ''} to" if n else "pushed to", repo, CYAN
    if t == "CreateEvent":
        if p.get("ref_type") != "repository":  # branches/tags are noise
            return None
        return "✨", "created repo", repo, GREEN
    if t == "PublicEvent":
        return "🔓", "open-sourced", repo, GREEN
    if t == "WatchEvent":
        return "⭐", "starred", repo, YELLOW
    if t == "ForkEvent":
        return "🍴", "forked", repo, PURPLE
    if t == "PullRequestEvent":
        return "🔀", f"{p.get('action', 'opened')} PR in", repo, PINK
    if t == "IssuesEvent":
        return "🐛", f"{p.get('action', 'opened')} issue in", repo, PINK
    if t == "ReleaseEvent":
        return "🚀", "released", repo, GREEN
    return None


rows, seen = [], set()
try:
    events = fetch(f"https://api.github.com/users/{USER}/events/public?per_page=50")
except Exception as exc:  # never fail the workflow over the feed
    print("events fetch failed:", exc)
    events = []
events.sort(key=lambda e: e["created_at"], reverse=True)
for e in events:
    d = describe(e)
    if not d:
        continue
    key = (d[1], d[2])
    if key in seen:  # collapse repeated identical actions
        continue
    seen.add(key)
    rows.append((*d, ago(e["created_at"])))
    if len(rows) == MAX_ROWS:
        break

W = 1000
H = 110 + max(len(rows), 1) * 34
o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  "font-family=\"'Fira Code','JetBrains Mono',Consolas,monospace\">")
a(f"""<defs>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{PURPLE}"><animate attributeName="stop-color" values="{PURPLE};{PINK};{CYAN};{PURPLE}" dur="6s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{PURPLE};{PINK};{CYAN}" dur="6s" repeatCount="indefinite"/></stop>
 </linearGradient>
 <filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <style>.r{{opacity:0;animation:f .45s ease forwards}}@keyframes f{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
</defs>""")
a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="#0b0221" stroke="url(#bd)" stroke-width="2"/>')
a(f'<text x="30" y="42" font-size="16" fill="{PINK}" filter="url(#gl)">❯ <tspan fill="{CYAN}">git log</tspan> '
  f'<tspan fill="{DIM}">--author=@{escape(USER)} --live</tspan></text>')
# live dot
a(f'<circle cx="{W-110}" cy="37" r="5" fill="{GREEN}" filter="url(#gl)"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
a(f'<text x="{W-98}" y="42" font-size="13" fill="{GREEN}">LIVE</text>')
a(f'<line x1="30" y1="60" x2="{W-30}" y2="60" stroke="#2a1158"/>')

if not rows:
    a(f'<text x="30" y="100" font-size="15" fill="{DIM}">no public activity yet — cooking something in private 🍳</text>')
for i, (icon, verb, repo, col, when) in enumerate(rows):
    y = 96 + i * 34
    a(f'<g class="r" style="animation-delay:{0.12 * i + 0.2:.2f}s">'
      f'<circle cx="38" cy="{y-5}" r="4" fill="{col}" filter="url(#gl)"/>'
      + (f'<line x1="38" y1="{y+1}" x2="38" y2="{y+25}" stroke="#2a1158" stroke-width="2"/>' if i < len(rows) - 1 else "")
      + f'<text x="56" y="{y}" font-size="15" fill="{TEXT}">{icon}  {escape(verb)} '
      f'<tspan fill="{col}" font-weight="700">{escape(repo)}</tspan></text>'
      f'<text x="{W-30}" y="{y}" font-size="13" text-anchor="end" fill="{DIM}">{when}</text></g>')

a(f'<text x="30" y="{H-18}" font-size="11" fill="#4b3d80">auto-refreshed by github actions · {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC</text>')
a("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(o))
print(f"wrote {OUT}: {len(rows)} rows")
