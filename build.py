"""Static site generator for Accurate Weighing Systems.

    python3 build.py        # writes every .html page, sitemap and product data
    npm run build           # compiles Tailwind into assets/css/app.css

All content comes from data.py; shared layout (top bar, mega menu, footer,
enquiry modal) lives here so every page stays consistent.
"""
import json
import os
from html import escape as e

from data import (BRANDS, CATEGORIES, COMPANY, FAQS, INDUSTRIES, ON_REQUEST,
                  PRODUCTS, SERVICES, WHY_US)

OUT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://www.accurateweighing.in"  # TODO: set the real domain
C = COMPANY
CAT = {c[0]: c for c in CATEGORIES}
IND = {i[0]: i for i in INDUSTRIES}

# ------------------------------------------------------------------ icons
ICONS = {
    "store": '<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M5 13v7h14v-7"/><path d="M10 20v-4h4v4"/>',
    "printer": '<path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/>',
    "platform": '<rect x="3" y="15" width="18" height="4" rx="1"/><path d="M12 15V8"/><rect x="7" y="4" width="10" height="4" rx="1"/><path d="M5 19v2M19 19v2"/>',
    "factory": '<path d="M2 20V9l6 4V9l6 4V4h8v16z"/><path d="M6 17h2M11 17h2M16 17h2"/>',
    "crane": '<path d="M4 21V5l14-2v2"/><path d="M4 5h16"/><path d="M18 5v6"/><rect x="15" y="11" width="6" height="5" rx="1"/><path d="M2 21h8"/>',
    "flask": '<path d="M9 3h6"/><path d="M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7 15h10"/>',
    "gem": '<path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M12 21 8 9l4-6 4 6z"/>',
    "cpu": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "truck": '<path d="M1 6h13v10H1z"/><path d="M14 10h4l4 4v2h-8"/><circle cx="5.5" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
    "droplet": '<path d="M12 3s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/>',
    "monitor": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "beaker": '<path d="M5 3h14M6 3v15a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V3"/><path d="M6 13h12"/>',
    "wheat": '<path d="M12 22V8"/><path d="M12 8c-3 0-4-2-4-5 3 0 4 2 4 5zM12 8c3 0 4-2 4-5-3 0-4 2-4 5z"/><path d="M12 14c-3 0-4-2-4-5 3 0 4 2 4 5zM12 14c3 0 4-2 4-5-3 0-4 2-4 5z"/>',
    "shirt": '<path d="M8 3 3 6l2 5 3-1v11h8V10l3 1 2-5-5-3a4 4 0 0 1-8 0z"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.3-1.3a4 4 0 0 0-5-5l2.6 2.6-2.8 2.8z"/><path d="M3 21l6-6"/>',
    "badge": '<circle cx="12" cy="9" r="6"/><path d="M9 14.5 8 22l4-2 4 2-1-7.5"/><path d="m9.5 9 1.8 1.8L14.5 7.5"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "arrow": '<path d="M5 12h14M13 5l7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
    "filter": '<path d="M22 3H2l8 9.5V19l4 2v-8.5z"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
}
WA_SVG = '<svg viewBox="0 0 24 24" class="{cls}" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-2.4-1.5 9 9 0 0 1-1.7-2.1c-.2-.3 0-.5.1-.6l.5-.6.3-.5v-.5c0-.1-.7-1.6-.9-2.2s-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c.7.3 1.3.5 1.7.6a4.2 4.2 0 0 0 1.9.1 3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.3zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4a9.8 9.8 0 1 1 8.3 4.6zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.9L.1 24l6.3-1.6a11.8 11.8 0 0 0 5.6 1.4 11.8 11.8 0 0 0 8.4-20.2z"/></svg>'


