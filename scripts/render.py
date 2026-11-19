#!/usr/bin/env python3
import json
import os
import subprocess
import textwrap
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

OWNER = "BardiaYaghmaie"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 blue="#58a6ff", key="#79c0ff", green="#3fb950", pill="#1f6feb26", pill_text="#58a6ff",
                 accent_a="#58a6ff", accent_b="#3fb950"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  blue="#0969da", key="#0550ae", green="#1a7f37", pill="#ddf4ff", pill_text="#0969da",
                  accent_a="#0969da", accent_b="#1a7f37"),
}

LANG_COLORS = {"Go": "#00ADD8", "Rust": "#dea584", "Python": "#3572A5", "Shell": "#89e051"}

PROJECTS = [
    ("kubectl-edit-secret", "krew index",
     "kubectl plugin that opens Secrets as plain text in your editor, re-encodes on save and shows what changed. No more base64 round-trips."),
    ("bardiup", "operator",
     "Kubernetes operator that backs up PVCs to any S3 bucket with GFS retention. Plain tar.gz archives, namespaced self-service, no node agents."),
    ("pingate", "pingora",
     "Reverse proxy and load balancer in Rust on Pingora. Discovers Docker Compose and Swarm workloads from labels, configured by env vars alone."),
    ("distributed-n8n-on-k8s", "HA",
     "n8n in queue mode on Kubernetes: CloudNativePG failover, Redis Sentinel, Gateway API and KEDA autoscaling on queue depth."),
    ("Graph-Edge-Magic-Total-Labeling", "BSc thesis",
     "Exact CP-SAT solver, verifier and visualizer for edge-magic total labelings of four-partite graphs, with the article."),
    ("Party-Management-Telegram-Bot", "bot",
     "Bilingual Telegram bot for managing RSVPs, guest lists and event details."),
]

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z")
STAR_ICON = ("M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z")


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch_repo(name, tok):
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{name}",
                                 headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def banner(t):
    w, line_h, x0, xv = 960, 32, 44, 196
    rows = [
        ("Name", "Bardia Yaghmaie"),
        ("Role", "Site Reliability Engineer @ Yektanet"),
        ("Focus", "Kubernetes · Platform Engineering · DevSecOps"),
        ("Serving", "4 clusters · 200+ nodes · 50k+ req/s"),
        ("Off-hours", "Go operators, kubectl plugins, Rust proxies"),
    ]
    cmd = "kubectl describe bardia"
    type_end = 0.4 + len(cmd) * 0.04
    y0 = 92
    h = y0 + line_h * (len(rows) + 2) + 30

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Bardia Yaghmaie, Site Reliability Engineer">',
           '<defs>',
           f'<linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="{t["accent_a"]}"/><stop offset="1" stop-color="{t["accent_b"]}"/></linearGradient>',
           f'<clipPath id="typing"><rect x="{x0 + 22}" y="{y0 - 22}" height="32" width="0">'
           f'<animate attributeName="width" from="0" to="{len(cmd) * 10.3 + 4:.0f}" begin="0.4s" dur="{type_end - 0.4:.2f}s" fill="freeze"/></rect></clipPath>',
           f'<clipPath id="frame"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>',
           '</defs>',
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>',
           f'<rect x="1" y="1" width="{w - 2}" height="3" fill="url(#accent)" clip-path="url(#frame)"/>',
           f'<circle cx="28" cy="28" r="6.5" fill="#ff5f56"/><circle cx="50" cy="28" r="6.5" fill="#ffbd2e"/><circle cx="72" cy="28" r="6.5" fill="#27c93f"/>',
           f'<text x="{w / 2}" y="33" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">bardia@prod-cluster: ~</text>',
           f'<line x1="1" y1="52" x2="{w - 1}" y2="52" stroke="{t["border"]}"/>',
           f'<g font-family="{MONO}" font-size="17">',
           f'<text x="{x0}" y="{y0}" fill="{t["green"]}" font-weight="600">$</text>',
           f'<text x="{x0 + 22}" y="{y0}" fill="{t["text"]}" clip-path="url(#typing)">{cmd}</text>']

    begin = type_end + 0.25
    y = y0
    for i, (k, v) in enumerate(rows):
        y += line_h
        b = begin + i * 0.18
        out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
                   f'<text x="{x0}" y="{y}" fill="{t["key"]}">{k}:</text>'
                   f'<text x="{xv}" y="{y}" fill="{t["text"]}">{escape(v)}</text></g>')
    y += line_h
    b = begin + len(rows) * 0.18
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>'
               f'<text x="{x0}" y="{y}" fill="{t["key"]}">Status:</text>'
               f'<circle cx="{xv + 6}" cy="{y - 6}" r="6" fill="{t["green"]}">'
               f'<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" begin="{b + 0.4:.2f}s" repeatCount="indefinite"/></circle>'
               f'<text x="{xv + 22}" y="{y}" fill="{t["green"]}">Running</text>'
               f'<text x="{xv + 112}" y="{y}" fill="{t["muted"]}">  # restarts: 0 (that we talk about)</text></g>')
    y += line_h
    b += 0.5
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.2s" fill="freeze"/>'
               f'<text x="{x0}" y="{y}" fill="{t["green"]}" font-weight="600">$</text>'
               f'<rect x="{x0 + 22}" y="{y - 16}" width="10" height="20" fill="{t["text"]}">'
               f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{b:.2f}s" repeatCount="indefinite"/></rect></g>')
    out += ['</g>', '</svg>']
    return "\n".join(out)


