# Rita Ovari – coaching website

Bilingual (HU default at `/`, EN at `/en/`) static site for Rita Ovari, coach & trainer. Built on the
"living sprint board" design system (Paper + Deep dive themes, Bricolage Grotesque / Instrument Serif / Geist).

## Build
```
python3 build.py                 # writes site/
python3 build.py --preview x.html  # single-file preview with an in-page HU/EN switch
```
Edit copy in `src/content.py`, styles in `src/styles.css`. Deploy the `site/` folder to any static host
(Netlify, Vercel, Cloudflare Pages, cPanel).

## SEO included
- Separate URLs per language with `hreflang` (hu, en, x-default), canonical, meta description, Open Graph/Twitter tags, `og-image.jpg`
- JSON-LD: WebSite, Person, ProfessionalService (with service catalogue, Budapest/Hungary, languages), FAQPage
- `sitemap.xml` with language alternates, `robots.txt`; semantic HTML, one `h1` per page, no JS needed to read content

## Before launch (edit the CONFIG block in `build.py`)
- `DOMAIN`: final domain (all canonical/hreflang/sitemap URLs use it)
- `EMAIL`: Rita's real address (placeholder now)
- `FORM_ENDPOINT`: e.g. a Formspree form ID; until set, the form shows a preview message
- Replace the illustrated portrait with real photos (hero + About section), add a privacy page
- Confirm certificates, add real testimonials and client logos (with permission)