def icon(name, cls="h-5 w-5"):
    return (f'<svg viewBox="0 0 24 24" class="{cls}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def wa_icon(cls="h-5 w-5"):
    return WA_SVG.format(cls=cls)


# ------------------------------------------------------------------ helpers
def inr(n):
    if n is None:
        return None
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


def big_img(url):
    if not url:
        return None
    a, b = url.rsplit("-125x125", 1)
    return a + "-500x500" + b


def img(p, root, cls="h-full w-full object-contain p-6 product-img", eager=False):
    if not p["img"]:
        return (f'<img src="{root}assets/img/scale-placeholder.svg" alt="{e(p["name"])}" class="{cls}" '
                f'loading="lazy" width="400" height="400">')
    return (f'<img src="{big_img(p["img"])}" data-fb="{p["img"]}" onerror="imgFallback(this)" '
            f'alt="{e(p["name"])}" class="{cls}" loading="{"eager" if eager else "lazy"}" width="500" height="500">')


def products_in(cat):
    return [p for p in PRODUCTS if p["cat"] == cat]


def price_html(p, size="text-lg"):
    if p["price"] is None:
        return f'<span class="{size} font-extrabold text-ink">Price on request</span>'
    return (f'<span class="{size} font-extrabold text-ink">₹{inr(p["price"])}</span>'
            f'<span class="text-xs text-ink-soft"> / {p["unit"]}</span>')


def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{C['whatsapp']}?text={quote(text)}"


def breadcrumb(root, items):
    out = [f'<a href="{root}index.html" class="hover:text-white">Home</a>']
    for label, href in items:
        out.append(icon("right", "h-3.5 w-3.5 opacity-60"))
        out.append(f'<a href="{href}" class="hover:text-white">{e(label)}</a>' if href
                   else f'<span class="text-white">{e(label)}</span>')
    return f'<nav class="flex flex-wrap items-center gap-2 text-sm text-white/60" aria-label="Breadcrumb">{"".join(out)}</nav>'


def page_hero(root, eyebrow, title, text, crumbs, extra=""):
    return f"""
<section class="relative overflow-hidden bg-navy-900 text-white">
  <div class="grid-pattern absolute inset-0"></div>
  <div class="absolute -right-24 -top-24 h-80 w-80 rounded-full bg-brand-500/30 blur-3xl"></div>
  <div class="container-x relative py-14 md:py-20">
    {breadcrumb(root, crumbs)}
    <p class="mt-6 text-xs font-bold uppercase tracking-[0.2em] text-accent-400">{e(eyebrow)}</p>
    <h1 class="mt-3 max-w-3xl text-3xl font-extrabold text-white md:text-5xl">{title}</h1>
    <p class="mt-4 max-w-2xl text-white/75 md:text-lg">{text}</p>
    {extra}
  </div>
</section>"""


def section_head(eyebrow, title, text="", center=False, action=""):
    align = "mx-auto text-center items-center" if center else ""
    wrap = "flex flex-col gap-6 md:flex-row md:items-end md:justify-between" if action and not center else ""
    return f"""<div class="{wrap}"><div class="flex max-w-2xl flex-col {align}">
  <span class="eyebrow">{e(eyebrow)}</span><h2 class="h2">{title}</h2>
  {f'<p class="lead">{text}</p>' if text else ''}</div>{action}</div>"""


# ------------------------------------------------------------------ cards
def product_card(p, root, order=0, extra_attrs=""):
    c = CAT[p["cat"]]
    tags = "".join(f'<span class="chip">{e(IND[i][1].split(" &")[0])}</span>' for i in p["industries"][:3])
    badge = f'<span class="badge badge-{p["badge"]}">{p["badge"]}</span>' if p["badge"] else ""
    return f"""
<article data-product data-cat="{p['cat']}" data-brand="{e(p['brand'])}" data-ind="{','.join(p['industries'])}"
  data-price="{p['price'] or ''}" data-order="{order}" data-badge="{p['badge'] or 'none'}" {extra_attrs}
  class="group card relative flex flex-col overflow-hidden transition hover:-translate-y-1 hover:border-brand-200 hover:shadow-xl hover:shadow-navy-900/5">
  {badge}
  <a href="{root}product/{p['slug']}.html" class="relative block aspect-square bg-surface">
    {img(p, root)}
  </a>
  <div class="flex flex-1 flex-col p-5">
    <p class="text-xs font-semibold uppercase tracking-wider text-brand-600">{e(p['brand'])} · {e(c[1])}</p>
    <h3 class="mt-1.5 text-[17px] font-bold leading-snug"><a href="{root}product/{p['slug']}.html" class="hover:text-brand-600">{e(p['name'])}</a></h3>
    <div class="mt-3 flex flex-wrap gap-1.5">{tags}</div>
    <div class="mt-auto pt-4">{price_html(p)}</div>
    <div class="mt-4 grid grid-cols-2 gap-2">
      <button type="button" data-enquire="{e(p['name'])}" class="btn btn-primary px-3 py-2.5 text-[13px]">Send enquiry</button>
      <a href="{root}product/{p['slug']}.html" class="btn btn-outline px-3 py-2.5 text-[13px]">View product</a>
    </div>
  </div>
</article>"""


def category_card(c, root):
    slug, name, desc, ic = c
    n = len(products_in(slug))
    return f"""
<a href="{root}category/{slug}.html" class="group card relative flex flex-col overflow-hidden p-6 transition hover:-translate-y-1 hover:border-brand-300 hover:shadow-xl hover:shadow-navy-900/5">
  <span class="grid h-14 w-14 place-items-center rounded-2xl bg-brand-50 text-brand-600 transition group-hover:bg-brand-600 group-hover:text-white">{icon(ic, 'h-7 w-7')}</span>
  <h3 class="mt-5 text-lg font-bold">{e(name)}</h3>
  <p class="mt-2 text-sm leading-relaxed text-ink-soft">{e(desc)}</p>
  <span class="mt-5 flex items-center justify-between border-t border-line pt-4 text-sm font-semibold">
    <span class="text-ink-soft">{n} product{'s' if n != 1 else ''}</span>
    <span class="flex items-center gap-1 text-brand-600">Explore {icon('arrow', 'h-4 w-4 transition group-hover:translate-x-1')}</span>
  </span>
</a>"""


def faq_block(items):
    return "".join(f"""
<details class="group card px-6 py-5 open:border-brand-200 open:shadow-sm">
  <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-semibold">{e(q)}
    <span class="faq-icon grid h-8 w-8 shrink-0 place-items-center rounded-full bg-surface text-lg text-brand-600 transition">+</span></summary>
  <p class="mt-3 text-sm leading-relaxed text-ink-soft">{e(a)}</p>
</details>""" for q, a in items)


def cta_band(root, title="Not sure which scale you need?", text="Tell us what you weigh, how much and how often. We'll recommend the right model and share the best price — usually within an hour."):
    return f"""
<section class="container-x pb-20">
  <div class="relative overflow-hidden rounded-3xl bg-brand-700 px-6 py-12 text-white md:px-14 md:py-14">
    <div class="grid-pattern absolute inset-0 opacity-60"></div>
    <div class="absolute -bottom-20 -right-10 h-72 w-72 rounded-full bg-accent-500/25 blur-3xl"></div>
    <div class="relative grid items-center gap-8 lg:grid-cols-[1.4fr_1fr]">
      <div><h2 class="text-3xl font-extrabold text-white md:text-4xl">{title}</h2>
        <p class="mt-3 max-w-xl text-white/80">{text}</p></div>
      <div class="flex flex-wrap gap-3 lg:justify-end">
        <button type="button" data-enquire="" class="btn btn-accent">{icon('tag', 'h-4 w-4')} Get a quote</button>
        <a href="{wa_link('Hi, I need help choosing a weighing scale.')}" target="_blank" rel="noopener" class="btn btn-wa">{wa_icon('h-4 w-4')} WhatsApp us</a>
        <a href="tel:+{C['phone_raw']}" class="btn btn-ghost-light">{icon('phone', 'h-4 w-4')} {C['phone']}</a>
      </div>
    </div>
  </div>
</section>"""


# ------------------------------------------------------------------ layout
NAV = [("index.html", "Home"), ("about.html", "About"), ("products.html", "Products"),
       ("industries.html", "Industries"), ("services.html", "Services"), ("brands.html", "Brands"),
       ("downloads.html", "Downloads"), ("contact.html", "Contact")]


def logo(root, light=False):
    txt = "text-white" if light else "text-ink"
    sub = "text-white/60" if light else "text-ink-soft"
    img = "light-logo.png" if light else "dark-logo.png"
    return f"""<a href="{root}index.html" class="flex items-center gap-3" aria-label="{C['name']} home">
  <img src="{root}assets/img/{img}" alt="{C['name']}" class="h-11 w-11 rounded-xl object-cover shadow-md shadow-brand-600/30">
  <span class="leading-none"><span class="block font-display text-lg font-extrabold {txt}">Accurate</span>
  <span class="block text-[11px] font-semibold uppercase tracking-[0.22em] {sub}">Weighing Systems</span></span>
</a>"""


def mega_menu(root):
    cols = "".join(f"""
<a href="{root}category/{s}.html" class="group flex gap-3 rounded-xl p-3 hover:bg-surface">
  <span class="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-600 group-hover:bg-brand-600 group-hover:text-white">{icon(ic)}</span>
  <span><span class="block text-sm font-bold text-ink">{e(n)}</span><span class="mt-0.5 block text-xs leading-snug text-ink-soft">{e(d)}</span></span>
</a>""" for s, n, d, ic in CATEGORIES)
    req = "".join(f'<li class="flex items-center gap-2 py-1 text-sm text-ink-soft">{icon(ic, "h-4 w-4 text-brand-500")}{e(n)}</li>' for n, _, ic in ON_REQUEST)
    return f"""
<div class="mega absolute inset-x-0 top-full z-40 pt-3">
  <div class="container-x"><div class="grid grid-cols-[1fr_280px] overflow-hidden rounded-2xl border border-line bg-white shadow-2xl shadow-navy-900/10">
    <div class="grid grid-cols-2 gap-1 p-5 xl:grid-cols-3">{cols}</div>
    <div class="bg-navy-900 p-6 text-white">
      <p class="text-xs font-bold uppercase tracking-widest text-accent-400">Also available on request</p>
      <ul class="mt-3 [&_li]:text-white/75 [&_svg]:text-brand-300">{req}</ul>
      <a href="{root}products.html" class="btn btn-accent mt-6 w-full">View all products {icon('arrow', 'h-4 w-4')}</a>
    </div>
  </div></div>
</div>"""


def industries_menu(root):
    items = "".join(f'<a href="{root}industries.html#{s}" class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold hover:bg-surface hover:text-brand-600">{icon(ic, "h-4 w-4 text-brand-500")}{e(n)}</a>'
                    for s, n, _, ic, _ in INDUSTRIES)
    return f'<div class="mega absolute left-0 top-full z-40 w-72 pt-3"><div class="rounded-2xl border border-line bg-white p-2 shadow-2xl shadow-navy-900/10">{items}</div></div>'


def header(root, active):
    links = []
    for href, label in NAV[1:-1]:
        cls = "nav-link is-active" if href == active else "nav-link"
        if label == "Products":
            links.append(f'<li class="has-mega static"><a href="{root}{href}" class="{cls}">{label}{icon("down", "h-4 w-4")}</a>{mega_menu(root)}</li>')
        elif label == "Industries":
            links.append(f'<li class="has-mega relative"><a href="{root}{href}" class="{cls}">{label}{icon("down", "h-4 w-4")}</a>{industries_menu(root)}</li>')
        else:
            links.append(f'<li><a href="{root}{href}" class="{cls}">{label}</a></li>')
    mobile = "".join(f'<a href="{root}{h}" class="block rounded-xl px-4 py-3 text-lg font-semibold {"bg-brand-50 text-brand-700" if h == active else "hover:bg-surface"}">{l}</a>' for h, l in NAV)
    mcats = "".join(f'<a href="{root}category/{s}.html" class="flex items-center gap-2 rounded-lg px-4 py-2 text-sm text-ink-soft hover:bg-surface">{icon(ic, "h-4 w-4 text-brand-500")}{e(n)}</a>' for s, n, _, ic in CATEGORIES)
    return f"""
<div class="hidden bg-navy-950 text-[13px] text-white/75 md:block">
  <div class="container-x flex h-10 items-center justify-between">
    <div class="flex items-center gap-6">
      <span class="flex items-center gap-2">{icon('pin', 'h-4 w-4 text-accent-400')}{C['city']}</span>
      <span class="flex items-center gap-2">{icon('clock', 'h-4 w-4 text-accent-400')}{C['hours']}</span>
    </div>
    <div class="flex items-center gap-6">
      <a href="mailto:{C['email']}" class="flex items-center gap-2 hover:text-white">{icon('mail', 'h-4 w-4 text-accent-400')}{C['email']}</a>
      <a href="tel:+{C['phone_raw']}" class="flex items-center gap-2 hover:text-white">{icon('phone', 'h-4 w-4 text-accent-400')}{C['phone']}</a>
      <span class="rounded-full bg-white/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-white">Authorised multi-brand dealer</span>
    </div>
  </div>
</div>
<header id="site-header" class="sticky top-0 z-50 border-b border-line bg-white/95 backdrop-blur transition-shadow">
  <div class="container-x relative flex h-20 items-center justify-between gap-4">
    {logo(root)}
    <nav class="hidden lg:block" aria-label="Main"><ul class="flex items-center gap-1">{''.join(links)}</ul></nav>
    <div class="flex items-center gap-2">
      <button type="button" data-search-open class="grid h-11 w-11 place-items-center rounded-full border border-line text-ink hover:border-brand-500 hover:text-brand-600" aria-label="Search products">{icon('search')}</button>
      <a href="{root}contact.html" class="btn btn-outline hidden xl:inline-flex {'border-brand-500 text-brand-700' if active == 'contact.html' else ''}">Contact</a>
      <button type="button" data-enquire="" class="btn btn-primary hidden sm:inline-flex">Get Quote</button>
      <button type="button" data-menu-open class="grid h-11 w-11 place-items-center rounded-full bg-navy-900 text-white lg:hidden" aria-label="Open menu">{icon('menu')}</button>
    </div>
  </div>
</header>
<div id="mobile-menu" class="fixed inset-0 z-[60] hidden">
  <div class="absolute inset-0 bg-navy-950/60" data-menu-close></div>
  <div class="absolute inset-y-0 right-0 flex w-[88%] max-w-sm flex-col overflow-y-auto bg-white p-5">
    <div class="flex items-center justify-between">{logo(root)}<button type="button" data-menu-close class="grid h-10 w-10 place-items-center rounded-full bg-surface" aria-label="Close menu">{icon('x')}</button></div>
    <nav class="mt-6 space-y-1">{mobile}</nav>
    <p class="mt-6 px-4 text-xs font-bold uppercase tracking-widest text-ink-soft">Product ranges</p>
    <div class="mt-2">{mcats}</div>
    <div class="mt-auto grid gap-2 pt-6">
      <button type="button" data-enquire="" data-menu-close class="btn btn-primary">Get Quote</button>
      <a href="tel:+{C['phone_raw']}" class="btn btn-outline">{icon('phone', 'h-4 w-4')} {C['phone']}</a>
    </div>
  </div>
</div>"""


def footer(root):
    cats = "".join(f'<li><a href="{root}category/{s}.html" class="hover:text-white">{e(n)}</a></li>' for s, n, _, _ in CATEGORIES)
    inds = "".join(f'<li><a href="{root}industries.html#{s}" class="hover:text-white">{e(n)}</a></li>' for s, n, *_ in INDUSTRIES[:6])
    comp = "".join(f'<li><a href="{root}{h}" class="hover:text-white">{l}</a></li>' for h, l in NAV[1:])
    return f"""
<footer class="bg-navy-950 text-white/65">
  <div class="container-x grid gap-12 py-16 md:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
    <div>
      {logo(root, light=True)}
      <p class="mt-5 max-w-sm text-sm leading-relaxed">Trader, wholesaler and distributor of electronic weighing scales, balances and systems in {C['city']} since {C['founded']}. Sales, calibration, service and ERP integration.</p>
      <ul class="mt-6 space-y-3 text-sm">
        <li class="flex gap-3">{icon('pin', 'h-5 w-5 shrink-0 text-accent-400')}{C['address']}</li>
        <li><a href="tel:+{C['phone_raw']}" class="flex gap-3 hover:text-white">{icon('phone', 'h-5 w-5 shrink-0 text-accent-400')}{C['phone']}</a></li>
        <li><a href="mailto:{C['email']}" class="flex gap-3 hover:text-white">{icon('mail', 'h-5 w-5 shrink-0 text-accent-400')}{C['email']}</a></li>
      </ul>
    </div>
    <div><h4 class="font-display text-sm font-bold uppercase tracking-widest text-white">Products</h4><ul class="mt-5 space-y-2.5 text-sm">{cats}</ul></div>
    <div><h4 class="font-display text-sm font-bold uppercase tracking-widest text-white">Industries</h4><ul class="mt-5 space-y-2.5 text-sm">{inds}</ul></div>
    <div><h4 class="font-display text-sm font-bold uppercase tracking-widest text-white">Company</h4><ul class="mt-5 space-y-2.5 text-sm">{comp}
      <li><a href="{C['indiamart']}" target="_blank" rel="noopener" class="hover:text-white">IndiaMart profile ↗</a></li></ul></div>
  </div>
  <div class="border-t border-white/10">
    <div class="container-x flex flex-col gap-3 py-6 text-xs md:flex-row md:items-center md:justify-between">
      <p>© <span data-year></span> {C['name']}. All rights reserved. · GST {C['gst']} · {C['udyam']}</p>
      <p>Designed &amp; developed by <a href="https://rewirenext.com" target="_blank" rel="noopener" class="hover:text-white">Rewire Next Innovations</a></p>
    </div>
  </div>
</footer>"""


def overlays(root):
    cats = "".join(f'<option>{e(n)}</option>' for _, n, _, _ in CATEGORIES)
    return f"""
<!-- Floating actions -->
<div class="fixed bottom-5 right-5 z-40 flex flex-col gap-3">
  <a href="{wa_link('Hi, I found you on your website and want to enquire about a weighing scale.')}" target="_blank" rel="noopener" class="grid h-14 w-14 place-items-center rounded-full bg-[#25d366] text-white shadow-xl shadow-black/20 transition hover:scale-105" aria-label="Chat on WhatsApp">{wa_icon('h-7 w-7')}</a>
  <a href="tel:+{C['phone_raw']}" class="grid h-14 w-14 place-items-center rounded-full bg-brand-600 text-white shadow-xl shadow-black/20 transition hover:scale-105 md:hidden" aria-label="Call us">{icon('phone', 'h-6 w-6')}</a>
</div>

<!-- Search -->
<div id="search-overlay" class="fixed inset-0 z-[70] hidden bg-navy-950/70 p-4 backdrop-blur-sm">
  <div class="mx-auto mt-16 max-w-2xl rounded-2xl bg-white p-4 shadow-2xl">
    <div class="flex items-center gap-3 border-b border-line px-2 pb-3">
      {icon('search', 'h-5 w-5 text-ink-soft')}
      <input id="search-input" type="search" placeholder="Search by model, brand or type — e.g. DS-215, gold, crane" class="w-full bg-transparent py-2 text-base outline-none" autocomplete="off">
      <button type="button" data-search-close class="grid h-9 w-9 place-items-center rounded-full bg-surface" aria-label="Close search">{icon('x', 'h-4 w-4')}</button>
    </div>
    <div id="search-results" class="max-h-[60vh] overflow-y-auto pt-2"></div>
  </div>
</div>

<!-- Enquiry modal -->
<div id="enquiry-modal" class="fixed inset-0 z-[80] hidden place-items-center bg-navy-950/70 p-4 backdrop-blur-sm [&:not(.hidden)]:grid" role="dialog" aria-modal="true" aria-labelledby="enq-title">
  <div class="w-full max-w-lg overflow-hidden rounded-3xl bg-white shadow-2xl">
    <div class="relative bg-navy-900 px-6 py-6 text-white">
      <div class="grid-pattern absolute inset-0"></div>
      <div class="relative flex items-start justify-between gap-4">
        <div><h3 id="enq-title" class="text-xl font-extrabold text-white">Request a quote</h3><p id="enq-sub" class="mt-1 text-sm text-white/70"></p></div>
        <button type="button" data-modal-close class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white/10 hover:bg-white/20" aria-label="Close">{icon('x', 'h-4 w-4')}</button>
      </div>
    </div>
    <form data-wa-form="Quote request" class="grid gap-4 p-6">
      <input type="hidden" id="enq-product" name="Product">
      <div class="grid gap-4 sm:grid-cols-2">
        <div><label class="label" for="enq-name">Your name *</label><input id="enq-name" name="Name" required class="field" placeholder="Full name"></div>
        <div><label class="label" for="enq-phone">Mobile *</label><input id="enq-phone" name="Mobile" required type="tel" pattern="[0-9+ ]{{10,14}}" class="field" placeholder="10-digit mobile"></div>
      </div>
      <div class="grid gap-4 sm:grid-cols-2">
        <div><label class="label" for="enq-city">City</label><input id="enq-city" name="City" class="field" placeholder="e.g. Ludhiana"></div>
        <div><label class="label" for="enq-qty">Quantity</label><input id="enq-qty" name="Quantity" type="number" min="1" class="field" placeholder="1"></div>
      </div>
      <div><label class="label" for="enq-msg">Requirement</label><textarea id="enq-msg" name="Requirement" rows="3" class="field" placeholder="Capacity, accuracy, where it will be used…"></textarea></div>
      <button class="btn btn-primary w-full py-3.5">{wa_icon('h-4 w-4')} Send enquiry on WhatsApp</button>
      <p data-form-ok class="hidden rounded-xl bg-brand-50 p-3 text-center text-sm font-medium text-brand-700">Thanks! WhatsApp has opened with your enquiry — just press send.</p>
      <p class="text-center text-xs text-ink-soft">Or call <a href="tel:+{C['phone_raw']}" class="font-semibold text-brand-600">{C['phone']}</a></p>
    </form>
  </div>
</div>"""


def layout(title, desc, body, root="", active="", schema=None, path="index.html"):
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}/{path}">
<meta name="theme-color" content="#0a1a2f">
<link rel="icon" href="{root}assets/img/favicon.ico" sizes="any">
<link rel="icon" href="{root}assets/img/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="icon" href="{root}assets/img/favicon-16x16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{root}assets/img/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/app.css">
<script>function imgFallback(el){{var l=(el.dataset.fb||"").split("|").filter(Boolean);if(l.length){{el.src=l.shift();el.dataset.fb=l.join("|")}}else{{el.onerror=null;el.src="{root}assets/img/scale-placeholder.svg"}}}}</script>
{ld}</head>
<body data-root="{root}" data-wa="{C['whatsapp']}">
<a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[90] focus:rounded-lg focus:bg-white focus:px-4 focus:py-2">Skip to content</a>
{header(root, active)}
<main id="main">
{body}
</main>
{footer(root)}
{overlays(root)}
<script src="{root}assets/js/products-data.js"></script>
<script src="{root}assets/js/main.js"></script>
</body>
</html>"""


def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


# ------------------------------------------------------------------ schema
def org_schema():
    return {
        "@context": "https://schema.org", "@type": "Store",
        "name": C["name"], "url": SITE_URL, "telephone": C["phone"], "email": C["email"],
        "foundingDate": str(C["founded"]),
        "founder": {"@type": "Person", "name": C["owner"]},
        "address": {"@type": "PostalAddress", "addressLocality": "Ludhiana", "addressRegion": "Punjab", "addressCountry": "IN"},
        "areaServed": "Punjab, India", "paymentAccepted": C["payment"],
        "brand": [b["name"] for b in BRANDS],
    }


# ------------------------------------------------------------------ pages
def home():
    root = ""
    slides = [
        ("Retail & printing scales", "Weigh, bill and print — <span class='text-accent-400'>in one step.</span>",
         "Essae receipt-printing, price-computing and counter scales for sweet shops, kirana and supermarkets across Punjab.",
         "essae-ds-252pr-receipt-printing", "category/retail-scales.html"),
        ("Industrial & platform scales", "Built for the <span class='text-accent-400'>factory floor.</span>",
         "Heavy-duty platform, counting and crane scales from 30 kg to 20 ton — installed and calibrated at your site.",
         "essae-ds-215hd", "category/platform-scales.html"),
        ("Precision & lab balances", "Milligram accuracy <span class='text-accent-400'>you can audit.</span>",
         "Essae AJ-series tuning-fork balances, wind-shield and gold scales for labs, pharma QC and jewellers.",
         "essae-aj-1200e", "category/precision-balances.html"),
    ]
    pmap = {p["slug"]: p for p in PRODUCTS}
    slide_html = ""
    for k, (eb, h, t, slug, href) in enumerate(slides):
        p = pmap[slug]
        slide_html += f"""
