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
START = "      <!-- PUBLICATIONS:START -->"
END = "      <!-- PUBLICATIONS:END -->"
MORE_LABEL = "More papers under review"
SELF = "Guangyuan Wang"
# Trailing author marks: * equal contribution, † equal advising.
AUTHOR_MARKS = "*†"
# Thumbnails are 16:10 images; see tools/make_thumbnail.py.
THUMB_WIDTH, THUMB_HEIGHT = 640, 400


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


def render_thumbnail(publication):
    """A figure linked to the paper, or a text card when no figure is available yet."""
    image = publication.get("thumbnail")
    if image:
        inner = '<img src="{}" alt="" width="{}" height="{}" loading="lazy" decoding="async">'.format(
            link_url(image), THUMB_WIDTH, THUMB_HEIGHT)
        classes = "publication-thumb"
    else:
        label = publication.get("short_title") or publication["title"].split(":")[0]
        inner = "<span>{}</span>".format(escape(label))
        classes = "publication-thumb publication-thumb--placeholder"
    # The title link carries the accessible name; the thumbnail duplicates it visually.
    if publication.get("url"):
        return '<a class="{}" href="{}" tabindex="-1" aria-hidden="true">{}</a>'.format(
            classes, link_url(publication["url"]), inner)
    return '<div class="{}" aria-hidden="true">{}</div>'.format(classes, inner)


def render_links(publication):
    """Tag buttons (Paper, Code, Webpage, ...). Without explicit "links", the main URL becomes a Paper tag."""
    links = publication.get("links")
    if links is None:
        links = [{"label": "Paper", "url": publication["url"]}] if publication.get("url") else []
    if not links:
        return ""
    tags = "".join('<li><a href="{}">{}</a></li>'.format(link_url(link["url"]), escape(link["label"]))
                   for link in links)
    return '<ul class="publication-links" aria-label="Links">{}</ul>'.format(tags)


def render_publication(publication):
    title = escape(publication["title"])
    if publication.get("url"):
        title = '<a href="{}">{}</a>'.format(link_url(publication["url"]), title)
    slug = re.sub(r"[^a-z0-9]+", "-", publication["title"].lower()).strip("-")
    lines = [
        '<li id="{}">'.format(slug),
        "  " + render_thumbnail(publication),
        '  <div class="publication-body">',
        '    <h3 class="publication-title">{}</h3>'.format(title),
    ]
    # An empty author list withholds authors (e.g. papers under anonymous review).
    if publication.get("authors"):
        lines.append('    <p class="publication-authors">{}</p>'.format(
            ", ".join(render_author(author) for author in publication["authors"])))
    lines.append('    <p class="publication-venue">{}</p>'.format(escape(publication["venue"])))
    links = render_links(publication)
    if links:
        lines.append("    " + links)
    lines.extend(["  </div>", "</li>"])
    return indent("\n".join(lines), " " * 8)


def has_links(publication):
    return bool(publication.get("url") or publication.get("links"))


def render_section(selected):
    """Papers with a link are listed up front; the rest wait behind a toggle, like the older news."""
    shown = [publication for publication in selected if has_links(publication)]
    held = [publication for publication in selected if not has_links(publication)]
    parts = ['      <ol class="publication-list">',
             *[render_publication(publication) for publication in shown],
             "      </ol>"]
    if held:
        parts += ['      <details class="more-publications">',
                  "        <summary>{}</summary>".format(MORE_LABEL),
                  '        <ol class="publication-list">',
                  *[indent(render_publication(publication), "  ") for publication in held],
                  "        </ol>",
                  "      </details>"]
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the homepage needs regeneration.")
    args = parser.parse_args()
    publications = json.loads((ROOT / "publications.json").read_text(encoding="utf-8"))["publications"]
    selected = [publication for publication in publications if publication.get("selected")]
    content = render_section(selected)
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