def card(name, pill, desc, lang, stars, t):
    w, h = 440, 168
    lines = textwrap.wrap(desc, 60)[:3]
    pill_w = len(pill) * 7 + 18
    name_w = sum(11 if c.isupper() else 5.5 if c in '-.' else 8.6 for c in name)
    pill_x = min(44 + name_w + 14, w - pill_w - 18)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(name)}">',
           f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>',
           f'<path transform="translate(20 20)" fill="{t["muted"]}" d="{REPO_ICON}"/>',
           f'<text x="44" y="33" font-family="{SANS}" font-size="16" font-weight="600" fill="{t["blue"]}">{escape(name)}</text>',
           f'<rect x="{pill_x:.0f}" y="18" width="{pill_w}" height="20" rx="10" fill="{t["pill"]}" stroke="{t["pill_text"]}" stroke-opacity="0.35"/>',
           f'<text x="{pill_x + pill_w / 2:.0f}" y="32" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="500" fill="{t["pill_text"]}">{escape(pill)}</text>']
    for i, ln in enumerate(lines):
        out.append(f'<text x="20" y="{66 + i * 21}" font-family="{SANS}" font-size="13.5" fill="{t["muted"]}">{escape(ln)}</text>')
    fy = h - 22
    x = 20
    if lang:
        out.append(f'<circle cx="{x + 6}" cy="{fy - 4.5}" r="6" fill="{LANG_COLORS.get(lang, t["muted"])}"/>')
        out.append(f'<text x="{x + 18}" y="{fy}" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{escape(lang)}</text>')
        x += 18 + len(lang) * 7.5 + 18
    if stars:
        out.append(f'<path transform="translate({x:.0f} {fy - 12.5})" fill="{t["muted"]}" d="{STAR_ICON}"/>')
        out.append(f'<text x="{x + 21:.0f}" y="{fy}" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{stars}</text>')
    out.append('</svg>')
    return "\n".join(out)


def main():
    (ASSETS / "cards").mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (ASSETS / f"banner-{theme}.svg").write_text(banner(t))
    tok = token()
    for name, pill, desc in PROJECTS:
        repo = fetch_repo(name, tok)
        for theme, t in THEMES.items():
            svg = card(name, pill, desc, repo.get("language"), repo["stargazers_count"], t)
            (ASSETS / "cards" / f"{name}-{theme}.svg").write_text(svg)


if __name__ == "__main__":
    main()
