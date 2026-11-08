#!/usr/bin/env python3
"""Render publications.json into the homepage using only the standard library."""

import argparse
from html import escape
import json
from pathlib import Path
import re
from textwrap import indent
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
START = "        <!-- PUBLICATIONS:START -->"
END = "        <!-- PUBLICATIONS:END -->"
LINK_LABELS = {
    "pdf": "PDF",
    "code": "Code",
    "project": "Project",
    "poster": "Poster",
    "slides": "Slides",
}


def link_url(value):
    """Allow web links and local files, but never executable URL schemes."""
    parsed = urlsplit(value)
    if parsed.scheme not in ("", "https", "http") or value.startswith("//"):
        raise ValueError("Unsupported publication URL: " + value)
    return escape(value, quote=True)


def render_publication(publication):
    title = escape(publication["title"])
    links = publication.get("links", {})
    title_html = (
        '<a href="{}">{}</a>'.format(link_url(links["pdf"]), title)
        if links.get("pdf") else title
    )
    authors = []
    for author in publication["authors"]:
        name = author.rstrip("*")
        formatted = escape(name)
        if name == "Guangyuan Wang":
            formatted = '<span class="self">{}</span>'.format(formatted)
        if author.endswith("*"):
            formatted += "<sup>{}</sup>".format("*" * (len(author) - len(name)))
        authors.append(formatted)

    slug = re.sub(r"[^a-z0-9]+", "-", publication["title"].lower()).strip("-")
    lines = [
        '<li class="publication" id="{}">'.format(slug),
        '  <div class="publication-badges">',
        '    <span class="venue-badge">{}</span>'.format(escape(publication.get("badge", "Research"))),
    ]
    if publication.get("badge_detail"):
        lines.append('    <span class="badge-detail">{}</span>'.format(escape(publication["badge_detail"])))
    lines.extend([
        "  </div>",
        '  <div class="publication-content">',
        '    <h3 class="publication-title">{}</h3>'.format(title_html),
        '    <p class="publication-authors">{}</p>'.format(", ".join(authors)),
        '    <p class="publication-venue">{}</p>'.format(escape(publication["venue"])),
    ])
    if publication.get("award"):
        lines.append('    <span class="publication-award">{}</span>'.format(escape(publication["award"])))
    resource_links = [
        '      <a class="resource-link" href="{}">{}</a>'.format(link_url(links[key]), label)
        for key, label in LINK_LABELS.items() if links.get(key)
    ]
    if resource_links:
        lines.extend(['    <div class="publication-links">'] + resource_links + ["    </div>"])
    lines.extend(["  </div>", "</li>"])
    return indent("\n".join(lines), " " * 8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the homepage needs regeneration.")
    args = parser.parse_args()
    publications = json.loads((ROOT / "publications.json").read_text(encoding="utf-8"))["publications"]
    selected = [publication for publication in publications if publication.get("selected")]
    content = "\n".join(render_publication(publication) for publication in selected)
    homepage = ROOT / "index.html"
    original = homepage.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("The homepage must have exactly one pair of publication markers.")
    before, rest = original.split(START, 1)
    _, after = rest.split(END, 1)
    updated = before + START + "\n" + content + "\n" + END + after
    if args.check:
        if original != updated:
            parser.exit(1, "Publications are out of date. Run python3 tools/render_publications.py\n")
        print("Publication HTML matches publications.json ({} entries).".format(len(selected)))
    else:
        homepage.write_text(updated, encoding="utf-8")
        print("Rendered {} publications into index.html.".format(len(selected)))


if __name__ == "__main__":
    main()