<div class="slide {'is-active' if k == 0 else ''} absolute inset-0">
  <div class="container-x grid h-full items-center gap-8 py-14 lg:grid-cols-[1.15fr_1fr]">
    <div class="slide-copy">
      <p class="inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-accent-400">{eb}</p>
      <h1 class="mt-5 text-4xl font-extrabold leading-[1.08] text-white sm:text-5xl lg:text-6xl">{h}</h1>
      <p class="mt-5 max-w-xl text-base text-white/75 md:text-lg">{t}</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <button type="button" data-enquire="" class="btn btn-accent">Get best price {icon('arrow', 'h-4 w-4')}</button>
        <a href="{href}" class="btn btn-ghost-light">View range</a>
      </div>
    </div>
    <div class="relative hidden lg:block">
      <div class="absolute inset-8 rounded-full bg-brand-500/30 blur-3xl"></div>
      <div class="relative mx-auto aspect-square max-w-md rounded-[2.5rem] bg-white p-6 shadow-2xl shadow-black/40">
        {img(p, root, 'h-full w-full object-contain product-img', eager=(k == 0))}
        <div class="absolute -bottom-5 -left-6 rounded-2xl bg-white px-5 py-4 shadow-xl">
          <p class="text-xs font-semibold uppercase tracking-wider text-brand-600">{e(p['brand'])}</p>
          <p class="font-display text-sm font-extrabold">{e(p['name'])}</p>
          <p class="mt-1 text-sm">{price_html(p, 'text-base')}</p>
        </div>
      </div>
    </div>
  </div>
