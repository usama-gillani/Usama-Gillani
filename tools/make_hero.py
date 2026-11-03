"""Generates assets/hero.svg — 'agent world' hero banner.

Synthwave scene + a walking robot agent (agentic), reward pop-ups (RL),
neural-network constellations (NN) and floating token chips (NLP).
Everything loops on the same LOOP-second cycle so it stays in sync.
"""
import random
import sys

random.seed(7)
W, H, HZ = 1200, 380, 285          # width, height, horizon y
CX = W // 2
LOOP = 16                           # robot walk cycle (s)
FEET_Y = 352                        # robot ground line
X0, X1 = -120, W + 120              # walk start / end
PINK, CYAN, PURPLE, GREEN, YELLOW, TEXT = "#ff2bd6", "#00f0ff", "#7b2ff7", "#39ff88", "#ffd319", "#e6dcff"

o = []
a = o.append


def x_at(frac):
    return X0 + (X1 - X0) * frac


def win(t0, t1, fade=0.015, on="1", off="0"):
    kt = [0, max(t0 - fade, 0), t0, t1, min(t1 + fade, 1), 1]
    return ";".join([off, off, on, on, off, off]), ";".join(f"{k:.3f}" for k in kt)


a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'''<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#05010f"/><stop offset=".65" stop-color="#1a0638"/><stop offset="1" stop-color="#3c0d5c"/>
 </linearGradient>
 <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{YELLOW}"/><stop offset=".5" stop-color="#ff7a45"/><stop offset="1" stop-color="{PINK}"/>
 </linearGradient>
 <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1a0638"/><stop offset="1" stop-color="#05010f"/>
 </linearGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="1"/>
 </linearGradient>
 <mask id="gridmask"><rect x="0" y="{HZ}" width="{W}" height="200" fill="url(#fade)"/></mask>
 <mask id="sunstripes">
  <rect x="0" y="0" width="{W}" height="{H+20}" fill="#fff"/>''')
y, h = HZ - 50, 2.5
while y < HZ:
    a(f'  <rect x="0" y="{y}" width="{W}" height="{h:.1f}" fill="#000"/>')
    y += 13
    h += 1.6
