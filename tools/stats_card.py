"""Builds an animated neon stats card (SVG) from the GitHub GraphQL API.

Usage: GITHUB_TOKEN=... python3 stats_card.py <username> <out.svg>
Stdlib only, so it runs on a bare GitHub Actions runner.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from collections import Counter
from html import escape

USER, OUT = sys.argv[1], sys.argv[2]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
  }
}"""


def gql():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "neon-stats-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def streaks(days):
    """Current streak (today may still be 0 without breaking it) and longest streak."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1  # today not counted yet
    while i >= 0 and counts[i]:
        cur += 1
        i -= 1
    return cur, longest


u = gql()
cc = u["contributionsCollection"]
days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
cur_streak, best_streak = streaks(days)
repos = u["repositories"]["nodes"]
stars = sum(r["stargazerCount"] for r in repos)

lang_size, lang_color = Counter(), {}
for r in repos:
    for e in r["languages"]["edges"]:
        lang_size[e["node"]["name"]] += e["size"]
        lang_color[e["node"]["name"]] = e["node"]["color"] or "#7b2ff7"
total = sum(lang_size.values()) or 1
langs = [(n, s / total, lang_color[n]) for n, s in lang_size.most_common(6)]

stats = [
    ("⚡", "contributions (1y)", cc["contributionCalendar"]["totalContributions"]),
    ("🔥", "current streak", f"{cur_streak}d"),
    ("🏆", "longest streak", f"{best_streak}d"),
    ("📦", "commits (1y)", cc["totalCommitContributions"] + cc["restrictedContributionsCount"]),
    ("🔀", "pull requests", cc["totalPullRequestContributions"]),
    ("⭐", "stars earned", stars),
    ("🗂️", "public repos", u["repositories"]["totalCount"]),
]

W, H = 1000, 300
s = []
a = s.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  'font-family="\'Fira Code\',\'JetBrains Mono\',Consolas,monospace">')
a("""<defs>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ff2bd6"><animate attributeName="stop-color" values="#ff2bd6;#00f0ff;#7b2ff7;#ff2bd6" dur="6s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="#00f0ff"><animate attributeName="stop-color" values="#00f0ff;#7b2ff7;#ff2bd6;#00f0ff" dur="6s" repeatCount="indefinite"/></stop>
 </linearGradient>
 <filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <style>.r{opacity:0;animation:f .5s ease forwards}@keyframes f{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}</style>
</defs>""")
a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="#0b0221" stroke="url(#bd)" stroke-width="2"/>')
a('<text x="36" y="48" font-size="20" font-weight="700" fill="#ff2bd6" filter="url(#gl)">❯ stats.exe</text>')
a(f'<text x="36" y="72" font-size="12" fill="#7b6bb5">@{escape(USER)} · updated {dt.date.today().isoformat()}</text>')

for i, (ico, label, val) in enumerate(stats):
    y = 108 + i * 26
    a(f'<g class="r" style="animation-delay:{0.15 * i + 0.2:.2f}s">'
      f'<text x="36" y="{y}" font-size="15">{ico}</text>'
      f'<text x="64" y="{y}" font-size="15" fill="#e6dcff">{escape(label)}</text>'
      f'<text x="420" y="{y}" font-size="16" font-weight="700" text-anchor="end" fill="#00f0ff" filter="url(#gl)">{escape(str(val))}</text></g>')

a('<line x1="470" y1="36" x2="470" y2="264" stroke="#2a1158" stroke-width="2"/>')
a('<text x="510" y="48" font-size="20" font-weight="700" fill="#00f0ff" filter="url(#gl)">❯ top_langs</text>')
BAR_X, BAR_W = 650, 290
if not langs:
    a('<text x="510" y="110" font-size="14" fill="#7b6bb5">no public code yet — loading… ⏳</text>')
for i, (name, frac, color) in enumerate(langs):
    y = 98 + i * 30
    w = max(BAR_W * frac, 4)
    d = 0.3 + 0.15 * i
    a(f'<g class="r" style="animation-delay:{d:.2f}s">'
      f'<circle cx="516" cy="{y-5}" r="5" fill="{color}"/>'
      f'<text x="530" y="{y}" font-size="14" fill="#e6dcff">{escape(name)}</text>'
      f'<rect x="{BAR_X}" y="{y-12}" width="{BAR_W}" height="10" rx="5" fill="#1a0638"/>'
      f'<rect x="{BAR_X}" y="{y-12}" width="0" height="10" rx="5" fill="{color}" filter="url(#gl)">'
      f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{d + 0.2:.2f}s" dur="1s" fill="freeze"/></rect>'
      f'<text x="{BAR_X + BAR_W + 10}" y="{y}" font-size="12" fill="#9d8fd9" text-anchor="start">{frac*100:.0f}%</text></g>')

a("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(s))
print(f"wrote {OUT}: {len(langs)} langs, streak {cur_streak}/{best_streak}")