</div>"""
    dots = "".join(f'<button type="button" data-dot class="h-1.5 w-4 rounded-full bg-white/40 transition-all" aria-label="Slide {k+1}"></button>' for k in range(len(slides)))

    stats = [(C and 2026 - C["founded"], "+", "Years in business"), (len(PRODUCTS), "+", "Models in stock"),
             (len(BRANDS), "", "Trusted brands"), (len(INDUSTRIES), "", "Industries served")]
    stat_html = "".join(f"""<div class="px-6 py-7 text-center md:text-left">
      <p class="font-display text-4xl font-extrabold text-ink"><span data-count="{n}" data-suffix="{s}">{n}{s}</span></p>
      <p class="mt-1 text-sm font-medium text-ink-soft">{l}</p></div>""" for n, s, l in stats)

    featured = [p for p in PRODUCTS if p["badge"]] + [p for p in PRODUCTS if not p["badge"] and p["img"]][:6]
    feat_cards = "".join(product_card(p, root, i) for i, p in enumerate(featured))

    ind_html = "".join(f"""
<a href="industries.html#{s}" class="group relative overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 transition hover:-translate-y-1 hover:bg-white/10">
  <span class="grid h-12 w-12 place-items-center rounded-xl bg-accent-500 text-navy-950">{icon(ic, 'h-6 w-6')}</span>
  <h3 class="mt-5 text-lg font-bold text-white">{e(n)}</h3>
  <p class="mt-2 text-sm leading-relaxed text-white/65">{e(d)}</p>
  <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-accent-400">Solutions {icon('arrow', 'h-4 w-4 transition group-hover:translate-x-1')}</span>
</a>""" for s, n, d, ic, _ in INDUSTRIES)

    svc_html = "".join(f"""
<div class="card p-6"><span class="grid h-12 w-12 place-items-center rounded-xl bg-brand-50 text-brand-600">{icon(ic, 'h-6 w-6')}</span>
  <h3 class="mt-5 text-lg font-bold">{e(n)}</h3><p class="mt-2 text-sm leading-relaxed text-ink-soft">{e(d)}</p></div>""" for n, d, ic in SERVICES)

    why_html = "".join(f"""<li class="flex gap-4"><span class="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-full bg-brand-600 text-white">{icon('check', 'h-4 w-4')}</span>
      <span><span class="block font-bold">{e(t)}</span><span class="mt-1 block text-sm leading-relaxed text-ink-soft">{e(d)}</span></span></li>""" for t, d in WHY_US)

    brand_html = "".join(f"""<a href="brands.html#{b['name'].split()[0].lower()}" class="grid h-24 place-items-center rounded-2xl border border-line bg-white px-6 font-display text-2xl font-extrabold tracking-tight text-navy-700 transition hover:border-brand-400 hover:text-brand-600">{e(b['name'])}</a>""" for b in BRANDS)

    req_html = "".join(f"""<div class="flex items-center gap-4 rounded-2xl border border-dashed border-brand-300 bg-white p-5">
      <span class="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-brand-50 text-brand-600">{icon(ic, 'h-6 w-6')}</span>
      <div class="min-w-0 flex-1"><h3 class="font-bold">{e(n)}</h3><p class="text-sm text-ink-soft">{e(d)}</p></div>
      <button type="button" data-enquire="{e(n)}" class="btn btn-outline shrink-0 px-4 py-2 text-xs">Enquire</button></div>""" for n, d, ic in ON_REQUEST)

    body = f"""
<!-- HERO -->
<section class="relative overflow-hidden bg-navy-900" data-slider>
  <div class="grid-pattern absolute inset-0"></div>
  <div class="absolute -left-40 top-10 h-96 w-96 rounded-full bg-brand-600/40 blur-3xl"></div>
  <div class="relative h-[560px] md:h-[620px]">{slide_html}</div>
  <div class="container-x absolute inset-x-0 bottom-16 flex items-center justify-between">
    <div class="flex items-center gap-2">{dots}</div>
    <div class="flex gap-2">
      <button type="button" data-prev class="grid h-11 w-11 place-items-center rounded-full border border-white/25 text-white hover:bg-white/10" aria-label="Previous slide">{icon('left')}</button>
      <button type="button" data-next class="grid h-11 w-11 place-items-center rounded-full border border-white/25 text-white hover:bg-white/10" aria-label="Next slide">{icon('right')}</button>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="container-x relative z-10 -mt-10">
  <div class="grid grid-cols-2 divide-line rounded-2xl border border-line bg-white shadow-xl shadow-navy-900/5 md:grid-cols-4 md:divide-x [&>*:nth-child(-n+2)]:border-b [&>*:nth-child(-n+2)]:border-line md:[&>*]:border-b-0">{stat_html}</div>
</section>

<!-- ABOUT -->
<section class="section container-x grid items-center gap-12 lg:grid-cols-2">
  <div class="relative">
    <div class="grid grid-cols-2 gap-4">
      <div class="aspect-[4/5] overflow-hidden rounded-3xl bg-surface">{img(pmap['essae-dc-85-counting-scale'], root, 'h-full w-full object-contain p-8 product-img')}</div>
      <div class="mt-12 aspect-[4/5] overflow-hidden rounded-3xl bg-brand-50">{img(pmap['essae-ds-852g-gold-scale'], root, 'h-full w-full object-contain p-8 product-img')}</div>
    </div>
    <div class="absolute -bottom-6 left-6 flex items-center gap-4 rounded-2xl bg-navy-900 px-6 py-5 text-white shadow-2xl">
      <span class="font-display text-5xl font-extrabold text-accent-400">{2026 - C['founded']}</span>
      <span class="text-sm font-semibold leading-tight">Years of trust<br><span class="font-normal text-white/60">Since {C['founded']}, Ludhiana</span></span>
    </div>
  </div>
  <div>
    <span class="eyebrow">About us</span>
    <h2 class="h2">Accurate stands for <span class="text-brand-600">precision you can rely on.</span></h2>
    <p class="lead">Established in {C['founded']} under the guidance of Mr. {C['owner']}, Accurate Weighing Systems trades, wholesales and distributes a complete range of weighing scales, lab balances, moisture analysers, POS systems, jewellery scales and electronic weighbridges.</p>
    <p class="mt-4 leading-relaxed text-ink-soft">Our scales serve pharmaceutical, chemical, jewellery, provision-store and food-processing businesses — and we go beyond the box with calibration, repairs and special indicators that feed weights straight into SAP, ERP and Busy software.</p>
    <div class="mt-8 flex flex-wrap gap-3">
      <a href="about.html" class="btn btn-primary">More about us {icon('arrow', 'h-4 w-4')}</a>
      <a href="{C['indiamart']}" target="_blank" rel="noopener" class="btn btn-outline">See us on IndiaMart ↗</a>
    </div>
  </div>
</section>

<!-- VERTICALS -->
<section class="section bg-surface">
  <div class="container-x">
    {section_head('Product verticals', 'Every kind of scale, <span class="text-brand-600">one trusted dealer.</span>', 'From a ₹6,750 counter scale to a 20-ton crane scale — browse by the job you need done.', action=f'<a href="products.html" class="btn btn-outline">All products {icon("arrow", "h-4 w-4")}</a>')}
    <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{''.join(category_card(c, root) for c in CATEGORIES)}</div>
  </div>
</section>

<!-- FEATURED -->
<section class="section container-x" data-tabs>
  <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
    {section_head('Featured products', 'Popular with our customers', 'A curated pick of proven models — send an enquiry for today’s best price.')}
    <div class="flex gap-2 rounded-full border border-line bg-surface p-1.5">
      <button type="button" data-tab="Trending" class="rounded-full px-4 py-2 text-sm font-semibold transition">Trending</button>
      <button type="button" data-tab="New" class="rounded-full px-4 py-2 text-sm font-semibold transition">New</button>
      <button type="button" data-tab="all" class="rounded-full px-4 py-2 text-sm font-semibold transition">All</button>
    </div>
  </div>
  <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{feat_cards}</div>
</section>

<!-- INDUSTRIES -->
<section class="section relative overflow-hidden bg-navy-900">
  <div class="grid-pattern absolute inset-0"></div>
  <div class="container-x relative">
    <div class="max-w-2xl"><span class="eyebrow text-accent-400">Industries we serve</span>
      <h2 class="h2 text-white">Weighing solutions for <span class="text-accent-400">every trade in Punjab.</span></h2>
      <p class="lead text-white/70">From kirana counters to pharma labs and textile mills — we match the scale to the work.</p></div>
    <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{ind_html}</div>
  </div>
</section>

<!-- SERVICES -->
<section class="section container-x">
  {section_head('Service & support', 'We don’t just sell scales — <span class="text-brand-600">we keep them accurate.</span>', center=True)}
  <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{svc_html}</div>
  <div class="mt-10 text-center"><a href="services.html" class="btn btn-primary">Explore services {icon('arrow', 'h-4 w-4')}</a></div>
</section>

