/* Accurate Weighing Systems — site interactions (no framework needed) */
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const ROOT = document.body.dataset.root || "";
  const WA = document.body.dataset.wa || "";

  /* ---------- sticky header shadow ---------- */
  const header = $("#site-header");
  const onScroll = () => header && header.classList.toggle("shadow-lg", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  const drawer = $("#mobile-menu");
  $$("[data-menu-open]").forEach((b) => b.addEventListener("click", () => { drawer.classList.remove("hidden"); document.body.classList.add("overflow-hidden"); }));
  $$("[data-menu-close]").forEach((b) => b.addEventListener("click", () => { drawer.classList.add("hidden"); document.body.classList.remove("overflow-hidden"); }));

  /* ---------- hero slider ---------- */
  const slider = $("[data-slider]");
  if (slider) {
    const slides = $$(".slide", slider);
    const dots = $$("[data-dot]", slider);
    let i = 0, timer;
    const go = (n) => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle("is-active", k === i));
      dots.forEach((d, k) => {
        d.classList.toggle("w-10", k === i); d.classList.toggle("bg-accent-500", k === i);
        d.classList.toggle("w-4", k !== i); d.classList.toggle("bg-white/40", k !== i);
      });
    };
    const start = () => { clearInterval(timer); timer = setInterval(() => go(i + 1), 6000); };
    $("[data-prev]", slider)?.addEventListener("click", () => { go(i - 1); start(); });
    $("[data-next]", slider)?.addEventListener("click", () => { go(i + 1); start(); });
    dots.forEach((d, k) => d.addEventListener("click", () => { go(k); start(); }));
    go(0); start();
  }

  /* ---------- tabs (featured products) ---------- */
  $$("[data-tabs]").forEach((wrap) => {
    const btns = $$("[data-tab]", wrap);
    const items = $$("[data-badge]", wrap);
    btns.forEach((b) => b.addEventListener("click", () => {
      btns.forEach((x) => { x.classList.remove("bg-navy-900", "text-white"); x.classList.add("bg-white", "text-ink"); });
      b.classList.add("bg-navy-900", "text-white"); b.classList.remove("bg-white", "text-ink");
      const t = b.dataset.tab;
      let shown = 0;
      items.forEach((it) => {
        const ok = (t === "all" || it.dataset.badge === t) && shown < 8;
        it.classList.toggle("hidden", !ok);
        if (ok) shown++;
      });
    }));
    btns[0]?.click();
  });

  /* ---------- animated counters ---------- */
  const counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target, end = +el.dataset.count, suffix = el.dataset.suffix || "";
      let cur = 0; const step = Math.max(1, Math.ceil(end / 40));
      const t = setInterval(() => { cur = Math.min(end, cur + step); el.textContent = cur + suffix; if (cur >= end) clearInterval(t); }, 30);
      io.unobserve(el);
    }), { threshold: 0.5 });
    counters.forEach((c) => io.observe(c));
  }

  /* ---------- search overlay ---------- */
  const search = $("#search-overlay");
  const input = $("#search-input");
  const results = $("#search-results");
  const data = window.AWS_PRODUCTS || [];
  const render = (q) => {
    q = q.trim().toLowerCase();
    const hits = q ? data.filter((p) => (p.name + " " + p.brand + " " + p.cat).toLowerCase().includes(q)).slice(0, 8) : [];
    results.innerHTML = hits.length
      ? hits.map((p) => `<a href="${ROOT}product/${p.slug}.html" class="flex items-center gap-4 rounded-xl p-3 hover:bg-surface">
          <span class="grid h-12 w-12 shrink-0 place-items-center rounded-lg bg-surface text-xs font-bold text-brand-700">${p.brand}</span>
          <span class="min-w-0"><span class="block truncate font-semibold">${p.name}</span><span class="text-sm text-ink-soft">${p.catName}${p.price ? " · ₹" + p.price : ""}</span></span></a>`).join("")
      : q ? `<p class="p-4 text-sm text-ink-soft">No match for “${q}”. <a class="font-semibold text-brand-600" href="${ROOT}contact.html">Ask us</a> — we source most models.</p>` : "";
  };
  $$("[data-search-open]").forEach((b) => b.addEventListener("click", () => { search.classList.remove("hidden"); setTimeout(() => input.focus(), 30); }));
  $$("[data-search-close]").forEach((b) => b.addEventListener("click", () => search.classList.add("hidden")));
  input?.addEventListener("input", (e) => render(e.target.value));

  /* ---------- product filters (products page) ---------- */
  const grid = $("#product-grid");
  if (grid) {
    const cards = $$("[data-product]", grid);
    const count = $("#result-count");
    const params = new URLSearchParams(location.search);
    ["cat", "brand", "ind"].forEach((k) => {
      const v = params.get(k);
      if (v) $$(`input[name="${k}"][value="${v}"]`).forEach((c) => (c.checked = true));
    });
    const apply = () => {
      const sel = (k) => $$(`input[name="${k}"]:checked`).map((c) => c.value);
      const cats = sel("cat"), brands = sel("brand"), inds = sel("ind");
      const sort = $("#sort")?.value || "default";
      let n = 0;
      cards.forEach((c) => {
        const ok = (!cats.length || cats.includes(c.dataset.cat)) &&
          (!brands.length || brands.includes(c.dataset.brand)) &&
          (!inds.length || c.dataset.ind.split(",").some((x) => inds.includes(x)));
        c.classList.toggle("hidden", !ok);
        if (ok) n++;
      });
      const sorted = [...cards].sort((a, b) => {
        const pa = +a.dataset.price || 1e9, pb = +b.dataset.price || 1e9;
        if (sort === "low") return pa - pb;
        if (sort === "high") return (+b.dataset.price || 0) - (+a.dataset.price || 0);
        return +a.dataset.order - +b.dataset.order;
      });
      sorted.forEach((c) => grid.appendChild(c));
      if (count) count.textContent = n;
      $("#no-results")?.classList.toggle("hidden", n !== 0);
    };
    $$("input[name=cat],input[name=brand],input[name=ind],#sort").forEach((el) => el.addEventListener("change", apply));
    $("#clear-filters")?.addEventListener("click", () => { $$("input[type=checkbox]").forEach((c) => (c.checked = false)); apply(); });
    $("#filter-toggle")?.addEventListener("click", () => $("#filters").classList.toggle("hidden"));
    apply();
  }

  /* ---------- enquiry modal + forms → WhatsApp ---------- */
  const modal = $("#enquiry-modal");
  const openModal = (product) => {
    if (!modal) return;
    $("#enq-product").value = product || "";
    $("#enq-title").textContent = product ? "Get the best price" : "Request a quote";
    $("#enq-sub").textContent = product || "Tell us what you need to weigh — we'll suggest the right scale.";
    modal.classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
    setTimeout(() => $("#enq-name").focus(), 30);
  };
  const closeModal = () => { modal.classList.add("hidden"); document.body.classList.remove("overflow-hidden"); };
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-enquire]");
    if (b) { e.preventDefault(); openModal(b.dataset.enquire); }
    if (e.target.closest("[data-modal-close]") || e.target === modal) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { modal && !modal.classList.contains("hidden") && closeModal(); search?.classList.add("hidden"); }
  });

  /* Forms: validate, then open WhatsApp with the enquiry pre-filled.
     To also email / store leads, point the form's action to a PHP/Laravel
     endpoint (see README) and remove data-wa-form. */
  $$("form[data-wa-form]").forEach((f) => f.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!f.reportValidity()) return;
    const fd = new FormData(f);
    const lines = [`*New enquiry — ${f.dataset.waForm}*`];
    for (const [k, v] of fd.entries()) if (String(v).trim()) lines.push(`${k}: ${v}`);
    lines.push(`Page: ${location.href}`);
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(lines.join("\n"))}`, "_blank", "noopener");
    const ok = $("[data-form-ok]", f);
    if (ok) ok.classList.remove("hidden");
    f.reset();
  }));

  $$("[data-year]").forEach((y) => (y.textContent = new Date().getFullYear()));
})();
