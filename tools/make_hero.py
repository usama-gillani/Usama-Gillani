"""Generates assets/hero.svg — animated synthwave hero banner."""
import random, sys
random.seed(7)
W, H, HZ = 1200, 380, 285          # width, height, horizon y
CX = W // 2
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#05010f"/><stop offset=".65" stop-color="#1a0638"/><stop offset="1" stop-color="#3c0d5c"/>
 </linearGradient>
 <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffd319"/><stop offset=".5" stop-color="#ff7a45"/><stop offset="1" stop-color="#ff2bd6"/>
 </linearGradient>
 <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1a0638"/><stop offset="1" stop-color="#05010f"/>
 </linearGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="1"/>
 </linearGradient>
 <mask id="gridmask"><rect x="0" y="''' + str(HZ) + '''" width="1200" height="200" fill="url(#fade)"/></mask>
 <mask id="sunstripes">
  <rect x="0" y="0" width="1200" height="400" fill="#fff"/>''')
# stripes cut into lower sun
y, h = HZ - 50, 2.5
while y < HZ:
    a(f'  <rect x="0" y="{y}" width="1200" height="{h:.1f}" fill="#000"/>')
    y += 13; h += 1.6
a(''' </mask>
 <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="bigglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
 <clipPath id="above"><rect x="0" y="0" width="1200" height="''' + str(HZ) + '''"/></clipPath>
 <clipPath id="below"><rect x="0" y="''' + str(HZ) + '''" width="1200" height="200"/></clipPath>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
# stars
for _ in range(70):
    x, yy = random.randint(0, W), random.randint(0, HZ - 20)
    r = random.choice([0.6, 0.8, 1, 1.3])
    d = random.uniform(1.5, 4.5); b = random.uniform(0, 4)
    c = random.choice(['#ffffff', '#ffffff', '#00f0ff', '#ff9bf0'])
    a(f'<circle cx="{x}" cy="{yy}" r="{r}" fill="{c}"><animate attributeName="opacity" values="0.15;1;0.15" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
# sun + halo
a(f'<circle cx="{CX}" cy="{HZ}" r="120" fill="#ff2bd6" opacity=".35" filter="url(#bigglow)"><animate attributeName="opacity" values=".25;.45;.25" dur="4s" repeatCount="indefinite"/></circle>')
a(f'<g clip-path="url(#above)"><circle cx="{CX}" cy="{HZ}" r="92" fill="url(#sun)" mask="url(#sunstripes)"/></g>')
# floor + grid
a(f'<rect x="0" y="{HZ}" width="{W}" height="{H-HZ}" fill="url(#floor)"/>')
a('<g clip-path="url(#below)" mask="url(#gridmask)" stroke="#ff2bd6" stroke-width="1.4" filter="url(#glow)">')
for i in range(-24, 25):
    a(f' <line x1="{CX}" y1="{HZ}" x2="{CX + i*90}" y2="{H+40}"/>')
a(' <g>')
for k in range(0, 14):
    yy = HZ + k * 10
    a(f'  <line x1="0" y1="{yy}" x2="{W}" y2="{yy}"/>')
a('  <animateTransform attributeName="transform" type="translate" from="0 0" to="0 10" dur="0.6s" repeatCount="indefinite"/>')
a(' </g>')
a('</g>')
a(f'<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="#ff9bf0" stroke-width="2" filter="url(#glow)"/>')
# glitch name
FONT = "font-family=\"'Orbitron','Audiowide','Arial Black','Segoe UI Black',Impact,sans-serif\" font-weight=\"900\" font-size=\"76\" text-anchor=\"middle\" letter-spacing=\"6\""
NAME, NY = "USAMA GILLANI", 100
jit = 'values="0 0;0 0;-6 0;5 0;-2 0;0 0;0 0" keyTimes="0;.86;.88;.9;.92;.94;1" dur="3.5s" repeatCount="indefinite"'
a(f'<g {FONT}>')
a(f' <text x="{CX}" y="{NY}" fill="#00f0ff" opacity=".85">{NAME}<animateTransform attributeName="transform" type="translate" {jit}/></text>')
a(f' <text x="{CX}" y="{NY}" fill="#ff2bd6" opacity=".85">{NAME}<animateTransform attributeName="transform" type="translate" values="0 0;0 0;6 0;-5 0;2 0;0 0;0 0" keyTimes="0;.86;.88;.9;.92;.94;1" dur="3.5s" repeatCount="indefinite"/></text>')
a(f' <text x="{CX}" y="{NY}" fill="#ffffff" filter="url(#glow)">{NAME}</text>')
a('</g>')
# subtitle
a(f'<text x="{CX}" y="{NY+44}" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="20" letter-spacing="5" fill="#00f0ff" filter="url(#glow)">AI ENGINEER <tspan fill="#ff2bd6">//</tspan> AGENTIC AI · LLMs · RAG</text>')
a(f'<text x="{CX}" y="{NY+72}" text-anchor="middle" font-family="\'Fira Code\',Consolas,monospace" font-size="14" letter-spacing="3" fill="#b9a7ff" opacity=".85">building AI that reasons, plans &amp; acts<tspan fill="#00f0ff">_<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></tspan></text>')
a('</svg>')
open(sys.argv[1], 'w').write('\n'.join(out))