<!-- WHY US -->
<section class="section bg-surface">
  <div class="container-x grid gap-12 lg:grid-cols-[1fr_1.3fr]">
    <div>
      <span class="eyebrow">Why choose us</span>
      <h2 class="h2">The dealer Ludhiana's businesses <span class="text-brand-600">come back to.</span></h2>
      <p class="lead">A rich vendor base, strict quality standards, fair dealings and a client-centric approach have kept our customers with us for over a decade.</p>
      <div class="mt-8 rounded-2xl bg-white p-6 shadow-sm">
        <p class="text-sm font-semibold text-ink-soft">Read what buyers say about us</p>
        <a href="{C['indiamart']}" target="_blank" rel="noopener" class="mt-2 inline-flex items-center gap-2 font-display text-lg font-extrabold text-brand-600">Reviews on IndiaMart {icon('arrow', 'h-4 w-4')}</a>
      </div>
    </div>
    <ul class="grid gap-7 sm:grid-cols-2">{why_html}</ul>
  </div>
</section>

<!-- BRANDS -->
<section class="section container-x">
  {section_head('Brands we deal in', 'Genuine products from <span class="text-brand-600">names you trust.</span>', center=True)}
  <div class="mt-10 grid grid-cols-2 gap-4 md:grid-cols-4">{brand_html}</div>
</section>

<!-- ON REQUEST -->
<section class="container-x pb-20">
  <div class="rounded-3xl bg-brand-50 p-6 md:p-10">
    <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
      <div><span class="eyebrow">Also available</span><h2 class="mt-2 text-2xl font-extrabold md:text-3xl">Weighbridges, moisture analysers & POS</h2></div>
      <p class="max-w-md text-sm text-ink-soft">Project-based ranges quoted to your site and specification.</p>
    </div>
    <div class="mt-8 grid gap-4 md:grid-cols-2">{req_html}</div>
  </div>
</section>

{cta_band(root)}
"""
    write("index.html", layout(
        f"{C['name']} | Weighing Scale Dealer in Ludhiana, Punjab",
        f"Authorised dealer of Essae, CAS, DIGI & Tula weighing scales in Ludhiana since {C['founded']}. Retail, industrial, crane, jewellery scales, lab balances, calibration, repair and ERP integration.",
        body, root, "index.html", [org_schema()], "index.html"))


def about():
    root = ""
    facts = [("Nature of business", "Trader — Wholesaler / Distributor"), ("Established", str(C["founded"])),
             ("Proprietor", C["owner"]), ("Legal status", C["legal"]), ("Team size", "Up to 10 people"),
             ("GST No.", C["gst"]), ("IEC", C["iec"]), ("UDYAM", C["udyam"]),
             ("Payment modes", C["payment"]), ("Shipment", C["shipping"])]
    fact_rows = "".join(f'<div class="flex justify-between gap-6 border-b border-line py-3.5 text-sm last:border-0"><dt class="text-ink-soft">{k}</dt><dd class="text-right font-semibold">{e(v)}</dd></div>' for k, v in facts)
    values = [("award", "Commitment to quality", "We follow a quality process from procurement to delivery at your site, so every scale arrives tested and accurate."),
              ("users", "Experienced team", "Our professionals know weighing inside out and attend regular training to keep up with new models and regulations."),
              ("shield", "Licensed & authorised", "Government-licensed to deal in weighing instruments, and an authorised distributor of Tula Digital (I) Pvt. Ltd."),
              ("cpu", "Future-ready", "We stay at the cutting edge — connected scales, label printing and ERP integration for growing businesses.")]
    val_html = "".join(f'<div class="card p-7"><span class="grid h-12 w-12 place-items-center rounded-xl bg-brand-600 text-white">{icon(ic, "h-6 w-6")}</span><h3 class="mt-5 text-lg font-bold">{t}</h3><p class="mt-2 text-sm leading-relaxed text-ink-soft">{d}</p></div>' for ic, t, d in values)
    certs = [("https://3.imimg.com/data3/DA/CP/MY-3338415/20140520_215804-1000x1000.jpg", "Dealer licence for weighing instruments"),
             ("https://4.imimg.com/data4/MI/DI/MY-2/1-1000x1000.jpeg", "Authorised distributor — Tula Digital (I) Pvt. Ltd.")]
    cert_html = "".join(f'<figure class="card overflow-hidden"><div class="aspect-[4/3] bg-surface"><img src="{u}" alt="{t}" loading="lazy" class="h-full w-full object-cover" onerror="this.onerror=null;this.src=\'assets/img/scale-placeholder.svg\'"></div><figcaption class="p-4 text-sm font-semibold">{t}</figcaption></figure>' for u, t in certs)
    body = page_hero(root, "About us", f"Weighing Punjab's business, <span class='text-accent-400'>accurately, since {C['founded']}.</span>",
                     "A Ludhiana-based trader, wholesaler and distributor of electronic weighing scales, balances and weighing systems.",
                     [("About", None)]) + f"""
<section class="section container-x grid gap-12 lg:grid-cols-[1.3fr_1fr]">
  <div class="prose-body">
    <span class="eyebrow">Our story</span>
    <h2 class="h2">From a single counter to a full weighing partner</h2>
    <p>Accurate Weighing Systems was set up in {C['founded']} in Ludhiana under the guidance of Mr. {C['owner']}. Through years of hard work and fair dealing, the company has grown into one of the region's trusted suppliers of Essae, CAS and DIGI weighing solutions.</p>
    <p>We trade, wholesale and distribute weighing scales, lab balances, advanced moisture analysers, POS systems and components, industrial and retail scales, jewellery scales, crane and hanging scales, marble-inlay table-top scales, printers and electronic weighbridges. We also supply special indicator systems that integrate weighing with SAP, ERP and Busy software.</p>
    <p>Our scales are made by renowned manufacturers to international quality standards and are valued for being easy to use, easy to install, durable, compact and long-lasting. They are used across pharmaceutical, chemical, jewellery, provision-store and food-processing businesses — and many more.</p>
    <blockquote class="mt-8 rounded-2xl border-l-4 border-accent-500 bg-surface p-6">
      <p class="font-display text-lg font-bold leading-snug text-ink">“A scale is a promise of fairness between a seller and a buyer. Our job is to make sure that promise is kept — every single weighing.”</p>
      <footer class="mt-3 text-sm text-ink-soft">— {C['owner']}, Proprietor</footer>
    </blockquote>
  </div>
  <aside class="h-fit rounded-3xl border border-line bg-white p-7 shadow-xl shadow-navy-900/5 lg:sticky lg:top-28">
    <h3 class="text-lg font-bold">Company fact sheet</h3>
    <dl class="mt-4">{fact_rows}</dl>
  </aside>
</section>

<section class="section bg-surface"><div class="container-x">
  {section_head('What drives us', 'Our values', center=True)}
  <div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{val_html}</div>
</div></section>

<section class="section container-x grid gap-12 lg:grid-cols-2">
  <div>
    <span class="eyebrow">Our mission</span>
    <h2 class="h2">Growth through innovation and people</h2>
    <ul class="mt-6 space-y-4">
      <li class="flex gap-4"><span class="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-accent-500 text-navy-950">{icon('check', 'h-4 w-4')}</span><span class="text-ink-soft">To be at the cutting edge of technology, in both physical and intellectual resources, and create value for our stakeholders through growth and innovation.</span></li>
      <li class="flex gap-4"><span class="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-accent-500 text-navy-950">{icon('check', 'h-4 w-4')}</span><span class="text-ink-soft">To nurture a culture of dynamism and learning that gives every team member room for professional and personal growth.</span></li>
    </ul>
    <h3 class="mt-10 text-xl font-bold">Customer support</h3>
    <p class="mt-3 leading-relaxed text-ink-soft">Our strength is total support: trained engineers at our head office and on customer projects take care of installation, calibration and service long after the sale.</p>
  </div>
  <div>
    <span class="eyebrow">Certifications</span>
    <h2 class="h2">Licensed. Authorised. Accountable.</h2>
    <div class="mt-8 grid gap-5 sm:grid-cols-2">{cert_html}</div>
  </div>
</section>
{cta_band(root, "Let's find the right scale for you")}
"""
    write("about.html", layout(f"About Us | {C['name']}, Ludhiana",
                               f"Since {C['founded']}, {C['name']} has supplied Essae, CAS and DIGI weighing scales, balances and systems to businesses across Punjab.",
                               body, root, "about.html", [org_schema()], "about.html"))


def products_page():
    root = ""
    def box(name, value, label, count):
        return f'<label class="flex cursor-pointer items-center justify-between gap-3 rounded-lg px-2 py-1.5 text-sm hover:bg-surface"><span class="flex items-center gap-2.5"><input type="checkbox" name="{name}" value="{e(value)}" class="h-4 w-4 accent-brand-600">{e(label)}</span><span class="text-xs text-ink-soft">{count}</span></label>'
    cats = "".join(box("cat", s, n, len(products_in(s))) for s, n, _, _ in CATEGORIES)
    brands = sorted({p["brand"] for p in PRODUCTS})
    brand_boxes = "".join(box("brand", b, b, sum(1 for p in PRODUCTS if p["brand"] == b)) for b in brands)
    inds = "".join(box("ind", s, n, sum(1 for p in PRODUCTS if s in p["industries"])) for s, n, *_ in INDUSTRIES)
    cards = "".join(product_card(p, root, i) for i, p in enumerate(PRODUCTS))
    body = page_hero(root, "Products", "Weighing scales, balances <span class='text-accent-400'>& systems</span>",
                     f"{len(PRODUCTS)} models from Essae, Tula and Swift in stock — plus CAS, DIGI, weighbridges and more on request.",
                     [("Products", None)]) + f"""
