# Guangyuan Wang's academic website

Static academic homepage at [al2wang.github.io](https://al2wang.github.io/),
with a design adapted from [Jonas Hübotter's website](https://jonhue.github.io/)
and [al-folio](https://github.com/alshedivat/al-folio).

The site uses plain HTML, CSS, and JavaScript. GitHub Pages serves the root of
the `main` branch; no package installation or framework build is required.

## Preview

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. The homepage also works when opened directly
as a file. Its content does not require JavaScript; JavaScript adds a persistent
theme preference.

## Update content

- The homepage currently shows only the name, one introductory sentence, and a
  cartoon placeholder portrait. Edit the sentence in `index.html`; keep the
  description and Open Graph description in sync.
- News, publications, talks, additional biography, and contact links are omitted.
  Existing PDFs and `publications.json` remain available for future updates.
- `tools/render_publications.py` is inactive while the homepage has no publication
  markers. To restore publications, add the previous publication section with its
  `PUBLICATIONS:START` / `PUBLICATIONS:END` markers, then run the renderer.
- The displayed portrait is `images/profile-placeholder.png`; the original photo
  is retained as `images/profile.jpg`. The existing `resume.pdf`
  belongs to the previous template's author and is intentionally not linked;
  replace it with your own résumé before adding a résumé link.
- Adjust the theme and responsive layout in `styles.css`. Theme initialization
  lives in `theme.js`; theme controls live in `scripts.js`.
- `index_new.html` and `index_backup.html` redirect old bookmarks to the homepage.

Before committing changes:

```sh
python3 tools/render_publications.py --check
git diff --check
```

Push to `main` to deploy through the existing GitHub Pages configuration.

## Credits

The typography and portrait layout follow Jonas Hübotter's al-folio site.
The al-folio MIT license is retained in
`assets/licenses/al-folio.txt`. Roboto is served locally; its SIL Open Font
License is in `assets/fonts/OFL.txt`. The repository's existing MIT license is
preserved in `LICENSE`.

## Placeholder portrait

Saved asset: `images/profile-placeholder.png`. Generated with the built-in
imagegen tool, using `images/profile.jpg` as the reference. The original photo
is unchanged.

Generation prompt:

> Transform the reference portrait into a simple, friendly 2D cartoon avatar for an academic website. Preserve the person's recognizable dark side-swept hair, rectangular glasses, face shape, and light gray shirt. Use clean linework, soft flat colors, a subtle smile, and a plain warm off-white background. Center a head-and-shoulders portrait in a square crop. Remove earbud wires. No text, logos, props, or watermark.
