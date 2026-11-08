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
as a file. Its content, publication links, and news disclosure do not require
JavaScript. JavaScript adds a persistent theme preference and mobile navigation.

## Update content

- Edit the biography, contact links, news, and talks in `index.html`.
- Edit papers in `publications.json`, then run
  `python3 tools/render_publications.py`. Entries with `selected: 1` appear
  on the homepage in their JSON order. The renderer keeps paper content in the
  delivered HTML so it remains accessible without a network request or JavaScript.
- Each paper can have `badge`, `badge_detail`, and `award` fields. Supported
  resource links are `pdf`, `code`, `project`, `poster`, and `slides`.
- Replace `images/profile.jpg` to update the portrait. The existing `resume.pdf`
  belongs to the previous template's author and is intentionally not linked;
  replace it with your own résumé before adding a résumé link.
- Adjust the theme and responsive layout in `styles.css`. Theme initialization
  lives in `theme.js`; navigation and theme controls live in `scripts.js`.
- `index_new.html` and `index_backup.html` redirect old bookmarks to the homepage.

Before committing publication changes:

```sh
python3 tools/render_publications.py --check
git diff --check
```

Push to `main` to deploy through the existing GitHub Pages configuration.

## Credits

The layout follows the typography, profile placement, news rows, and publication
badges of Jonas Hübotter's al-folio site. The al-folio MIT license is retained in
`assets/licenses/al-folio.txt`. Roboto is served locally; its SIL Open Font
License is in `assets/fonts/OFL.txt`. The repository's existing MIT license is
preserved in `LICENSE`.
