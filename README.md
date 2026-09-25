# Accurate Weighing Systems — Website (HTML + Tailwind CSS)

Static, multi-page website for Accurate Weighing Systems, Ludhiana. Content comes from the IndiaMart profile; the layout follows the Essae pattern (hero slider, product verticals, featured products, industries, enquiry-first product cards).

## Pages (58)
| Page | File |
|---|---|
| Home | `index.html` |
| About (story, fact sheet, mission, certifications) | `about.html` |
| All products (filters: category, brand, industry; sort by price) | `products.html` |
| 8 category pages | `category/*.html` |
| 41 product detail pages (specs, price, FAQs, similar products, schema) | `product/*.html` |
| Industries (8 industries with recommended ranges) | `industries.html` |
| Services (installation, calibration, AMC, ERP integration, service form) | `services.html` |
| Brands (Essae, CAS, DIGI, Tula/Swift) | `brands.html` |
| Downloads (brochures) | `downloads.html` |
| Contact (form, map, business details) | `contact.html` |
| 404, `sitemap.xml`, `robots.txt` | |

## Features
- Mega menu, industries dropdown, mobile drawer, sticky header
- Auto-playing hero slider, animated stat counters, featured-product tabs
- Site-wide product search (`assets/js/products-data.js`)
- "Send enquiry" modal on every product; all forms open WhatsApp with the enquiry pre-filled
- Floating WhatsApp / call buttons
- SEO: unique titles and descriptions, canonical URLs, Store, Product and FAQPage JSON-LD, sitemap

## Editing
All content lives in **`data.py`** (company details, categories, industries, services, products, FAQs).

```bash
npm install          # once
npm run build        # regenerates all HTML from data.py + compiles Tailwind → assets/css/app.css
npm run dev          # watch mode for CSS while tweaking classes
```

Design tokens (colours, fonts) are in `src/input.css` under `@theme`.

## Before launch — checklist
1. **Contact details** in `data.py`: the phone number is IndiaMart's routed number. Replace it with the direct mobile/WhatsApp number, and replace the placeholder email and full address.
2. **Domain**: set `SITE_URL` in `build.py`.
3. **Logo**: replace the logo block in `logo()` in `build.py` with the real logo file.
4. **Product images** are loaded from IndiaMart's CDN (500px, falling back to 125px, then a placeholder). Download them into `assets/img/products/` and point `img` at local files. Products marked "Photo coming soon" need photos.
5. **Brochures**: place PDFs in `assets/brochures/` and update the links in `downloads_page()`.
6. **FAQ, warranty and service wording**: confirm with the client.
7. **Brand usage**: only show manufacturer logos or photos with dealer permission.
8. **Forms** currently send to WhatsApp. To also email or store leads, post the forms to a small PHP or Laravel endpoint and remove `data-wa-form`.
