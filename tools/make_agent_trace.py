"""Generates assets/agent-trace.svg — a looping animation of an agent run.

query -> planner -> (web_search | rag.retrieve | code_exec) -> reflect -> answer
Every animation shares one 8s cycle; timings are fractions of that cycle.
"""
import sys

T = 8  # seconds per loop
W, H = 1000, 400
PINK, CYAN, PURPLE, GREEN, TEXT, DIM = "#ff2bd6", "#00f0ff", "#7b2ff7", "#39ff88", "#e6dcff", "#7b6bb5"

nodes = {  # id: (cx, cy, w, label, color, active_from, active_to)
    "query":   (105, 200, 150, "👤 query",       PINK,   0.00, 0.16),
    "planner": (300, 200, 150, "🧠 planner",     PURPLE, 0.13, 0.27),
    "search":  (520, 95,  180, "🔎 web_search",  CYAN,   0.33, 0.48),
    "rag":     (520, 200, 180, "📚 rag.retrieve", CYAN,  0.35, 0.50),
    "code":    (520, 305, 180, "🐍 code_exec",   CYAN,   0.37, 0.52),
    "reflect": (735, 200, 150, "🪞 reflect",     PURPLE, 0.56, 0.68),
    "answer":  (905, 200, 140, "✅ answer",      GREEN,  0.73, 0.97),
}
NH = 50
edges = [  # src, dst, travel_start, travel_end, color
    ("query", "planner", 0.05, 0.14, PINK),
    ("planner", "search", 0.22, 0.34, PURPLE),
    ("planner", "rag", 0.23, 0.35, PURPLE),
    ("planner", "code", 0.24, 0.36, PURPLE),
    ("search", "reflect", 0.46, 0.57, CYAN),
    ("rag", "reflect", 0.48, 0.58, CYAN),
    ("code", "reflect", 0.50, 0.59, CYAN),
    ("reflect", "answer", 0.65, 0.74, GREEN),
]
status = [  # text, from, to
    ("parsing query · extracting intent…", 0.00, 0.20),
    ("planner → dispatching 3 tools in parallel", 0.20, 0.45),
    ("retrieved 12 chunks · grounding the answer", 0.45, 0.63),
    ("reflect: self-check passed ✓ no hallucinations", 0.63, 0.75),
    ("answer ready in 2.4s ⚡", 0.75, 1.00),
]


def window(t0, t1, on="1", off="0", fade=0.02):
    """values/keyTimes strings for an attribute that is `on` only inside [t0, t1]."""
    a, b = max(t0 - fade, 0), min(t1 + fade, 1)
    kt = [0, a, t0, t1, b, 1]
    vals = [off, off, on, on, off, off]
    # de-duplicate equal keyTimes at the edges (keyTimes must be non-decreasing; equal is allowed)
    return ";".join(vals), ";".join(f"{k:.3f}" for k in kt)


def edge_path(s, d):
    sx, sy, sw = nodes[s][0], nodes[s][1], nodes[s][2]
    dx, dy, dw = nodes[d][0], nodes[d][1], nodes[d][2]
    x1, x2 = sx + sw / 2, dx - dw / 2
    mx = (x1 + x2) / 2
    return f"M{x1:.0f},{sy} C{mx:.0f},{sy} {mx:.0f},{dy} {x2:.0f},{dy}"


o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  "font-family=\"'Fira Code','JetBrains Mono',Consolas,monospace\">")
a(f"""<defs>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{PINK}"><animate attributeName="stop-color" values="{PINK};{CYAN};{PURPLE};{PINK}" dur="6s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{PURPLE};{PINK};{CYAN}" dur="6s" repeatCount="indefinite"/></stop>
 </linearGradient>
 <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#2a1158"/></pattern>
 <filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="halo" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>""")
a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="#0b0221" stroke="url(#bd)" stroke-width="2"/>')
a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="url(#dots)"/>')
a(f'<text x="30" y="40" font-size="16" fill="{PINK}" filter="url(#gl)">❯ <tspan fill="{CYAN}">agent.run</tspan>'
  f'<tspan fill="{TEXT}">(</tspan><tspan fill="{GREEN}">"summarize Q3 contracts &amp; flag risks"</tspan><tspan fill="{TEXT}">)</tspan></text>')

# loop counter in the corner
a(f'<text x="{W-30}" y="40" font-size="12" text-anchor="end" fill="{DIM}">langgraph · live trace</text>')

# edges (static rail + travelling pulse)
for i, (s, d, t0, t1, col) in enumerate(edges):
    p = edge_path(s, d)
    a(f'<path id="e{i}" d="{p}" fill="none" stroke="#2a1158" stroke-width="2"/>')
    vals, kt = window(t0, t1)
    a(f'<path d="{p}" fill="none" stroke="{col}" stroke-width="2" opacity="0" filter="url(#gl)">'
      f'<animate attributeName="opacity" values="{vals.replace("1", "0.55")}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></path>')
    a(f'<circle r="5" fill="#fff" opacity="0" filter="url(#gl)">'
      f'<animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{t0:.3f};{t1:.3f};1"><mpath href="#e{i}"/></animateMotion>'
      f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{t0:.3f};{t0+0.005:.3f};{t1:.3f};{t1+0.005:.3f};1" dur="{T}s" repeatCount="indefinite"/></circle>')

# nodes
for nid, (cx, cy, w, label, col, t0, t1) in nodes.items():
    x, y = cx - w / 2, cy - NH / 2
    vals, kt = window(t0, t1)
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="12" fill="{col}" opacity="0" filter="url(#halo)">'
      f'<animate attributeName="opacity" values="{vals.replace("1", "0.55")}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="12" fill="#12042b" stroke="{col}" stroke-width="1.5" stroke-opacity="0.45">'
      f'<animate attributeName="stroke-opacity" values="{vals.replace("1", "1").replace("0", "0.45")}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect>')
    a(f'<text x="{cx}" y="{cy+5}" font-size="14" text-anchor="middle" fill="{TEXT}">{label}</text>')

# status ticker
a(f'<line x1="30" y1="{H-62}" x2="{W-30}" y2="{H-62}" stroke="#2a1158"/>')
for txt, t0, t1 in status:
    vals, kt = window(t0 + 0.008, t1 - 0.008, fade=0.006)
    col = GREEN if "ready" in txt or "✓" in txt else CYAN
    a(f'<text x="30" y="{H-30}" font-size="15" fill="{col}" opacity="0" filter="url(#gl)">'
      f'<tspan fill="{PINK}">●</tspan>  {txt.replace("&", "&amp;")}'
      f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></text>')

# progress bar along the bottom
a(f'<rect x="30" y="{H-18}" width="{W-60}" height="3" rx="1.5" fill="#1a0638"/>')
a(f'<rect x="30" y="{H-18}" width="0" height="3" rx="1.5" fill="{PINK}" filter="url(#gl)">'
  f'<animate attributeName="width" values="0;{W-60}" dur="{T}s" repeatCount="indefinite"/></rect>')

a("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
print("wrote", sys.argv[1])
