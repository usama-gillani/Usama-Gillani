"""Generates assets/skill-net.svg — skills as inputs of a pulsing neural network."""
import random
import sys

random.seed(42)
W, H = 1000, 420
PINK, CYAN, PURPLE, GREEN, TEXT, DIM = "#ff2bd6", "#00f0ff", "#7b2ff7", "#39ff88", "#e6dcff", "#7b6bb5"

inputs = ["PyTorch", "LangGraph", "Hugging Face", "YOLO · OpenCV", "RAG · VectorDBs", "MCP · Tools", "FastAPI · Docker"]
outputs = ["Agentic AI", "Computer Vision", "NLP · LLMs"]
layers_x = [210, 410, 590, 790]
hidden = [8, 8]


def column(n, top=90, bottom=H - 50):
    if n == 1:
        return [(top + bottom) / 2]
    step = (bottom - top) / (n - 1)
    return [top + i * step for i in range(n)]


cols = [column(len(inputs)), column(hidden[0]), column(hidden[1]), column(len(outputs), 140, H - 100)]
pts = [[(layers_x[li], y) for y in ys] for li, ys in enumerate(cols)]

o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  "font-family=\"'Fira Code','JetBrains Mono',Consolas,monospace\">")
a(f"""<defs>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{PURPLE};{PINK};{CYAN}" dur="6s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="{PINK}"><animate attributeName="stop-color" values="{PINK};{CYAN};{PURPLE};{PINK}" dur="6s" repeatCount="indefinite"/></stop>
 </linearGradient>
 <radialGradient id="node"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="{PURPLE}"/><stop offset="1" stop-color="#1a0638"/></radialGradient>
 <filter id="gl" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>""")
a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="#0b0221" stroke="url(#bd)" stroke-width="2"/>')
a(f'<text x="30" y="40" font-size="16" fill="{PINK}" filter="url(#gl)">❯ <tspan fill="{CYAN}">model.forward</tspan>'
  f'<tspan fill="{TEXT}">(</tspan><tspan fill="{GREEN}">skills</tspan><tspan fill="{TEXT}">)</tspan></text>')
a(f'<text x="{W-30}" y="40" font-size="12" text-anchor="end" fill="{DIM}">input → hidden → hidden → output</text>')

# all connections (faint)
edges = []
for li in range(3):
    for p in pts[li]:
        for q in pts[li + 1]:
            edges.append((p, q, li))
            a(f'<line x1="{p[0]}" y1="{p[1]:.1f}" x2="{q[0]}" y2="{q[1]:.1f}" stroke="{PURPLE}" stroke-opacity="0.13" stroke-width="1"/>')

# signals: random forward chains so pulses look like they propagate layer by layer
CYCLE = 6.0
for k in range(40):
    start = random.uniform(0, CYCLE)
    i0 = random.randrange(len(pts[0]))
    path_nodes = [pts[0][i0]] + [random.choice(pts[l]) for l in (1, 2, 3)]
    for li in range(3):
        p, q = path_nodes[li], path_nodes[li + 1]
        col = [PINK, PURPLE, CYAN][li]
        t0 = (start + li * 0.55) % CYCLE
        f0, f1 = t0 / CYCLE, (t0 + 0.55) / CYCLE
        if f1 > 1:  # keep each hop inside one cycle
            f0, f1 = f0 - (f1 - 1) - 0.001, 0.999
        d = f"M{p[0]},{p[1]:.1f} L{q[0]},{q[1]:.1f}"
        a(f'<line x1="{p[0]}" y1="{p[1]:.1f}" x2="{q[0]}" y2="{q[1]:.1f}" stroke="{col}" stroke-width="1.5" opacity="0">'
          f'<animate attributeName="opacity" values="0;0;.7;0;0" keyTimes="0;{f0:.3f};{(f0+f1)/2:.3f};{f1:.3f};1" dur="{CYCLE}s" repeatCount="indefinite"/></line>')
        a(f'<circle r="3.5" fill="#fff" opacity="0" filter="url(#gl)">'
          f'<animateMotion path="{d}" dur="{CYCLE}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{f0:.3f};{f1:.3f};1"/>'
          f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f0:.3f};{f0+0.003:.3f};{f1-0.003:.3f};{f1:.3f};1" dur="{CYCLE}s" repeatCount="indefinite"/></circle>')

# nodes
for li, layer in enumerate(pts):
    for ni, (x, y) in enumerate(layer):
        r = 9 if li in (0, 3) else 7
        col = [PINK, PURPLE, PURPLE, GREEN][li]
        b = random.uniform(0, 2.5)
        a(f'<circle cx="{x}" cy="{y:.1f}" r="{r+6}" fill="{col}" opacity=".15" filter="url(#gl)">'
          f'<animate attributeName="opacity" values=".08;.4;.08" dur="2.5s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
        a(f'<circle cx="{x}" cy="{y:.1f}" r="{r}" fill="#12042b" stroke="{col}" stroke-width="2"/>')
        a(f'<circle cx="{x}" cy="{y:.1f}" r="{r-4}" fill="{col}"><animate attributeName="r" values="{r-5};{r-2};{r-5}" dur="2.5s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')

for (x, y), name in zip(pts[0], inputs):
    a(f'<text x="{x-22}" y="{y+5:.1f}" font-size="14" text-anchor="end" fill="{TEXT}">{name}</text>')
for (x, y), name in zip(pts[3], outputs):
    a(f'<text x="{x+22}" y="{y+5:.1f}" font-size="15" font-weight="700" fill="{GREEN}" filter="url(#gl)">{name}</text>')

# softmax-ish caption
a(f'<text x="{W-30}" y="{H-22}" font-size="13" text-anchor="end" fill="{DIM}">argmax → <tspan fill="{PINK}" font-weight="700">AI Engineer</tspan> '
  f'<tspan fill="{CYAN}">(p = 0.99)</tspan></text>')
a("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
print("wrote", sys.argv[1])