<section class="container-x py-12">
  <div class="grid gap-8 lg:grid-cols-[270px_1fr]">
    <aside>
      <button type="button" id="filter-toggle" class="btn btn-outline w-full lg:hidden">{icon('filter', 'h-4 w-4')} Filters</button>
      <div id="filters" class="hidden space-y-6 lg:sticky lg:top-28 lg:block">
        <div class="mt-4 flex items-center justify-between lg:mt-0"><h2 class="text-lg font-bold">Filter</h2><button type="button" id="clear-filters" class="text-sm font-semibold text-brand-600">Clear all</button></div>
        <div class="card p-4"><h3 class="mb-2 px-2 text-xs font-bold uppercase tracking-widest text-ink-soft">Category</h3>{cats}</div>
        <div class="card p-4"><h3 class="mb-2 px-2 text-xs font-bold uppercase tracking-widest text-ink-soft">Brand</h3>{brand_boxes}</div>
        <div class="card p-4"><h3 class="mb-2 px-2 text-xs font-bold uppercase tracking-widest text-ink-soft">Industry</h3>{inds}</div>
      </div>
    </aside>
    <div>
      <div class="flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-surface px-5 py-4">
        <p class="text-sm text-ink-soft">Showing <strong id="result-count" class="text-ink">{len(PRODUCTS)}</strong> products</p>
        <label class="flex items-center gap-2 text-sm text-ink-soft">Sort
          <select id="sort" class="rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink">
            <option value="default">Recommended</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option>
          </select></label>
      </div>
      <div id="product-grid" class="mt-6 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">{cards}</div>
      <div id="no-results" class="hidden rounded-2xl border border-dashed border-line p-10 text-center">
        <p class="font-semibold">No products match these filters.</p>
        <p class="mt-1 text-sm text-ink-soft">We can source most models — <button type="button" data-enquire="" class="font-semibold text-brand-600">send us your requirement</button>.</p>
      </div>
    </div>
  </div>
</section>
{cta_band(root, "Can't find your model?", "We source most brands and capacities. Share your requirement and we'll get back with options and prices.")}
"""
    write("products.html", layout(f"Weighing Scales & Balances — Products | {C['name']}",
                                  "Browse retail, printing, platform, industrial, crane, jewellery scales, lab balances and weighing systems with prices. Essae, Tula, Swift, CAS and DIGI.",
                                  body, root, "products.html", None, "products.html"))


def category_page(c):
    root = "../"
    slug, name, desc, ic = c
    items = products_in(slug)
    inds = [i for i in INDUSTRIES if slug in i[4]]
    ind_chips = "".join(f'<a href="{root}industries.html#{s}" class="inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-sm font-semibold text-white hover:bg-white/20">{icon(i_ic, "h-4 w-4 text-accent-400")}{e(n)}</a>' for s, n, _, i_ic, _ in inds)
    extra = f'<div class="mt-8 flex flex-wrap gap-2">{ind_chips}</div>' if ind_chips else ""
    cards = "".join(product_card(p, root, i) for i, p in enumerate(items))
    others = "".join(f'<a href="{s}.html" class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold hover:bg-surface {"bg-brand-50 text-brand-700" if s == slug else ""}">{icon(o_ic, "h-4 w-4 text-brand-500")}{e(n)}</a>' for s, n, _, o_ic in CATEGORIES)
    faqs = FAQS.get(slug, []) + FAQS["_default"]
    body = page_hero(root, f"{len(items)} products", e(name), e(desc), [("Products", f"{root}products.html"), (name, None)], extra) + f"""
<section class="container-x py-12">
  <div class="grid gap-8 lg:grid-cols-[1fr_260px]">
    <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">{cards}</div>
    <aside class="space-y-5 lg:sticky lg:top-28 lg:h-fit">
      <div class="card p-3"><p class="px-3 pb-2 pt-2 text-xs font-bold uppercase tracking-widest text-ink-soft">All categories</p>{others}</div>
      <div class="rounded-2xl bg-navy-900 p-6 text-white">
        <span class="grid h-11 w-11 place-items-center rounded-xl bg-accent-500 text-navy-950">{icon(ic, 'h-6 w-6')}</span>
        <p class="mt-4 font-display text-lg font-extrabold">Need help choosing?</p>
        <p class="mt-1 text-sm text-white/70">Tell us capacity and accuracy — we'll suggest the best fit.</p>
        <button type="button" data-enquire="{e(name)}" class="btn btn-accent mt-5 w-full">Ask an expert</button>
      </div>
    </aside>
  </div>
</section>
<section class="section bg-surface"><div class="container-x grid gap-12 lg:grid-cols-[1fr_1.4fr]">
  {section_head('FAQs', f'Questions about {e(name.lower())}')}
  <div class="space-y-3">{faq_block(faqs)}</div>
</div></section>
<div class="pt-20">{cta_band(root)}</div>
"""
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    write(f"category/{slug}.html", layout(f"{name} in Ludhiana | {C['name']}", f"{desc} Prices, specifications and enquiry — {C['name']}, Ludhiana.",
                                          body, root, "products.html", [faq_ld], f"category/{slug}.html"))


BENEFITS = {
    "retail-scales": ["Legal-for-trade accuracy", "Bright display readable by customers", "Battery backup for power cuts", "Rugged steel platter"],
    "printing-scales": ["No separate billing step", "Barcode / receipt printing", "Stores item and price memory", "Connects to PC and ERP"],
    "platform-scales": ["Heavy-duty load cell", "Large platform for bags and cartons", "Low-profile for easy loading", "Battery backup"],
    "industrial-scales": ["Count parts by weight", "Over/under check alerts", "Built for 24×7 duty", "Overload protection"],
    "crane-scales": ["Weigh while lifting", "Large display readable from the floor", "Rechargeable battery", "Saves floor space and time"],
    "precision-balances": ["Milligram-level repeatability", "Draft shield for stable readings", "Long-term stability", "Audit-ready calibration"],
    "jewellery-scales": ["10 mg resolution", "Gram and carat units", "Fast, stable readings", "Compact counter footprint"],
    "weighing-systems": ["Built to your site", "PLC / ERP connectivity", "Remote indicator", "Batching and stock control"],
}


def product_page(p, idx):
    root = "../"
    c = CAT[p["cat"]]
    rows = "".join(f'<tr class="border-b border-line last:border-0"><th scope="row" class="w-2/5 bg-surface px-5 py-3.5 text-left text-sm font-semibold text-ink-soft">{e(k)}</th><td class="px-5 py-3.5 text-sm font-semibold">{e(v)}</td></tr>' for k, v in [("Brand", p["brand"]), ("Category", c[1])] + list(p["specs"].items()))
    tags = "".join(f'<a href="{root}industries.html#{i}" class="chip hover:bg-brand-50 hover:text-brand-700">{e(IND[i][1])}</a>' for i in p["industries"])
    bens = "".join(f'<li class="flex items-center gap-3 rounded-xl bg-surface px-4 py-3 text-sm font-semibold">{icon("check", "h-4 w-4 shrink-0 text-brand-600")}{b}</li>' for b in BENEFITS[p["cat"]])
    similar = [x for x in PRODUCTS if x["cat"] == p["cat"] and x is not p][:4]
    if len(similar) < 4:
        similar += [x for x in PRODUCTS if x["cat"] != p["cat"] and any(i in x["industries"] for i in p["industries"])][:4 - len(similar)]
    sim = "".join(product_card(x, root, i) for i, x in enumerate(similar))
    faqs = FAQS.get(p["cat"], []) + FAQS["_default"]
    wa = wa_link(f"Hi, please share the best price for {p['name']}.")
    body = f"""
<section class="bg-navy-900 py-5"><div class="container-x">{breadcrumb(root, [("Products", f"{root}products.html"), (c[1], f"{root}category/{c[0]}.html"), (p["name"], None)])}</div></section>
<section class="container-x grid gap-10 py-12 lg:grid-cols-2 lg:gap-16">
  <div class="lg:sticky lg:top-28 lg:h-fit">
    <div class="relative aspect-square overflow-hidden rounded-3xl border border-line bg-surface">
      {f'<span class="badge badge-{p["badge"]}">{p["badge"]}</span>' if p["badge"] else ''}
      {img(p, root, 'h-full w-full object-contain p-10 product-img', eager=True)}
    </div>
    <p class="mt-3 text-center text-xs text-ink-soft">Images are for reference; actual product may vary slightly.</p>
  </div>
  <div>
    <a href="{root}category/{c[0]}.html" class="text-sm font-semibold uppercase tracking-wider text-brand-600 hover:underline">{e(p['brand'])} · {e(c[1])}</a>
    <h1 class="mt-2 text-3xl font-extrabold md:text-4xl">{e(p['name'])}</h1>
    <p class="mt-4 text-lg leading-relaxed text-ink-soft">{e(p['desc'])}</p>
    <div class="mt-6 flex flex-wrap items-end gap-3 rounded-2xl bg-brand-50 p-5">
      <div><p class="text-xs font-semibold uppercase tracking-wider text-brand-700">Indicative price</p><p class="mt-1">{price_html(p, 'text-3xl')}</p></div>
      <p class="ml-auto text-xs text-ink-soft">+ GST · Delivery extra · Ask for bulk rates</p>
    </div>
    <div class="mt-6 grid gap-3 sm:grid-cols-2">
      <button type="button" data-enquire="{e(p['name'])}" class="btn btn-primary py-3.5">{icon('tag', 'h-4 w-4')} Get best price</button>
      <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa py-3.5">{wa_icon('h-4 w-4')} Enquire on WhatsApp</a>
      <a href="tel:+{C['phone_raw']}" class="btn btn-outline py-3.5">{icon('phone', 'h-4 w-4')} Call {C['phone']}</a>
      <a href="{wa_link(f'Please send the brochure for {p["name"]}.')}" target="_blank" rel="noopener" class="btn btn-outline py-3.5">{icon('download', 'h-4 w-4')} Request brochure</a>
    </div>
    <div class="mt-8"><p class="text-sm font-semibold text-ink-soft">Ideal for</p><div class="mt-2 flex flex-wrap gap-2">{tags}</div></div>
    <h2 class="mt-10 text-xl font-extrabold">Specifications</h2>
    <div class="mt-4 overflow-hidden rounded-2xl border border-line"><table class="w-full">{rows}</table></div>
    <h2 class="mt-10 text-xl font-extrabold">Key benefits</h2>
    <ul class="mt-4 grid gap-3 sm:grid-cols-2">{bens}</ul>
    <div class="mt-10 grid gap-3 sm:grid-cols-3">
      <div class="flex items-center gap-3 rounded-xl border border-line p-4 text-sm font-semibold">{icon('shield', 'h-6 w-6 text-brand-600')}Warranty support</div>
      <div class="flex items-center gap-3 rounded-xl border border-line p-4 text-sm font-semibold">{icon('wrench', 'h-6 w-6 text-brand-600')}Installation & demo</div>
      <div class="flex items-center gap-3 rounded-xl border border-line p-4 text-sm font-semibold">{icon('badge', 'h-6 w-6 text-brand-600')}Calibration help</div>
    </div>
  </div>