a(f''' </mask>
 <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="bigglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
 <clipPath id="above"><rect x="0" y="0" width="{W}" height="{HZ}"/></clipPath>
 <clipPath id="below"><rect x="0" y="{HZ}" width="{W}" height="200"/></clipPath>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# ── background stars (dim) ──
for _ in range(45):
    x, yy = random.randint(0, W), random.randint(0, HZ - 30)
    if 230 < x < 970 and yy < 190:   # keep the title area clean
        continue
    d, b = random.uniform(2, 5), random.uniform(0, 4)
    a(f'<circle cx="{x}" cy="{yy}" r="{random.choice([0.6, 0.9, 1.1])}" fill="#ffffff">'
      f'<animate attributeName="opacity" values="0.1;0.8;0.1" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')

# ── NN constellations (neural net touch) ──
clusters = [
    [(55, 62), (140, 38), (205, 98), (112, 132), (42, 178), (178, 196), (95, 236)],
    [(1000, 52), (1085, 92), (1158, 44), (1022, 152), (1135, 160), (1168, 228), (1062, 222)],
]
for pts in clusters:
    links = []
    for i, p in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: (pts[j][0]-p[0])**2 + (pts[j][1]-p[1])**2)[1:3]
        for j in near:
            if (j, i) not in links:
                links.append((i, j))
    for i, j in links:
        (x1, y1), (x2, y2) = pts[i], pts[j]
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PURPLE}" stroke-opacity=".35" stroke-width="1"/>')
    for k, (i, j) in enumerate(links):
        (x1, y1), (x2, y2) = pts[i], pts[j]
        b = random.uniform(0, 4)
        a(f'<circle r="2.2" fill="{CYAN}" filter="url(#sglow)" opacity="0">'
          f'<animateMotion path="M{x1},{y1} L{x2},{y2}" dur="1.6s" begin="{b:.2f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="1.6s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
    for (x, yy) in pts:
        b = random.uniform(0, 3)
        a(f'<circle cx="{x}" cy="{yy}" r="3.2" fill="{PINK}" filter="url(#sglow)">'
          f'<animate attributeName="r" values="2.4;4;2.4" dur="2.4s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')

# ── sun ──
a(f'<circle cx="{CX}" cy="{HZ}" r="120" fill="{PINK}" opacity=".35" filter="url(#bigglow)"><animate attributeName="opacity" values=".25;.45;.25" dur="4s" repeatCount="indefinite"/></circle>')
a(f'<g clip-path="url(#above)"><circle cx="{CX}" cy="{HZ}" r="92" fill="url(#sun)" mask="url(#sunstripes)"/></g>')

# ── NLP / RL tokens floating up from the horizon ──
tokens = [("attention", PINK), ("tool_call()", CYAN), ("π(a|s)", GREEN), ("softmax", PURPLE),
          ("Q(s,a)", CYAN), ("embed()", PINK), ("∇θ L", YELLOW), ("&lt;plan&gt;", GREEN)]
slots = [70, 195, 70, 195, 1010, 1135, 1010, 1135]
starts = [0, 2, 4, 6, 1, 3, 5, 7]
for i, ((tok, col), x) in enumerate(zip(tokens, slots)):
    b = starts[i]
    w = 11 + 8.2 * len(tok.replace("&lt;", "<").replace("&gt;", ">"))
    a(f'<g opacity="0">'
      f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -90" dur="8s" begin="{b}s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.2;.7;1" dur="8s" begin="{b}s" repeatCount="indefinite"/>'
      f'<rect x="{x - w/2:.0f}" y="{HZ - 30}" width="{w:.0f}" height="20" rx="10" fill="#12042b" stroke="{col}" stroke-width="1"/>'
      f'<text x="{x}" y="{HZ - 16}" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="12" fill="{col}">{tok}</text></g>')

# ── floor + grid ──
a(f'<rect x="0" y="{HZ}" width="{W}" height="{H-HZ}" fill="url(#floor)"/>')
a(f'<g clip-path="url(#below)" mask="url(#gridmask)" stroke="{PINK}" stroke-width="1.4" filter="url(#glow)">')
for i in range(-24, 25):
    a(f' <line x1="{CX}" y1="{HZ}" x2="{CX + i*90}" y2="{H+40}"/>')
a(' <g>')
for k in range(0, 12):
    yy = HZ + k * 10
    a(f'  <line x1="0" y1="{yy}" x2="{W}" y2="{yy}"/>')
a('  <animateTransform attributeName="transform" type="translate" from="0 0" to="0 10" dur="0.6s" repeatCount="indefinite"/>')
a(' </g>')
a('</g>')
a(f'<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="#ff9bf0" stroke-width="2" filter="url(#glow)"/>')

# ── RL reward pop-ups along the walk ──
for frac, label in ((0.20, "+1 reward"), (0.50, "+1 reward"), (0.80, "+10 goal ⚡")):
    x = x_at(frac)
    vals, kt = win(frac, frac + 0.06, fade=0.01)
    a(f'<g opacity="0" font-family="\'Fira Code\',Consolas,monospace" font-size="15" font-weight="700">'
      f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{LOOP}s" repeatCount="indefinite"/>'
      f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -28;0 -28" keyTimes="0;{frac:.3f};{frac+0.07:.3f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
      f'<text x="{x:.0f}" y="228" text-anchor="middle" fill="{GREEN}" filter="url(#sglow)">{label}</text></g>')
    # a little glowing tile where the reward was collected
    a(f'<ellipse cx="{x:.0f}" cy="{FEET_Y+2}" rx="26" ry="6" fill="{GREEN}" opacity="0" filter="url(#glow)">'
      f'<animate attributeName="opacity" values="{win(frac, frac + 0.04, 0.01, on=".7")[0]}" keyTimes="{win(frac, frac + 0.04, 0.01)[1]}" dur="{LOOP}s" repeatCount="indefinite"/></ellipse>')

# ── the robot agent ──
a(f'<g><animateTransform attributeName="transform" type="translate" values="{X0} {FEET_Y};{X1} {FEET_Y}" dur="{LOOP}s" repeatCount="indefinite"/>')
a(' <g transform="scale(1.15)">')
a(f'  <ellipse cx="0" cy="3" rx="24" ry="4.5" fill="#000" opacity=".55"/>')
a('  <g>')  # bobbing body
a('   <animateTransform attributeName="transform" type="translate" values="0 0;0 -2.5;0 0" dur="0.6s" repeatCount="indefinite"/>')
# legs
for side, phase in ((-1, "-22;22;-22"), (1, "22;-22;22")):
    hx = side * 8
    a(f'   <g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{v} {hx} -26" for v in phase.split(";"))}" dur="0.6s" repeatCount="indefinite"/>'
      f'<rect x="{hx-4}" y="-27" width="8" height="24" rx="3" fill="#1d0b40" stroke="{CYAN}" stroke-width="1.2"/>'
      f'<rect x="{hx-6}" y="-5" width="12" height="5" rx="2" fill="{CYAN}" filter="url(#sglow)"/></g>')
# left arm swings with walk
a(f'   <g><animateTransform attributeName="transform" type="rotate" values="18 -24 -58;-18 -24 -58;18 -24 -58" dur="0.6s" repeatCount="indefinite"/>'
  f'<rect x="-29" y="-60" width="7" height="26" rx="3" fill="#1d0b40" stroke="{CYAN}" stroke-width="1.2"/></g>')
# right arm: swings, but waves while talking (bubble windows)
a(f'   <g><animateTransform attributeName="transform" type="rotate" '
  f'values="-18 24 -58;18 24 -58;-18 24 -58" dur="0.6s" repeatCount="indefinite"/>'
  f'<g><animateTransform attributeName="transform" type="rotate" values="0 24 -58;0 24 -58;-150 24 -58;-120 24 -58;-150 24 -58;-120 24 -58;0 24 -58;0 24 -58" '
  f'keyTimes="0;.28;.30;.33;.36;.39;.43;1" dur="{LOOP}s" repeatCount="indefinite"/>'
  f'<rect x="22" y="-60" width="7" height="26" rx="3" fill="#1d0b40" stroke="{CYAN}" stroke-width="1.2"/></g></g>')
# body + chest core
a(f'   <rect x="-21" y="-63" width="42" height="40" rx="9" fill="#12042b" stroke="{CYAN}" stroke-width="1.6" filter="url(#sglow)"/>')
a(f'   <circle cx="0" cy="-44" r="6" fill="{PINK}" filter="url(#glow)"><animate attributeName="r" values="4.5;7;4.5" dur="1.2s" repeatCount="indefinite"/></circle>')
a(f'   <path d="M-13,-33 h26" stroke="{PURPLE}" stroke-width="2" stroke-linecap="round"/>')
# neck + head
a(f'   <rect x="-4" y="-69" width="8" height="7" fill="#1d0b40" stroke="{CYAN}" stroke-width="1"/>')
a(f'   <rect x="-23" y="-100" width="46" height="33" rx="11" fill="#12042b" stroke="{PINK}" stroke-width="1.8" filter="url(#sglow)"/>')
a(f'   <rect x="-17" y="-93" width="34" height="15" rx="7" fill="#05010f"/>')
for ex in (-8, 8):
    a(f'   <ellipse cx="{ex}" cy="-85.5" rx="3.4" ry="3.4" fill="{CYAN}" filter="url(#sglow)">'
      f'<animate attributeName="ry" values="3.4;3.4;0.4;3.4;3.4" keyTimes="0;.88;.92;.96;1" dur="3.2s" repeatCount="indefinite"/>'
      f'<animate attributeName="cx" values="{ex-2};{ex+2};{ex-2}" dur="4s" repeatCount="indefinite"/></ellipse>')
# antenna
a(f'   <line x1="0" y1="-100" x2="0" y2="-112" stroke="{PINK}" stroke-width="2"/>')
a(f'   <circle cx="0" cy="-115" r="4" fill="{PINK}" filter="url(#glow)"><animate attributeName="opacity" values="1;.2;1" dur="0.9s" repeatCount="indefinite"/></circle>')
a('  </g>')
# speech bubbles (move with the robot, not with the bob)
bubbles = [(0.28, 0.43, "observe → plan → act"), (0.56, 0.71, "policy updated ✓ ε → 0.05")]
for t0, t1, msg in bubbles:
    vals, kt = win(t0, t1, fade=0.01)
    bw = 22 + 8.1 * len(msg)
    a(f'  <g opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{LOOP}s" repeatCount="indefinite"/>'
      f'<rect x="36" y="-112" width="{bw:.0f}" height="28" rx="12" fill="#12042b" stroke="{GREEN}" stroke-width="1.4" filter="url(#sglow)"/>'
      f'<path d="M37,-96 L26,-90 L37,-90 Z" fill="{GREEN}"/>'
      f'<text x="{36 + bw/2:.0f}" y="-93" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="13.5" fill="{GREEN}">{msg}</text></g>')
a(' </g>')
a('</g>')

# ── title (glitch) ──
FONT = "font-family=\"'Orbitron','Audiowide','Arial Black','Segoe UI Black',Impact,sans-serif\" font-weight=\"900\" font-size=\"76\" text-anchor=\"middle\" letter-spacing=\"6\""
NAME, NY = "USAMA GILLANI", 100
jit = 'keyTimes="0;.86;.88;.9;.92;.94;1" dur="3.5s" repeatCount="indefinite"'
a(f'<g {FONT}>')
a(f' <text x="{CX}" y="{NY}" fill="{CYAN}" opacity=".85">{NAME}<animateTransform attributeName="transform" type="translate" values="0 0;0 0;-6 0;5 0;-2 0;0 0;0 0" {jit}/></text>')
a(f' <text x="{CX}" y="{NY}" fill="{PINK}" opacity=".85">{NAME}<animateTransform attributeName="transform" type="translate" values="0 0;0 0;6 0;-5 0;2 0;0 0;0 0" {jit}/></text>')
a(f' <text x="{CX}" y="{NY}" fill="#ffffff" filter="url(#glow)">{NAME}</text>')
a('</g>')
a(f'<text x="{CX}" y="{NY+44}" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="20" letter-spacing="5" fill="{CYAN}" filter="url(#glow)">AI ENGINEER <tspan fill="{PINK}">//</tspan> AGENTIC AI · LLMs · RAG</text>')
a(f'<text x="{CX}" y="{NY+72}" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="14" letter-spacing="3" fill="#b9a7ff" opacity=".85">building AI that reasons, plans &amp; acts<tspan fill="{CYAN}">_<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></tspan></text>')
a('</svg>')
open(sys.argv[1], 'w').write('\n'.join(o))
print("wrote", sys.argv[1])
