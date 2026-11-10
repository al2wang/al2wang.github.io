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
SELF = "Guangyuan Wang"
# Trailing author marks: * equal contribution, † equal advising.
AUTHOR_MARKS = "*†"


def link_url(value):
    """Allow web links and local files, but never executable URL schemes."""
    parsed = urlsplit(value)
    if parsed.scheme not in ("", "https", "http") or value.startswith("//"):
        raise ValueError("Unsupported publication URL: " + value)
    return escape(value, quote=True)


def render_author(author):
    name = author.rstrip(AUTHOR_MARKS)
    formatted = escape(name)
    if name == SELF:
        formatted = '<span class="self">{}</span>'.format(formatted)
    marks = author[len(name):]
    if marks:
        formatted += "<sup>{}</sup>".format(escape(marks))
    return formatted


def render_publication(publication):
    title = escape(publication["title"])
    if publication.get("url"):
        title = '<a href="{}">{}</a>'.format(link_url(publication["url"]), title)
    slug = re.sub(r"[^a-z0-9]+", "-", publication["title"].lower()).strip("-")
    lines = [
        '<li id="{}">'.format(slug),
        '  <h3 class="publication-title">{}</h3>'.format(title),
    ]
    # An empty author list withholds authors (e.g. papers under anonymous review).
    if publication.get("authors"):
        lines.append('  <p class="publication-authors">{}</p>'.format(
            ", ".join(render_author(author) for author in publication["authors"])))
    lines.extend([
        '  <p class="publication-venue">{}</p>'.format(escape(publication["venue"])),
        "</li>",
    ])
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
    if START not in original and END not in original:
        print("The minimal homepage omits publications; no changes needed.")
        return
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