</section>
<section class="section bg-surface"><div class="container-x grid gap-12 lg:grid-cols-[1fr_1.4fr]">
  {section_head('FAQs', 'Frequently asked questions')}
  <div class="space-y-3">{faq_block(faqs)}</div>
</div></section>
<section class="section container-x">
  {section_head('You may also like', 'Similar products', action=f'<a href="{root}category/{c[0]}.html" class="btn btn-outline">View all {e(c[1].lower())} {icon("arrow", "h-4 w-4")}</a>')}
  <div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{sim}</div>
</section>
{cta_band(root)}
"""
    schema = {"@context": "https://schema.org", "@type": "Product", "name": p["name"],
              "brand": {"@type": "Brand", "name": p["brand"]}, "category": c[1], "description": p["desc"],
              "image": big_img(p["img"]) if p["img"] else f"{SITE_URL}/assets/img/scale-placeholder.svg",
              "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["specs"].items()]}
    if p["price"]:
        schema["offers"] = {"@type": "Offer", "priceCurrency": "INR", "price": p["price"], "availability": "https://schema.org/InStock",
                            "seller": {"@type": "Organization", "name": C["name"]}}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    price_txt = f"₹{inr(p['price'])}" if p["price"] else "Best price"
    write(f"product/{p['slug']}.html", layout(f"{p['name']} — {price_txt} | {C['name']}",
                                               f"{p['name']} ({p['brand']}): {p['desc']} Buy in Ludhiana from {C['name']}.",
                                               body, root, "products.html", [schema, faq_ld], f"product/{p['slug']}.html"))


def industries_page():
    root = ""
    nav = "".join(f'<a href="#{s}" class="inline-flex shrink-0 items-center gap-2 rounded-full border border-line bg-white px-4 py-2 text-sm font-semibold hover:border-brand-500 hover:text-brand-600">{icon(ic, "h-4 w-4 text-brand-500")}{e(n)}</a>' for s, n, _, ic, _ in INDUSTRIES)
    blocks = ""
    for k, (s, n, d, ic, cats) in enumerate(INDUSTRIES):
        prods = [p for p in PRODUCTS if s in p["industries"]][:3]
        cat_links = "".join(f'<a href="category/{cs}.html" class="flex items-center justify-between rounded-xl border border-line bg-white px-4 py-3 text-sm font-semibold hover:border-brand-400 hover:text-brand-600">{e(CAT[cs][1])}{icon("arrow", "h-4 w-4")}</a>' for cs in cats)
        blocks += f"""
<section id="{s}" class="scroll-mt-28 py-14 {'bg-surface' if k % 2 else ''}">
  <div class="container-x grid gap-10 lg:grid-cols-[1fr_2fr]">
    <div>
      <span class="grid h-14 w-14 place-items-center rounded-2xl bg-navy-900 text-accent-400">{icon(ic, 'h-7 w-7')}</span>
      <h2 class="mt-5 text-2xl font-extrabold md:text-3xl">{e(n)}</h2>
      <p class="mt-3 leading-relaxed text-ink-soft">{e(d)}</p>
      <p class="mt-6 text-xs font-bold uppercase tracking-widest text-ink-soft">Recommended ranges</p>
      <div class="mt-3 grid gap-2">{cat_links}</div>
      <button type="button" data-enquire="Solution for {e(n)}" class="btn btn-primary mt-6">Talk to an expert</button>
    </div>
    <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">{''.join(product_card(p, root, i) for i, p in enumerate(prods))}</div>
  </div>
</section>"""
    body = page_hero(root, "Industries", "The right scale for <span class='text-accent-400'>your trade.</span>",
                     "Explore weighing solutions for your industry — with recommended ranges and popular models.",
                     [("Industries", None)]) + f"""
<div class="sticky top-20 z-30 border-b border-line bg-white/95 backdrop-blur"><div class="container-x no-scrollbar flex gap-2 overflow-x-auto py-3">{nav}</div></div>
{blocks}
<div class="pt-10">{cta_band(root)}</div>"""
    write("industries.html", layout(f"Industries We Serve | {C['name']}",
                                    "Weighing solutions for retail, jewellery, pharma, chemical, food processing, textile, engineering and logistics businesses in Punjab.",
                                    body, root, "industries.html", None, "industries.html"))


def services_page():
    root = ""
    details = {
        "Installation & Demo": ["Site check and levelling", "Load-cell and indicator set-up", "Staff demo and training", "Handover with test report"],
        "Calibration & Stamping": ["Certified test weights", "Calibration certificate", "Legal Metrology verification support", "Re-stamping reminders"],
        "Repair & AMC": ["All major brands serviced", "Genuine spare parts", "Preventive maintenance visits", "Priority breakdown response"],
        "ERP / SAP / Busy Integration": ["RS-232 / USB / LAN indicators", "Auto-capture of weight into ERP", "Barcode and label workflows", "Custom reports and slips"],
    }
    svc = ""
    for k, (n, d, ic) in enumerate(SERVICES):
        pts = "".join(f'<li class="flex items-center gap-3 text-sm">{icon("check", "h-4 w-4 text-brand-600")}{x}</li>' for x in details[n])
        svc += f"""<div class="card flex flex-col p-8">
  <div class="flex items-center justify-between"><span class="grid h-14 w-14 place-items-center rounded-2xl bg-brand-600 text-white">{icon(ic, 'h-7 w-7')}</span><span class="font-display text-5xl font-extrabold text-line">0{k+1}</span></div>
  <h2 class="mt-6 text-2xl font-extrabold">{e(n)}</h2><p class="mt-3 leading-relaxed text-ink-soft">{e(d)}</p>
  <ul class="mt-6 grid gap-2.5 sm:grid-cols-2">{pts}</ul>
  <button type="button" data-enquire="Service: {e(n)}" class="btn btn-outline mt-8 self-start">Request this service</button></div>"""
    steps = [("Tell us", "Share your problem or requirement by call, WhatsApp or the form."), ("We assess", "Our engineer checks the scale or site and gives a clear quote."),
             ("We fix / install", "Repair, calibration or installation done on schedule."), ("Stay accurate", "Reminders for calibration and AMC visits.")]
    step_html = "".join(f'<div class="relative"><span class="grid h-12 w-12 place-items-center rounded-full bg-accent-500 font-display text-lg font-extrabold text-navy-950">{k+1}</span><h3 class="mt-4 text-lg font-bold text-white">{t}</h3><p class="mt-2 text-sm text-white/65">{d}</p></div>' for k, (t, d) in enumerate(steps))
    body = page_hero(root, "Services", "Accurate today. <span class='text-accent-400'>Accurate every day.</span>",
                     "Installation, calibration, repair, AMC and ERP integration — from the team that sold you the scale.",
                     [("Services", None)]) + f"""
<section class="section container-x"><div class="grid gap-6 md:grid-cols-2">{svc}</div></section>
<section class="section relative overflow-hidden bg-navy-900"><div class="grid-pattern absolute inset-0"></div>
  <div class="container-x relative">
    <div class="max-w-2xl"><span class="eyebrow text-accent-400">How it works</span><h2 class="h2 text-white">Simple, fast service</h2></div>
    <div class="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">{step_html}</div>
  </div>
</section>
<section class="section container-x grid gap-12 lg:grid-cols-2">
  <div>
    <span class="eyebrow">Service request</span>
    <h2 class="h2">Book a service visit</h2>
    <p class="lead">Scale showing wrong weight, not switching on, or due for stamping? Tell us and our engineer will call you back.</p>
    <ul class="mt-8 space-y-4 text-sm">
      <li class="flex items-center gap-3">{icon('phone', 'h-5 w-5 text-brand-600')}<a href="tel:+{C['phone_raw']}" class="font-semibold">{C['phone']}</a></li>
      <li class="flex items-center gap-3">{icon('clock', 'h-5 w-5 text-brand-600')}{C['hours']}</li>
      <li class="flex items-center gap-3">{icon('pin', 'h-5 w-5 text-brand-600')}{C['address']}</li>
    </ul>
  </div>
  <form data-wa-form="Service request" class="card grid gap-4 p-6 md:p-8">
    <div class="grid gap-4 sm:grid-cols-2">
      <div><label class="label" for="s-name">Name *</label><input id="s-name" name="Name" required class="field"></div>
      <div><label class="label" for="s-phone">Mobile *</label><input id="s-phone" name="Mobile" type="tel" required class="field"></div>
    </div>
    <div class="grid gap-4 sm:grid-cols-2">
      <div><label class="label" for="s-type">Service needed</label><select id="s-type" name="Service" class="field">{''.join(f'<option>{e(n)}</option>' for n, _, _ in SERVICES)}</select></div>
      <div><label class="label" for="s-brand">Scale brand / model</label><input id="s-brand" name="Scale" class="field" placeholder="e.g. Essae DS-215"></div>
    </div>
    <div><label class="label" for="s-msg">Describe the issue</label><textarea id="s-msg" name="Issue" rows="4" class="field"></textarea></div>
    <button class="btn btn-primary">{wa_icon('h-4 w-4')} Send service request</button>
    <p data-form-ok class="hidden rounded-xl bg-brand-50 p-3 text-center text-sm font-medium text-brand-700">Thanks! WhatsApp has opened with your request — just press send.</p>
  </form>
