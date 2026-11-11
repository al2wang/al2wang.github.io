#!/usr/bin/env python3
"""Make a 640x400 (16:10) WebP publication thumbnail.

From a PDF region (coordinates in PDF points, origin at the top left):
    python3 tools/make_thumbnail.py paper.pdf --page 2 --rect 70 71 517 260 images/publications/air.webp

From a whole PDF page (e.g. a compiled TikZ drawing in images/publications/tikz/):
    python3 tools/make_thumbnail.py build/tame.pdf images/publications/tame.webp

From an existing figure image (PNG/JPG):
    python3 tools/make_thumbnail.py figure.png images/publications/tame.webp

The figure is scaled to fit inside a white 16:10 canvas with a small margin.
Requires Pillow, plus PyMuPDF (`pip install pymupdf`) for PDF input.
"""

import argparse
import io

from PIL import Image

WIDTH, HEIGHT, MARGIN = 640, 400, 14


def render_pdf_region(path, page_number, rect):
    import pymupdf

    page = pymupdf.open(path)[page_number - 1]
    clip = pymupdf.Rect(*rect) if rect else page.rect
    # Render well above the target size, then downsample for crisp lines and text.
    zoom = max(4.0, 3 * WIDTH / clip.width)
    pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
    return Image.open(io.BytesIO(pixmap.tobytes("png")))


def make_thumbnail(figure, output):
    figure = figure.convert("RGBA")
    figure.thumbnail((WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN), Image.LANCZOS)
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "white")
    canvas.alpha_composite(figure, ((WIDTH - figure.width) // 2, (HEIGHT - figure.height) // 2))
    canvas.convert("RGB").save(output, "WEBP", quality=88, method=6)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="PDF file or figure image")
    parser.add_argument("output", help="Destination .webp path")
    parser.add_argument("--page", type=int, default=1, help="1-based PDF page number (default 1)")
    parser.add_argument("--rect", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"),
                        help="PDF region to crop, in points (default: the whole page)")
    args = parser.parse_args()
    if args.source.lower().endswith(".pdf"):
        figure = render_pdf_region(args.source, args.page, args.rect)
    else:
        figure = Image.open(args.source)
    make_thumbnail(figure, args.output)
    print("Wrote", args.output)


if __name__ == "__main__":
    main()
