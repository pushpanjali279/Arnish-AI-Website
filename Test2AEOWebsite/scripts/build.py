#!/usr/bin/env python3
"""Build a deploy-ready copy of site/ into dist/.

Source pages in site/ use root-relative URLs ("/about/", "/#organization") so
they work on any domain and in local preview. This script reads the domain
from DOMAIN in .env (or --domain) and, in dist/ only:

  * turns canonical links, og:url and JSON-LD URLs into absolute https URLs
  * writes sitemap.xml and adds the Sitemap line to robots.txt

Without a real domain it still builds dist/ with relative URLs and no sitemap,
and says so. No third-party packages needed.

Usage:
  python scripts/build.py                      # domain from .env
  python scripts/build.py --domain example.com
  python scripts/build.py --require-domain     # fail if no real domain (used by deploy.sh)
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site"
OUT = ROOT / "dist"
PLACEHOLDERS = {"", "yourdomain.com", "example.com"}


def read_env_domain():
    env = ROOT / ".env"
    if not env.exists():
        return ""
    for line in env.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*DOMAIN\s*=\s*(.*)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return ""


def normalise(domain):
    d = domain.strip().rstrip("/")
    d = re.sub(r"^https?://", "", d)
    return d


def absolutise_html(html, base):
    html = re.sub(r'(<link rel="canonical" href=")(/[^"]*)"', lambda m: f'{m.group(1)}{base}{m.group(2)}"', html)
    html = re.sub(r'(<meta property="og:url" content=")(/[^"]*)"', lambda m: f'{m.group(1)}{base}{m.group(2)}"', html)

    def fix_jsonld(m):
        block = re.sub(r'(":\s*")(/[^"]*)"', lambda n: f'{n.group(1)}{base}{n.group(2)}"', m.group(2))
        return m.group(1) + block + m.group(3)

    return re.sub(r'(?s)(<script type="application/ld\+json">)(.*?)(</script>)', fix_jsonld, html)


def page_url(path):
    rel = path.relative_to(OUT).as_posix()
    return "/" if rel == "index.html" else "/" + rel[: -len("index.html")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default=None)
    ap.add_argument("--require-domain", action="store_true")
    args = ap.parse_args()

    domain = normalise(args.domain if args.domain is not None else read_env_domain())
    has_domain = domain.lower() not in PLACEHOLDERS
    if args.require_domain and not has_domain:
        sys.exit("ERROR: no real domain set. Put DOMAIN=yourrealdomain.com in .env first.")

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns("_*", ".DS_Store", "Thumbs.db"))

    base = f"https://{domain}" if has_domain else ""
    pages = sorted(OUT.rglob("index.html"))
    errors = []
    for p in pages:
        html = p.read_text(encoding="utf-8")
        if base:
            html = absolutise_html(html, base)
            p.write_text(html, encoding="utf-8")
        for blk in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', html):
            try:
                json.loads(blk)
            except ValueError as e:
                errors.append(f"{p.relative_to(OUT)}: invalid JSON-LD ({e})")
        if "yourdomain" in html:
            errors.append(f"{p.relative_to(OUT)}: contains placeholder domain")

    if base:
        today = dt.date.today().isoformat()
        urls = "\n".join(
            f"  <url><loc>{base}{page_url(p)}</loc><lastmod>{dt.date.fromtimestamp(p.stat().st_mtime).isoformat() or today}</lastmod></url>"
            for p in pages
        )
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
            encoding="utf-8",
        )
        robots = OUT / "robots.txt"
        robots.write_text(robots.read_text(encoding="utf-8").rstrip() + f"\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    print(f"Built {len(pages)} pages into dist/")
    if base:
        print(f"Absolute URLs and sitemap.xml use {base}")
    else:
        print("No real domain set: URLs stay relative and no sitemap.xml was written.")


if __name__ == "__main__":
    main()