</section>"""
    write("services.html", layout(f"Weighing Scale Repair, Calibration & AMC | {C['name']}",
                                  "Weighing scale installation, calibration, Legal Metrology stamping support, repair, AMC and SAP/ERP/Busy integration in Ludhiana.",
                                  body, root, "services.html", None, "services.html"))


def brands_page():
    root = ""
    blocks = ""
    for b in BRANDS:
        key = b["name"].split()[0].lower()
        names = {"tula": ("Tula", "Swift")}.get(key, (b["name"],))
        prods = [p for p in PRODUCTS if p["brand"] in names][:4]
        grid = "".join(product_card(p, root, i) for i, p in enumerate(prods)) if prods else f'<div class="card col-span-full grid place-items-center p-10 text-center"><p class="font-semibold">Full {e(b["name"])} range available on request.</p><button type="button" data-enquire="{e(b["name"])} products" class="btn btn-primary mt-4">Ask for {e(b["name"])} models</button></div>'
        link = f'<a href="products.html?brand={names[0]}" class="btn btn-outline">All {e(b["name"])} products {icon("arrow", "h-4 w-4")}</a>' if prods else ""
        blocks += f"""<section id="{key}" class="scroll-mt-28 border-b border-line py-14 last:border-0">
  <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
    <div class="max-w-2xl"><p class="font-display text-4xl font-extrabold text-navy-700">{e(b['name'])}</p><p class="mt-3 text-ink-soft">{e(b['desc'])}</p></div>{link}</div>
  <div class="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{grid}</div></section>"""
    body = page_hero(root, "Brands", "Genuine brands. <span class='text-accent-400'>Honest advice.</span>",
                     "As a multi-brand dealer, we recommend the scale that fits your work and budget — not just one maker's catalogue.",
                     [("Brands", None)]) + f'<div class="container-x">{blocks}</div>{cta_band(root)}'
    write("brands.html", layout(f"Brands — Essae, CAS, DIGI, Tula | {C['name']}",
                                "Authorised multi-brand weighing scale dealer in Ludhiana: Essae, CAS, DIGI, Tula and Swift.",
                                body, root, "brands.html", None, "brands.html"))


def downloads_page():
    root = ""
    rows = ""
    for s, n, d, ic in CATEGORIES:
        rows += f"""<div class="card flex items-center gap-5 p-5">
  <span class="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-red-50 text-red-600">{icon('file', 'h-7 w-7')}</span>
  <div class="min-w-0 flex-1"><h3 class="font-bold">{e(n)} brochure</h3><p class="text-sm text-ink-soft">{len(products_in(s))} models · PDF</p></div>
  <!-- Put the PDF in assets/brochures/{s}.pdf and change this to a direct download link -->
  <a href="{wa_link(f'Please send the {n} brochure.')}" target="_blank" rel="noopener" class="btn btn-outline shrink-0 px-4 py-2 text-xs">{icon('download', 'h-4 w-4')} Get PDF</a>
</div>"""
    body = page_hero(root, "Downloads", "Brochures & <span class='text-accent-400'>catalogues</span>",
                     "Product brochures, price lists and manuals — download or request them on WhatsApp.",
                     [("Downloads", None)]) + f"""
<section class="section container-x">
  <div class="grid gap-4 md:grid-cols-2">{rows}</div>
  <div class="mt-10 rounded-2xl bg-surface p-6 text-center text-sm text-ink-soft">Need a user manual, calibration certificate or price list? <button type="button" data-enquire="Document request" class="font-semibold text-brand-600">Request it here</button>.</div>
</section>"""
    write("downloads.html", layout(f"Downloads — Brochures & Catalogues | {C['name']}",
                                   "Download weighing scale brochures and catalogues from Accurate Weighing Systems, Ludhiana.",
                                   body, root, "downloads.html", None, "downloads.html"))


def contact_page():
    root = ""
    cards = [("phone", "Call us", C["phone"], f"tel:+{C['phone_raw']}"), ("mail", "Email", C["email"], f"mailto:{C['email']}"),
             ("pin", "Visit", C["address"], f"https://maps.google.com/?q={C['map_query']}"), ("clock", "Hours", C["hours"], None)]
    card_html = "".join(f"""<{'a href="' + h + '"' if h else 'div'} class="card flex items-center gap-4 p-5 transition {'hover:border-brand-400' if h else ''}">
  <span class="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-brand-600 text-white">{icon(ic, 'h-5 w-5')}</span>
  <span><span class="block text-xs font-semibold uppercase tracking-wider text-ink-soft">{t}</span><span class="block font-semibold">{e(v)}</span></span></{'a' if h else 'div'}>""" for ic, t, v, h in cards)
    cats = "".join(f'<option>{e(n)}</option>' for _, n, _, _ in CATEGORIES)
    body = page_hero(root, "Contact", "Let's talk <span class='text-accent-400'>weighing.</span>",
                     "Call, WhatsApp or send the form — we usually reply within an hour during business hours.",
                     [("Contact", None)]) + f"""
<section class="container-x relative z-10 -mt-8"><div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{card_html}</div></section>
<section class="section container-x grid gap-10 lg:grid-cols-[1.2fr_1fr]">
  <form data-wa-form="Website contact" class="card grid gap-4 p-6 md:p-10">
    <h2 class="text-2xl font-extrabold">Send us your requirement</h2>
    <div class="grid gap-4 sm:grid-cols-2">
      <div><label class="label" for="c-name">Name *</label><input id="c-name" name="Name" required class="field"></div>
      <div><label class="label" for="c-company">Company</label><input id="c-company" name="Company" class="field"></div>
    </div>
    <div class="grid gap-4 sm:grid-cols-2">
      <div><label class="label" for="c-phone">Mobile *</label><input id="c-phone" name="Mobile" type="tel" required class="field"></div>
      <div><label class="label" for="c-email">Email</label><input id="c-email" name="Email" type="email" class="field"></div>
    </div>
    <div class="grid gap-4 sm:grid-cols-2">
      <div><label class="label" for="c-cat">Product interest</label><select id="c-cat" name="Product interest" class="field"><option value="">Select…</option>{cats}<option>Service / calibration</option><option>ERP integration</option></select></div>
      <div><label class="label" for="c-city">City</label><input id="c-city" name="City" class="field"></div>
    </div>
    <div><label class="label" for="c-msg">Message *</label><textarea id="c-msg" name="Message" rows="5" required class="field" placeholder="Capacity, accuracy, quantity, where you'll use it…"></textarea></div>
    <button class="btn btn-primary py-3.5">{wa_icon('h-4 w-4')} Send via WhatsApp</button>
    <p data-form-ok class="hidden rounded-xl bg-brand-50 p-3 text-center text-sm font-medium text-brand-700">Thanks! WhatsApp has opened with your message — just press send.</p>
  </form>
  <div class="flex flex-col gap-6">
    <div class="overflow-hidden rounded-3xl border border-line"><iframe title="Map" src="https://maps.google.com/maps?q={C['map_query'].replace(' ', '%20')}&z=12&output=embed" class="h-80 w-full" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    <div class="rounded-3xl bg-navy-900 p-7 text-white">
      <h3 class="text-lg font-bold text-white">Business details</h3>
      <dl class="mt-4 space-y-2 text-sm text-white/70">
        <div class="flex justify-between gap-4"><dt>Proprietor</dt><dd class="font-semibold text-white">{C['owner']}</dd></div>
        <div class="flex justify-between gap-4"><dt>GST</dt><dd class="font-semibold text-white">{C['gst']}</dd></div>
        <div class="flex justify-between gap-4"><dt>Payments</dt><dd class="text-right font-semibold text-white">{C['payment']}</dd></div>
      </dl>
      <a href="{wa_link('Hi, I would like to know more about your weighing scales.')}" target="_blank" rel="noopener" class="btn btn-wa mt-6 w-full">{wa_icon('h-4 w-4')} Chat on WhatsApp</a>
    </div>
  </div>
</section>"""
    write("contact.html", layout(f"Contact Us | {C['name']}, Ludhiana",
                                 f"Contact {C['name']} in Ludhiana for weighing scale prices, service and calibration. Call {C['phone']}.",
                                 body, root, "contact.html", [org_schema()], "contact.html"))


def not_found():
    body = f"""<section class="container-x grid min-h-[60vh] place-items-center py-20 text-center"><div>
<p class="font-display text-8xl font-extrabold text-brand-100">404</p><h1 class="mt-2 text-3xl font-extrabold">This page tipped the scale</h1>
<p class="mt-3 text-ink-soft">The page you're looking for doesn't exist. Try the product search or head home.</p>
<div class="mt-8 flex justify-center gap-3"><a href="/index.html" class="btn btn-primary">Go home</a><button type="button" data-search-open class="btn btn-outline">Search products</button></div></div></section>"""
    write("404.html", layout(f"Page not found | {C['name']}", "Page not found.", body, "/", "", None, "404.html"))


def data_js():
    rows = [{"slug": p["slug"], "name": p["name"], "brand": p["brand"], "cat": p["cat"],
             "catName": CAT[p["cat"]][1], "price": inr(p["price"])} for p in PRODUCTS]
    write("assets/js/products-data.js", "/* generated by build.py */\nwindow.AWS_PRODUCTS = " + json.dumps(rows, ensure_ascii=False) + ";\n")


def sitemap():
    urls = ["index.html", "about.html", "products.html", "industries.html", "services.html", "brands.html", "downloads.html", "contact.html"]
    urls += [f"category/{c[0]}.html" for c in CATEGORIES] + [f"product/{p['slug']}.html" for p in PRODUCTS]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE_URL}/{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", xml)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


if __name__ == "__main__":
    data_js(); home(); about(); products_page()
    for c in CATEGORIES:
        category_page(c)
    for i, p in enumerate(PRODUCTS):
        product_page(p, i)
    industries_page(); services_page(); brands_page(); downloads_page(); contact_page(); not_found(); sitemap()
    print(f"Built {8 + len(CATEGORIES) + len(PRODUCTS) + 1} pages")
