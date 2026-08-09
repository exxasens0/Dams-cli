#!/usr/bin/env python3
"""Generate Lonely Planet–style HTML travel guide."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIKI = json.loads((ROOT / "_wiki_cache.json").read_text())
EXTRAS = json.loads((ROOT / "_day_extras.json").read_text())
REGS = json.loads((ROOT / "_municipal_regs.json").read_text())


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def img(key: str, alt: str, cls: str = "hero-img") -> str:
    w = WIKI.get(key) or {}
    src = w.get("thumb")
    if not src:
        return ""
    credit = w.get("wiki") or "#"
    return f'''<figure class="photo">
<img class="{cls}" src="{esc(src)}" alt="{esc(alt)}" loading="lazy" referrerpolicy="no-referrer">
<figcaption>Foto: Wikimedia / Wikipedia · <a href="{esc(credit)}" target="_blank" rel="noopener">fuente</a></figcaption>
</figure>'''


def quote(who: str, when: str, text: str, source: str = "Park4Night") -> str:
    return f'''<blockquote class="op">
<p>“{esc(text)}”</p>
<footer>— <strong>{esc(who)}</strong>, {esc(when)} · {esc(source)}</footer>
</blockquote>'''


def links(items: list[tuple[str, str, str]]) -> str:
    """items: (label, url, kind) — kind: g|o|w|p|wiki"""
    btns = []
    for label, url, kind in items:
        cls = {
            "g": "btn btn-g",
            "o": "btn btn-o",
            "w": "btn btn-w",
            "p": "btn btn-p",
            "wiki": "btn btn-wiki",
        }.get(kind, "btn")
        btns.append(f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>')
    return '<div class="btns">' + "".join(btns) + "</div>"


def wikiloc_box(items: list[tuple[str, str]]) -> str:
    """Dedicated visible Wikiloc button row."""
    if not items:
        return ""
    btns = "".join(
        f'<a class="btn btn-wiki" href="{esc(url)}" target="_blank" rel="noopener">Wikiloc · {esc(label)}</a>'
        for label, url in items
    )
    return (
        '<div class="wikiloc-box">'
        "<strong>Tracks Wikiloc (fácil/moderado)</strong>"
        f'<div class="btns">{btns}</div>'
        "</div>"
    )


def gmaps_dir(origin: tuple[float, float], dest: tuple[float, float], mode: str = "driving") -> str:
    """origin/dest as (lon, lat)."""
    olon, olat = origin
    dlon, dlat = dest
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}&travelmode={mode}"
    )


def gmaps_multi(
    origin: tuple[float, float],
    dest: tuple[float, float],
    waypoints: list[tuple[float, float]],
    mode: str = "driving",
) -> str:
    olon, olat = origin
    dlon, dlat = dest
    wps = "%7C".join(f"{lat},{lon}" for lon, lat in waypoints)
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}"
        f"&waypoints={wps}&travelmode={mode}"
    )


def poi_extra(region: str, items: list[str], link_items: list[tuple[str, str, str]]) -> str:
    lis = "\n".join(f"  <li>{item}</li>" for item in items)
    return f"""<div class="trail">
<h4>Puntos de interés extra ({region})</h4>
<ul>
{lis}
</ul>
{links(link_items)}
</div>"""


def parking_routes(
    dest_label: str,
    base: tuple[str, tuple[float, float]],
    dest: tuple[float, float],
    alts: list[tuple[str, tuple[float, float]]],
    base_mode: str = "walking",
    alt_mode: str = "walking",
) -> str:
    """Standard Google links: base→dest, each alt→dest, and A→B→C multi-stop."""
    base_id, base_coord = base
    mode_word = lambda m: "a pie" if m == "walking" else "coche"
    items: list[tuple[str, str, str]] = [
        (f"Google ({mode_word(base_mode)}) {base_id} → {dest_label}", gmaps_dir(base_coord, dest, base_mode), "g"),
    ]
    for alt_id, alt_coord in alts:
        items.append(
            (f"Google {mode_word(alt_mode)} {alt_id} → {dest_label}", gmaps_dir(alt_coord, dest, alt_mode), "g")
        )
    if alts:
        items.append(
            (f"Google A→B→C → {dest_label}", gmaps_multi(base_coord, dest, [c for _, c in alts], alt_mode), "g")
        )
    return links(items)


def day_extras_html(day_num: int) -> str:
    """Weather forecast + web opinions / plan-B alternatives for one day."""
    block = EXTRAS["days"].get(str(day_num)) or {}
    wx = block.get("weather") or {}
    opinions = block.get("opinions") or []
    alts = block.get("alternatives") or []
    meta = EXTRAS.get("meta") or {}

    if wx.get("available"):
        tips = "".join(f"<li>{esc(t)}</li>" for t in (wx.get("tips") or []))
        tips_html = f"<ul>{tips}</ul>" if tips else ""
        precip_prob = wx.get("precip_prob")
        precip_txt = f"{precip_prob:.0f}%" if precip_prob is not None else "—"
        uv = wx.get("uv_max")
        uv_txt = f"{uv:.1f}" if uv is not None else "—"
        wx_html = f"""<div class="wx">
<div class="wx-head"><strong>Meteo · {esc(wx.get('place') or '')}</strong>
<span>{esc(wx.get('date') or '')} · Open-Meteo</span></div>
<div class="wx-grid">
<div><em>Cielo</em><strong>{esc(wx.get('summary_es') or '—')}</strong></div>
<div><em>Temp</em><strong>{wx.get('t_min'):.0f}–{wx.get('t_max'):.0f}°C</strong></div>
<div><em>Lluvia</em><strong>{wx.get('precip_mm'):.1f} mm · {esc(precip_txt)}</strong></div>
<div><em>Viento / UV</em><strong>{wx.get('wind_max'):.0f} km/h · UV {esc(uv_txt)}</strong></div>
</div>
{tips_html}
<p class="wx-src">Fuente: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> best_match (modelos Météo-France / DWD / ECMWF). Previsión del {esc((meta.get('weather_fetched_at') or '')[:10])}; revisad la mañana del día.</p>
</div>"""
    else:
        wx_html = """<div class="wx"><div class="wx-head"><strong>Meteo</strong></div>
<p>Previsión aún fuera de horizonte o no disponible. Consultad Open-Meteo / Météo-France la víspera.</p></div>"""

    op_lis = "".join(f"<li>{esc(o)}</li>" for o in opinions)
    alt_lis = "".join(
        f'<li><strong>{esc(a.get("title") or "")}</strong> — {esc(a.get("why") or "")}'
        + (
            f' · <a href="{esc(a["url"])}" target="_blank" rel="noopener">ver</a>'
            if a.get("url")
            else ""
        )
        + "</li>"
        for a in alts
    )
    plan_html = f"""<div class="planb">
<h4>Opiniones web + plan B (si no os gusta)</h4>
<p class="wx-src">{esc(meta.get("opinions_note") or "")}</p>
<ul class="op-list">{op_lis}</ul>
<p><strong>Alternativas:</strong></p>
<ul>{alt_lis}</ul>
</div>"""
    return wx_html + plan_html


def _lis(items: list[str]) -> str:
    return "".join(f"<li>{esc(x)}</li>" for x in items)


def municipal_html(day_num: int) -> str:
    """Municipal / communal motorhome rules for the day's zone (August)."""
    block = REGS["days"].get(str(day_num)) or {}
    if not block:
        return ""
    meta = REGS.get("meta") or {}
    risk = (block.get("riesgo") or "medio").lower()
    risk_cls = {"alto": "risk-alto", "medio": "risk-medio", "bajo": "risk-bajo"}.get(risk, "risk-medio")
    fuentes = block.get("fuentes") or []
    src_btns = links([(f.get("label") or "Fuente", f["url"], "w") for f in fuentes if f.get("url")])
    tarifas = block.get("tarifas") or []
    tarifas_html = (
        f"<p><strong>Tarifas / agosto:</strong></p><ul>{_lis(tarifas)}</ul>" if tarifas else ""
    )
    return f"""<div class="regs">
<h4>Normativa municipal · autocaravanas<span class="regs-badge {risk_cls}">riesgo {esc(risk)}</span></h4>
<p><strong>{esc(block.get("commune") or "")}</strong> · {esc(block.get("agosto") or "")}</p>
<p class="regs-sum">{esc(block.get("resumen") or "")}</p>
<p><strong>Aparcamiento:</strong></p>
<ul>{_lis(block.get("aparcamiento") or [])}</ul>
<p><strong>Pernocta:</strong></p>
<ul>{_lis(block.get("pernocta") or [])}</ul>
{tarifas_html}
<p><strong>Estacionar ≠ acampar:</strong> {esc(block.get("camping_vs_stationnement") or "")}</p>
<p class="wx-src">{esc(meta.get("note_es") or "")}</p>
{src_btns}
</div>"""


def day_context_html(day_num: int) -> str:
    """Weather + opinions/plan B + municipal regs for one day."""
    return day_extras_html(day_num) + municipal_html(day_num)


def live_three_day_html() -> str:
    """Priority field plan for the current Monday–Wednesday itinerary."""
    return """
<section class="section live-plan" id="plan-rapido">
<div class="live-title"><span>Plan activo</span><h2>Lunes 10 · martes 11 · miércoles 12</h2></div>
<div class="warn"><strong>Prioridad miércoles:</strong> ruta <em>y</em> noche en alta montaña — no bajéis a Sentein / La Grange. Base fija: <strong>Col de la Core · P4N #6527 (~1.395 m)</strong>. Es alto y fresco, pero <strong>expuesto, sin sombra ni servicios</strong>: llenad agua el lunes, batería cargada, ventanas/toldos listos. No tratéis el parking como refugio de calor a las 17 h con el van cerrado. Bentaillou queda aparcado: demasiado exigente para este tramo.</div>

<article class="card prose">
<h3>Lunes 10 · Saint-Lizier + Col de la Core</h3>
<div class="meta"><span class="tag">visita + comida</span><span class="tag">P4N #6527</span><span class="tag">1.395 m</span><span class="tag">~24 °C máx. en el Col</span></div>
<div class="wx">
<div class="wx-head"><strong>Meteo actual · Col de la Core</strong><span>Lun 10 · Open-Meteo actualizado 9 ago</span></div>
<div class="wx-grid"><div><em>Mañana</em><strong>Seca · 15–21°C</strong></div><div><em>Mediodía</em><strong>21–24°C</strong></div><div><em>Tarde</em><strong>Chubascos desde ~17–18 h</strong></div><div><em>Noche</em><strong>Fresca, posible lluvia</strong></div></div>
</div>
<ol>
<li><strong>Salida tranquila del camping Ustou.</strong> <a href="https://www.google.com/maps/dir/?api=1&amp;origin=42.79757,1.26285&amp;destination=43.00045,1.13720&amp;travelmode=driving" target="_blank" rel="noopener">Google · Ustou → Saint-Lizier</a> (~40 min).</li>
<li><strong>Comida y visita corta de Saint-Lizier:</strong> aparcad en el <em>Palais des Évêques</em>, parking plano apto para camper alto; no entréis al casco por calles estrechas. Palacio, catedral, claustro y mirador. <strong>Agua:</strong> llenad bidones aquí o en Ustou — en el Col no hay.</li>
<li><strong>Después de comer:</strong> <a href="https://www.google.com/maps/dir/?api=1&amp;origin=43.00045,1.13720&amp;destination=42.85879,1.10511&amp;travelmode=driving" target="_blank" rel="noopener">Google · Saint-Lizier → Col de la Core</a> (~40 min). Llegad antes de que cambie el cielo y antes de que se llene. Esta será vuestra base martes <em>y</em> miércoles.</li>
</ol>
<div class="trail"><h4>Dormir lun + mar + (ideal) mié</h4>
<p><strong>P4N #6527 · Col de la Core</strong> — parking alto, vistas y dos salidas de sendero. Gratis, perros OK, sin agua/luz/ducha y <strong>sin sombra</strong>. Aparcad discretamente, sin desplegar material; los carteles locales mandan. Hay reseñas de obras/plazas reducidas: si no hay sitio, plan B inmediato abajo.</p>
<div class="btns"><a class="btn btn-o" href="https://park4night.com/es/place/6527" target="_blank" rel="noopener">P4N #6527 · Col de la Core</a><a class="btn btn-g" href="https://www.google.com/maps/dir/?api=1&amp;destination=42.85879,1.10511&amp;travelmode=driving" target="_blank" rel="noopener">Google Col de la Core</a><a class="btn btn-w" href="https://www.visorando.com/randonnee-estives-du-bouirex/" target="_blank" rel="noopener">Visorando · Bouirex</a><a class="btn btn-w" href="https://www.visorando.com/randonnee-etang-d-ayes/" target="_blank" rel="noopener">Visorando · Ayès</a></div>
</div>
</article>

<article class="card prose">
<h3>Martes 11 · 1ª ruta alta · dormir otra vez en el Col</h3>
<div class="meta"><span class="tag">salida 7:00–7:30</span><span class="tag">seca hasta ~14–15 h</span><span class="tag tag-bad">tormenta probable tarde</span><span class="tag">noche en altura</span></div>
<div class="wx">
<div class="wx-head"><strong>Meteo actual · altura Core</strong><span>Mar 11 · Open-Meteo actualizado 9 ago</span></div>
<div class="wx-grid"><div><em>Temp</em><strong>14–24°C</strong></div><div><em>Hasta 14 h</em><strong>Seco</strong></div><div><em>15–17 h</em><strong>Riesgo creciente</strong></div><div><em>17–22 h</em><strong>Tormenta probable</strong></div></div>
</div>
<div class="photo-grid">
<div class="trail"><h4>Elegid UNA · Cap de Bouirex</h4><p><strong>8 km · +516 m · 3 h 30 · 1.873 m.</strong> Circular amarilla desde el P4N, cumbre y gran panorama. Opción más corta y limpia — recomendada si el cielo es dudoso a las 7 h.</p><div class="btns"><a class="btn btn-w" href="https://www.tourisme-couserans-pyrenees.com/randonnees/estives-du-bouirex/" target="_blank" rel="noopener">Ficha oficial Bouirex</a><a class="btn btn-w" href="https://www.visorando.com/randonnee-estives-du-bouirex/" target="_blank" rel="noopener">Visorando · Bouirex (GPS)</a></div></div>
<div class="trail"><h4>O Étang d’Ayès + Chemin de la Liberté</h4><p><strong>9,7 km A/R · +590 m · ~3 h 45 · 1.742 m.</strong> Lago de altura y antigua ruta de evasión hacia España. Un pelín más larga; guardadla para el miércoles si hoy preferís Bouirex.</p><div class="btns"><a class="btn btn-w" href="https://www.petiterepublique.com/2022/07/29/tourisme-randonnee-letang-dayes-au-depart-du-col-de-la-corre/" target="_blank" rel="noopener">Ficha Étang d’Ayès</a><a class="btn btn-w" href="https://www.visorando.com/randonnee-etang-d-ayes/" target="_blank" rel="noopener">Visorando · Ayès (GPS)</a><a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944" target="_blank" rel="noopener">Wikiloc · Bethmale–Ayès</a></div></div>
</div>
<p><strong>Decisión:</strong> regresad al van <strong>antes de las 14 h</strong>. Perras con correa: estives, ganado y patous. Si aparecen nubes verticales o se oye trueno, bajad sin completar cumbre/lago.</p>
<p><strong>Tras la ruta · NO bajéis a Sentein.</strong> Quedaos en el Col de la Core. Si la tormenta es fuerte, el Col se llena o necesitáis sombra/WC: <a href="https://park4night.com/fr/place/10723" target="_blank" rel="noopener">P4N #10723 · Lac de Bethmale (~1.074 m)</a> — más bajo que el Col pero con sombra y servicios básicos; <a href="https://www.google.com/maps/dir/?api=1&amp;origin=42.85879,1.10511&amp;destination=42.8615,1.0565&amp;travelmode=driving" target="_blank" rel="noopener">Google · Core → Lac Bethmale</a> (~20 min). Prohibido bañarse en el lago.</p>
</article>

<article class="card prose">
<h3>Miércoles 12 · 2ª ruta alta · noche en altura</h3>
<div class="meta"><span class="tag">prioridad alta montaña</span><span class="tag">P4N #6527</span><span class="tag">salida 7:00–7:30</span><span class="tag">día más estable</span></div>
<div class="wx">
<div class="wx-head"><strong>Meteo actual · Col de la Core</strong><span>Mié 12 · Open-Meteo actualizado 9 ago</span></div>
<div class="wx-grid"><div><em>Temp</em><strong>16–26°C</strong></div><div><em>Lluvia</em><strong>~0,5 mm · pmax 5%</strong></div><div><em>Mañana</em><strong>Seca y usable</strong></div><div><em>Tarde</em><strong>Mejor que el martes</strong></div></div>
</div>
<div class="trail"><h4>Ruta · la que no hicisteis el martes</h4>
<p>Salís andando desde el mismo parking. Si el martes fue <strong>Bouirex</strong> → hoy <strong>Étang d’Ayès</strong> (9,7 km A/R, +590 m, ~3 h 45, lago a 1.742 m). Si el martes fue Ayès → hoy Bouirex (8 km, +516 m, 3 h 30, 1.873 m). Ambas son moderadas de altura, <strong>muy por debajo</strong> de Bentaillou (14 km / +1.000 m).</p>
<div class="btns"><a class="btn btn-w" href="https://www.visorando.com/randonnee-estives-du-bouirex/" target="_blank" rel="noopener">Visorando · Bouirex</a><a class="btn btn-w" href="https://www.visorando.com/randonnee-etang-d-ayes/" target="_blank" rel="noopener">Visorando · Ayès</a><a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944" target="_blank" rel="noopener">Wikiloc · Bethmale–Ayès</a></div>
</div>
<div class="trail"><h4>Dormir miércoles · alta montaña</h4>
<p><strong>Plan A:</strong> otra noche en <strong>Col de la Core · #6527</strong> (1.395 m) — coherente con la prioridad de altura. Revisad agua y batería; a mediodía puede hacer ~26 °C al sol: abrid todo, usad toldo si el viento lo permite, y no os enclaustréis en el van.</p>
<p><strong>Plan B sombra:</strong> <strong>Lac de Bethmale · P4N #10723</strong> (~1.074 m) si necesitáis árboles/WC tras dos noches expuestas. Sigue siendo montaña, no valle de Sentein.</p>
<div class="btns"><a class="btn btn-o" href="https://park4night.com/fr/place/6527" target="_blank" rel="noopener">P4N #6527 · Col de la Core</a><a class="btn btn-o" href="https://park4night.com/fr/place/10723" target="_blank" rel="noopener">P4N #10723 · Lac Bethmale</a><a class="btn btn-g" href="https://www.google.com/maps/dir/?api=1&amp;destination=42.8615,1.0565&amp;travelmode=driving" target="_blank" rel="noopener">Google Lac Bethmale</a></div>
</div>
<p class="wx-src"><strong>Aplazado a propósito:</strong> Camping La Grange (Sentein) y Mines de Bentaillou — valle + ruta dura. Solo si más adelante os apetece y estáis fuertes; no es el miércoles.</p>
</article>
</section>
"""


CSS = r"""
:root{--bg:#f2eee4;--ink:#1a221c;--muted:#4d5c52;--card:#fffdf8;--pine:#1b4a3b;--clay:#9a5528;--line:#d7cdbc;--shadow:0 14px 32px rgba(26,34,28,.09)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"Source Sans 3",system-ui,sans-serif;color:var(--ink);background:
radial-gradient(1000px 480px at 0% 0%,#dfe8df,transparent 55%),
radial-gradient(900px 420px at 100% 0%,#efe2d0,transparent 50%),var(--bg);line-height:1.65}
h1,h2,h3,h4{font-family:Fraunces,Georgia,serif;line-height:1.2;margin:0 0 .6rem}
a{color:var(--pine)}.wrap{width:min(980px,calc(100% - 1.2rem));margin:0 auto}
.top{position:sticky;top:0;z-index:50;background:rgba(255,253,248,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top-in{display:flex;justify-content:space-between;gap:.6rem;align-items:center;min-height:58px;flex-wrap:wrap;padding:.35rem 0}
.brand{font-family:Fraunces,serif;font-weight:700}.brand small{display:block;font-family:"Source Sans 3",sans-serif;color:var(--muted);font-size:.72rem;font-weight:400}
.btns{display:flex;flex-wrap:wrap;gap:.4rem;margin:.7rem 0}
.btn{display:inline-flex;align-items:center;text-decoration:none;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:.48rem .9rem;font-size:.84rem;font-weight:700}
.btn-p{background:var(--pine);border-color:var(--pine);color:#fff}.btn-g{background:#e8f0fe;border-color:#c6d7f5;color:#1a4f9c}
.btn-o{background:#fff1e6;border-color:#efd0b5;color:var(--clay)}.btn-w{background:#e7f6ef;border-color:#b9dccb;color:#146247}
.btn-wiki{background:#ff6a00;border-color:#e85e00;color:#fff;box-shadow:0 2px 0 rgba(180,70,0,.25)}
.btn-wiki:hover{filter:brightness(1.05)}
.wikiloc-box{margin:.85rem 0;padding:.85rem 1rem;border:2px solid #ff6a00;border-radius:14px;background:#fff7f0}
.wikiloc-box strong{display:block;color:#c24e00;font-size:.92rem;margin-bottom:.35rem}
.hero{padding:1.4rem 0 1rem}.hero h1{font-size:clamp(1.85rem,5.5vw,2.85rem);max-width:18ch}
.lead{color:var(--muted);font-size:1.08rem;max-width:62ch}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0}.chip{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:.25rem .7rem;font-size:.78rem;color:var(--muted)}
.section{margin:2.2rem 0}.section>h2{font-size:1.7rem;border-bottom:2px solid var(--pine);padding-bottom:.35rem;margin-bottom:1rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:1.15rem 1.2rem;margin:0 0 1.15rem;box-shadow:var(--shadow)}
.prose p{margin:.65rem 0}.prose ul,.prose ol{margin:.45rem 0 .8rem;padding-left:1.2rem}.prose li{margin:.28rem 0}
.meta{display:flex;flex-wrap:wrap;gap:.35rem;margin:.45rem 0 .85rem}
.tag{font-size:.72rem;font-weight:700;background:#e8efe9;color:var(--pine);border-radius:8px;padding:.22rem .5rem}
.tag-bad{background:#fff1e8;color:var(--clay)}
.callout{border-left:4px solid var(--pine);background:#eef5f0;padding:.8rem .95rem;border-radius:0 12px 12px 0;margin:.85rem 0}
.warn{border-left:4px solid var(--clay);background:#fff4ec;padding:.8rem .95rem;border-radius:0 12px 12px 0;margin:.85rem 0}
.photo{margin:1rem 0 1.1rem}.photo img{width:100%;max-height:420px;object-fit:cover;border-radius:14px;border:1px solid var(--line);display:block}
.photo figcaption{font-size:.75rem;color:var(--muted);margin-top:.35rem}
.photo-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:.55rem;margin:1rem 0}
@media(max-width:720px){.photo-grid{grid-template-columns:1fr}}
.photo-grid .photo{margin:0}.photo-grid img{max-height:280px}
.op{margin:1rem 0;padding:1rem 1.1rem;background:#f7f3ea;border-radius:14px;border:1px solid var(--line)}
.op p{margin:0 0 .55rem;font-style:italic}.op footer{font-size:.82rem;color:var(--muted)}
.trail{background:#f6faf7;border:1px dashed #b7cfc2;border-radius:14px;padding:.9rem 1rem;margin:.9rem 0}
.trail h4{margin-top:0;color:var(--pine)}
.wx{margin:.85rem 0;padding:.85rem 1rem;border-radius:14px;background:linear-gradient(135deg,#e8f2fb,#f4f7f2);border:1px solid #c5d6e6}
.wx-head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.35rem;margin-bottom:.55rem}
.wx-head span{font-size:.78rem;color:var(--muted)}
.wx-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.45rem .7rem;margin:.35rem 0 .55rem}
@media(min-width:640px){.wx-grid{grid-template-columns:repeat(4,1fr)}}
.wx-grid em{display:block;font-size:.68rem;color:var(--muted);font-style:normal;text-transform:uppercase;letter-spacing:.03em}
.wx-grid strong{font-size:.95rem}
.wx ul{margin:.35rem 0 0;padding-left:1.1rem}
.wx-src{font-size:.75rem;color:var(--muted);margin:.45rem 0 0}
.planb{margin:.85rem 0;padding:.9rem 1rem;border-radius:14px;background:#fff8f0;border:1px solid #e8d2b8}
.planb h4{margin-top:0;color:var(--clay)}
.planb .op-list{margin:.4rem 0 .7rem}
.regs{margin:.85rem 0;padding:.9rem 1rem;border-radius:14px;background:#f3f6f8;border:1px solid #c5d0d8}
.regs h4{margin-top:0;color:#1a3a4a}
.regs .regs-badge{display:inline-block;font-size:.72rem;font-weight:700;border-radius:8px;padding:.18rem .5rem;margin-left:.35rem}
.regs .risk-alto{background:#ffe5d9;color:#8a3010}
.regs .risk-medio{background:#fff0cc;color:#7a5a10}
.regs .risk-bajo{background:#e3f5e8;color:#1a5c32}
.regs ul{margin:.35rem 0 .65rem;padding-left:1.15rem}
.regs .regs-sum{font-weight:700;margin:.5rem 0 .35rem}
.day-nav{position:sticky;top:59px;z-index:40;display:grid;grid-template-columns:repeat(7,1fr);gap:.28rem;background:rgba(242,238,228,.96);padding:.4rem 0;backdrop-filter:blur(8px)}
.day-nav a{text-align:center;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.32rem .1rem;font-size:.68rem;font-weight:700;color:var(--ink)}
.day-nav a span{display:block;font-weight:400;color:var(--muted);font-size:.58rem}
.foot{margin:2.5rem 0 5rem;color:var(--muted);font-size:.9rem}
.fab{position:fixed;right:.8rem;bottom:.8rem;display:flex;flex-direction:column;gap:.35rem;z-index:60}
.mapframe{width:100%;height:min(42vh,340px);border:0;border-radius:14px;border:1px solid var(--line);margin:.5rem 0 .7rem}
h4{margin-top:1.05rem;font-size:1.05rem;color:var(--pine)}
code{background:#efe9dc;padding:.05rem .3rem;border-radius:4px;font-size:.88em}
.toc a{display:block;padding:.55rem .7rem;margin:.3rem 0;background:var(--card);border:1px solid var(--line);border-radius:12px;text-decoration:none;color:var(--ink);font-weight:700}
.toc a span{display:block;font-weight:400;color:var(--muted);font-size:.8rem;margin-top:.15rem}
.live-plan{scroll-margin-top:90px}.live-title{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap;margin-bottom:1rem}.live-title span{font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:#c24e00;color:#fff;border-radius:999px;padding:.24rem .6rem}.live-title h2{margin:0}.live-plan .card{border-color:#d6b996}.live-plan .wx{background:linear-gradient(135deg,#edf6f3,#fff8ef)}
"""


def day_shell(did: str, title: str, tags: list[str], body: str) -> str:
    tags_html = "".join(
        f'<span class="tag{" tag-bad" if "CANCEL" in t or "NO noche" in t or "ban" in t.lower() else ""}">{esc(t)}</span>'
        for t in tags
    )
    return f'''<article class="card prose" id="{did}">
<h3>{esc(title)}</h3>
<div class="meta">{tags_html}</div>
{body}
</article>'''


# ---- content builders ----

def build() -> str:
    parts: list[str] = []
    parts.append(f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Guía Lonely Planet · Camper Francia · 6–19 ago 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap top-in">
<div class="brand">Guía camper · Francia verde<small>6–19 agosto 2026 · estilo Lonely Planet · v2026-08-06a (normativa municipal CC)</small></div>
<div class="btns">
<a class="btn btn-p" href="#plan-rapido">Plan lun–mié</a>
<a class="btn btn-g" href="https://www.google.com/maps/dir/Tei%C3%A0,+Spain/Ax-les-Thermes,+France/Seix,+France/Entraygues-sur-Truy%C3%A8re,+France/Le+Lioran,+France/Salers,+France/Nasbinals,+France/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain" target="_blank" rel="noopener">Google Maps ruta</a>
<a class="btn btn-o" href="https://park4night.com/es" target="_blank" rel="noopener">Park4Night</a>
</div></div></header>
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Refugio climático</span><span class="chip">Sunlight 600 + 2 perras</span><span class="chip">P4N ≤15 min</span><span class="chip">Meteo Open-Meteo</span><span class="chip">Normativa municipal CC</span><span class="chip">Plan B por día</span></div>
<h1>Del Pirineo ariégeois al Capcir</h1>
<p class="lead">Guía de viaje completa: normativa municipal de autocaravanas (agosto), meteo por día, opiniones/plan B, P4N auditado, Wikiloc/Visorando y mapas Google.</p>
{img('ax', 'Ax-les-Thermes', 'hero-img')}
<div class="btns">
<a class="btn btn-p" href="#plan-rapido">Plan lun–mié</a>
<a class="btn btn-p" href="#dias">Día a día</a>
<a class="btn" href="#regiones">Regiones</a>
<a class="btn" href="#mapas">Mapas</a>
<a class="btn" href="#p4n">Park4Night</a>
<a class="btn" href="#perras">Regla perras</a>
</div>
</section>
""")

    parts.append(live_three_day_html())

    # reglas
    parts.append("""
<section class="section" id="perras"><h2>Reglas del viaje</h2>
<div class="card prose">
<div class="warn"><strong>Perras:</strong> cualquier sitio con <em>perros prohibidos</em> (chiens interdits) está cancelado. No se deja a las perras en la furgoneta para “hacer la visita”.</div>
<div class="warn"><strong>Pernocta:</strong> leed siempre el último comentario de Park4Night. Si dice noche prohibida / 20h–6h / propiedad privada → no dormir ahí.</div>
<div class="callout"><strong>Meteo + plan B + normativa:</strong> cada día incluye previsión Open-Meteo, opiniones/alternativas y <em>normativa municipal</em> de aparcamiento/pernocta para autocaravanas en agosto. Los carteles in situ prevalecen; revisad meteo a las 7:00.</div>
<ul>
<li><strong>Cancelado noche:</strong> #51675 Cagateille (ban 20:00–6:00 desde 26/7/2026).</li>
<li><strong>Cancelado total:</strong> #98143 Aubrac nature (privado + perros prohibidos); Orlu / #17010.</li>
<li><strong>Horario calor:</strong> hike 7:30–11:30 · sombra 12–17 · paseo corto al atardecer.</li>
</ul>
</div></section>
""")

    # mapas
    parts.append(f"""
<section class="section" id="mapas"><h2>Mapas</h2>
<div class="card prose">
<p>Los iframes usan OpenStreetMap (sin API key). Para navegar de verdad abrid <strong>Google Maps</strong>. Para pernoctas, <strong>Park4Night</strong>.</p>
{links([
 ("Ruta completa Google Maps","https://www.google.com/maps/dir/Tei%C3%A0,+Spain/Ax-les-Thermes,+France/Seix,+France/Entraygues-sur-Truy%C3%A8re,+France/Le+Lioran,+France/Salers,+France/Nasbinals,+France/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain","g"),
 ("Park4Night mapa Francia","https://park4night.com/es/search?lat=44.5&lng=2.5&z=7","o"),
 ("Cómo importar KML a My Maps","https://support.google.com/mymaps/answer/3024836?hl=es","g"),
 ("Descargar ruta.kml","ruta.kml","p"),
])}
<div class="callout"><strong>Google My Maps en 5 min:</strong> crear mapa → nombre <em>FRANCIA AGOSTO 2026</em> → importar <code>ruta.kml</code> (ver enlace de ayuda) → abrir en el móvil (Maps → Tus mapas) y descargar offline.</div>
<div class="warn"><strong>Park4Night carpeta:</strong> entrar por <a href="https://park4night.com/es" target="_blank" rel="noopener">park4night.com/es</a> → favoritos → <code>FRANCIA AGOSTO 2026</code>. El login automático falló; checklist al final.</div>
</div>
<div class="card"><h3>Vista Couserans / Guzet</h3>
<iframe class="mapframe" loading="lazy" title="Couserans" src="https://www.openstreetmap.org/export/embed.html?bbox=1.05%2C42.72%2C1.40%2C42.90&amp;layer=mapnik&amp;marker=42.7876%2C1.3008"></iframe>
{links([("Google Guzet","https://www.google.com/maps/dir/?api=1&destination=42.7876,1.3008&travelmode=driving","g"),("P4N #24616","https://park4night.com/es/place/24616","o")])}
</div>
<div class="card"><h3>Vista Aubrac / Déroc</h3>
<iframe class="mapframe" loading="lazy" title="Aubrac" src="https://www.openstreetmap.org/export/embed.html?bbox=2.94%2C44.55%2C3.10%2C44.71&amp;layer=mapnik&amp;marker=44.63%2C3.02"></iframe>
{links([("Google Déroc","https://www.google.com/maps/dir/?api=1&destination=44.63,3.02&travelmode=driving","g"),("P4N #5073","https://park4night.com/es/place/5073","o")])}
</div>
</section>
""")

    # regiones
    parts.append(f"""
<section class="section" id="regiones"><h2>Regiones · literatura de viaje</h2>

<div class="card prose"><h3>1. Haute Ariège · Ax-les-Thermes</h3>
{img('ax','Ax-les-Thermes')}
<p>{esc(WIKI['ax']['extract'])} El pueblo vive del agua caliente desde la Edad Media: el <strong>Bassin des Ladres</strong> (baño de pies termal, monumento histórico) es un espacio público donde la gente se sienta a remojar los pies mientras charla. Alrededor, hayedos, torrentes y la sombra de las crestas hacia Orgeix y Ascou.</p>
<p><strong>Orlu está cancelado</strong> (perros prohibidos). Vuestra Haute Ariège es la de los bosques y collados abiertos, no la de la reserva.</p>
<p><strong>Qué ver:</strong> paseo del Ariège al atardecer; panadería temprano; Bonascre para coger altura si aprieta el calor; Tournals (#22287) para dormir lejos de las autocaravanas del pueblo.</p>
{links([
 ("Wikipedia Ax", WIKI['ax']['wiki'], "p"),
 ("Bassin des Ladres", WIKI['ladres']['wiki'], "p"),
 ("Google Ax", "https://www.google.com/maps/search/?api=1&query=Ax-les-Thermes", "g"),
 ("OT Pirineos Ariégeois", "https://www.pyrenees-ariegeoises.com/", "w"),
])}
</div>

<div class="card prose"><h3>2. Couserans · Seix, Guzet, Cagateille, Mont Valier</h3>
<div class="photo-grid">{img('cagateille','Cirque de Cagateille')}{img('guzet','Guzet')}</div>
<p>{esc(WIKI['couserans']['extract'])}</p>
<p>El Couserans son dieciocho valles al oeste del Ariège, dominados por el <strong>Mont Valier</strong> (2.838 m). Historia de trashumancia, minería en Biros y pueblos vivos. <strong>Saint-Lizier</strong> (patrimonio) merece una parada corta: catedral y casco sin necesidad de cola.</p>
<p>El <strong>Cirque de Cagateille</strong> es un anfiteatro glaciar clasificado: agua, verde, paredes. Ideal de día con parking <strong>#51675</strong> (solo día). <strong>No dormir ahí</strong> (ban 20h–6h). Pernocta ≤15 min al interés del día: <strong>Cascade d'Ars / Guzet</strong> (#4258, #40904, #24616). Cagateille desde Guzet ~28 min = excepción al criterio ≤15 min.</p>
<p>La <strong>Cascade d'Ars</strong> (cerca de Aulus) es una de las cascadas más fotografiadas del Pirineo ariégeois: id temprano.</p>
{links([
 ("Wikipedia Cagateille", WIKI['cagateille']['wiki'], "p"),
 ("OT Couserans", "https://www.tourisme-couserans-pyrenees.com/", "w"),
 ("Wikiloc Cagateille (Moderado)","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020","wiki"),
 ("Visorando Cagateille", "https://www.visorando.com/randonnee-cirque-de-cagateille/", "w"),
 ("Komoot Cagateille", "https://www.komoot.com/es-es/highlight/6134573", "w"),
])}
</div>

<div class="card prose"><h3>3. Puente · Entraygues / Lot–Truyère</h3>
{img('entraygues','Entraygues-sur-Truyère')}
<p>{esc(WIKI['entraygues']['extract'])} Día de transición: no lo convirtáis en visita turística interminable. El valle puede calentar; priorizad llegar a cota fresca al día siguiente (Lioran).</p>
{links([("Google Entraygues","https://www.google.com/maps/search/?api=1&query=Entraygues-sur-Truy%C3%A8re","g"),("P4N #208568","https://park4night.com/en/place/208568","o")])}
</div>

<div class="card prose"><h3>4. Cantal · Le Lioran, crestas, Salers</h3>
<div class="photo-grid">{img('lioran','Le Lioran')}{img('salers','Salers')}</div>
<p>{esc(WIKI['lioran']['extract'])} El Cantal es un estratovolcán desmantelado: pastos, burones, queso AOP y basalto. El <strong>Bec de l'Aigle</strong> (~1.700 m) es vuestra jornada estrella: bosque, pasto, senda marcada, sin alpinismo técnico.</p>
<p>{esc(WIKI['salers']['extract'])} En agosto, Salers a mediodía es un embudo: visitad temprano o al atardecer y dormid fuera (Ferme Fouey / hierba).</p>
<p>El <strong>Puy Mary</strong> (1.783 m) es el belvedere famoso; no hace falta coronarlo si el parking es un caos — el Bec de l'Aigle ya da la experiencia volcánica.</p>
{links([
 ("Wikipedia Lioran", WIKI['lioran']['wiki'], "p"),
 ("Wikiloc Bec + Téton (Moderado)","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058","wiki"),
 ("Topo Bec de l'Aigle (Moyenne)","https://www.visorando.com/randonnee-le-teton-de-venus-au-dessus-du-lioran/","w"),
 ("Wikipedia Salers", WIKI['salers']['wiki'], "p"),
 ("OT Salers", "https://www.salers-tourisme.fr/", "w"),
])}
</div>

<div class="card prose"><h3>5. Aubrac · meseta, Déroc, Compostela</h3>
<div class="photo-grid">{img('aubrac','Aubrac')}{img('deroc','Cascada del Déroc')}</div>
<p>{esc(WIKI['aubrac']['extract'])}</p>
<p>La <strong>cascada del Déroc</strong> (~32 m) cae sobre una falla de órganos basálticos; detrás hay una pequeña cueva. Es el icono natural de la meseta. Pernocta en <strong>#5073</strong>. El spot nature #98143 está <strong>cancelado</strong> (privado + perros).</p>
<p>Patous frecuentes: protocolo estricto. El GR 65 (Compostela) cruza Nasbinals: usad trozos bonitos, no hace falta “hacer el camino”.</p>
{links([
 ("Wikipedia Déroc", WIKI['deroc']['wiki'], "p"),
 ("Wikiloc Cascada del Déroc (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479","wiki"),
 ("Turismo Lozère Déroc", "https://www.lozere-tourisme.com/patrimoine-naturel/la-cascade-du-deroc/", "w"),
 ("Visorando Cascada del Déroc", "https://www.visorando.com/randonnee-nasbinals-cascade-du-deroc/", "w"),
 ("PNR Aubrac", "https://www.parc-naturel-aubrac.fr/", "w"),
])}
</div>

<div class="card prose"><h3>6. Capcir · Formiguères, Matemale, Camporells</h3>
<div class="photo-grid">{img('formigueres','Formiguères')}{img('matemale','Lac de Matemale')}</div>
<p>{esc(WIKI['formigueres']['extract'])}</p>
<p>{esc(WIKI['capcir']['extract'])} Los <strong>lagos de Camporells</strong> quedan fuera del criterio moderado (fichas Visorando = Difficile, ~800 m D+). Prioridad: <strong>lago de Matemale / Forêt de la Matte</strong> (fácil, perros OK). Evitad reservas naturales catalanas vecinas (perros prohibidos).</p>
{links([
 ("Wikipedia Formiguères", WIKI['formigueres']['wiki'], "p"),
 ("Wikiloc Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412","wiki"),
 ("Visorando bucle Matemale (fácil)","https://www.visorando.com/randonnee-boucle-depuis-le-lac-de-matemale/","w"),
 ("OT Pirineo Cerdanya", "https://www.pyrenees-cerdagne.com/", "w"),
])}
</div>
</section>
""")

    # day nav
    parts.append(
        '<nav class="day-nav">'
        + "".join(f'<a href="#d{i}">{i}<span>día</span></a>' for i in range(1, 15))
        + '</nav>'
        + '<div class="callout"><strong>Criterio de dificultad:</strong> Wikiloc y Visorando solo <em>Fácil/Facile</em> o <em>Moderado/Moyenne</em>. Rechazado ejemplo: <a href="https://es.wikiloc.com/rutas-senderismo/col-de-la-core-7866059" target="_blank" rel="noopener">Col de la Core #7866059</a> (Muy difícil, +1.488 m).</div>'
        + '<section class="section" id="dias"><h2>Itinerario día a día</h2>'
    )

    # DAYS

    # Criterio P4N: parking ≥4 · camping/pago >4 · pernocta OK ≤2 años · ≤15 min coche al interés del día
    parts.append(day_shell("d1", "Día 1 · Jueves 6 — Teià → Ax-les-Thermes",
        ["~180 km / 2h15", "P4N #297295", "P4N #94127", "P4N #22287", "≤15 min"],
        f"""
{day_context_html(1)}
{img('ax','Llegada a Ax')}
<p>Salís de Teià sin prisa. Objetivo: Haute Ariège con luz de tarde.</p>
<div class="callout"><strong>Filtro P4N:</strong> nota ≥4 (camping/pago &gt;4) · pernocta OK en comentarios ≤2 años · <strong>≤15 min en coche</strong> del P4N al interés del día.</div>
<h4>Dónde dormir · ≤15 min coche → Ax / Ladres</h4>
<p>Orden por tiempo al centro / Bassin des Ladres:</p>
<ul>
  <li><strong>#297295 Savignac Route d'Espagne</strong> (4.38/5) — ~4 min · noche OK 2024–26.</li>
  <li><strong>#94127 Orgeix La Payssière</strong> (4.47/5) — ~6 min · río; mirad carteles (algunos comentan límite/camping).</li>
  <li><strong>#22287 Tournals</strong> (4.35/5) — ~13 min · nature, acceso estrecho, noche OK 2024–26.</li>
</ul>
<p><em>Descartados (&gt;15 min o nota baja):</em> #152052 Bonascre (~15–16 min), #101924 Ascou (~21 min), #7266 Aire Ax (2.4/5).</p>
{quote('DDlaPRALINE','06/06/2024','Hay un cartel que indica que el aparcamiento es para una sola noche.','P4N #22287')}
{quote('jackhyde','26/06/2023','La zona está después de la barrera (el cable): recordad cerrarla al pasar.','P4N #22287')}

<div class="trail">
<h4>Paseo al llegar · ribera Ariège + Bassin des Ladres</h4>
<p><strong>Tiempo coche → Ax / Ladres:</strong> #297295 ~4 min · #94127 ~6 min · #22287 ~13 min.</p>
{parking_routes("Ax / Ladres", ("#297295", (1.8148, 42.7300)), (1.8393, 42.7194), [("#94127", (1.8698, 42.7067)), ("#22287", (1.8216, 42.7056))], "driving", "driving")}
{links([
 ("P4N #297295 Savignac","https://park4night.com/es/place/297295","o"),
 ("P4N #94127 Orgeix","https://park4night.com/es/place/94127","o"),
 ("P4N #22287 Tournals","https://park4night.com/es/place/22287","o"),
])}
</div>
{poi_extra("Ax-les-Thermes", [
  "<strong>Baño termal:</strong> Bassin des Ladres (pies; perras fuera del vaso).",
  "<strong>Baño en río:</strong> Ariège (picnic aguas arriba).",
  "<strong>Monumento:</strong> centro termal / casino.",
  "<strong>Compra:</strong> pan y quesos del Ariège en el pueblo.",
], [
 ("Google Bassin des Ladres","https://www.google.com/maps/search/?api=1&query=Bassin+des+Ladres+Ax-les-Thermes","g"),
 ("Google Ariège picnic","https://www.google.com/maps/search/?api=1&query=Ari%C3%A8ge+baignade+Ax-les-Thermes","g"),
 ("Google centro Ax","https://www.google.com/maps/search/?api=1&query=Ax-les-Thermes+centre","g"),
 ("Wikipedia Ladres", WIKI['ladres']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d2", "Día 2 · Viernes 7 — Bosques Orgeix (apto con perras)",
        ["Local", "P4N #94127", "P4N #20472", "P4N #22280", "Orlu trails CANCEL", "≤15 min"],
        f"""
{day_context_html(2)}
{img('ladres','Ax y alrededores')}
<p>Día 100 % con perras. <strong>Senderos de la reserva Orlu cancelados</strong> (perros prohibidos). Interés: valle / picnic Orgeix.</p>
<h4>Dónde dormir · ≤15 min coche → Orgeix (La Payssière)</h4>
<ul>
  <li><strong>#94127 Orgeix La Payssière</strong> (4.47/5) — 0 min · al lado del interés; verificad carteles.</li>
  <li><strong>#20472 Camping municipal Les Ioules***</strong> (4.39/5, camping &gt;4) — ~2 min · servicio completo.</li>
  <li><strong>#22280 Orlu D22</strong> (4.40/5) — ~5 min · parking noche OK; <em>no</em> entrar en reserva Orlu con perras.</li>
</ul>
<p><em>Descartados (&gt;15 min a Orgeix):</em> #22287 Tournals (~17 min), #152052, #101924.</p>

<div class="trail">
<h4>Sendero A · Orgeix (Moyenne · ~8,5 km)</h4>
{wikiloc_box([("Orgeix (Moderado)","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983")])}
<p>Confirmad que el track <strong>no entra en reserva Orlu</strong>.</p>
<p><strong>Tiempo coche → Orgeix Payssière:</strong> #94127 0 min · #20472 ~2 min · #22280 ~5 min.</p>
{parking_routes("Orgeix La Payssière", ("#94127", (1.8698, 42.7067)), (1.8698, 42.7067), [("#20472", (1.8831, 42.7032)), ("#22280", (1.8966, 42.6963))], "walking", "driving")}
{links([
 ("Visorando Ax–Orgeix","https://www.visorando.com/randonnee-d-ax-les-thermes-a-orgeix/","w"),
 ("Wikiloc Orgeix","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983","wiki"),
 ("P4N #94127","https://park4night.com/es/place/94127","o"),
 ("P4N #20472 Les Ioules","https://park4night.com/es/place/20472","o"),
 ("P4N #22280","https://park4night.com/es/place/22280","o"),
])}
</div>
<div class="trail">
<h4>Sendero B · Solo sombra (calor)</h4>
<p>6–8 km ribera Orgeix / pistas locales sin entrar en Orlu. Siesta 12–17 h.</p>
</div>
{poi_extra("Ax / Orgeix", [
  "<strong>Bosque/río:</strong> valle de Orgeix.",
  "<strong>Baño natural:</strong> Ariège picnic.",
  "<strong>Pueblo:</strong> Orgeix (no Ascou si queréis ≤15 min desde esta base).",
  "<strong>Compra:</strong> pan/quesos en Ax antes.",
], [
 ("Google Orgeix","https://www.google.com/maps/search/?api=1&query=Orgeix+Ari%C3%A8ge","g"),
 ("Google Ariège picnic","https://www.google.com/maps/search/?api=1&query=Ari%C3%A8ge+picnic+Ax","g"),
])}
"""))

    parts.append(day_shell("d3", "Día 3 · Sábado 8 — Ax → Foix corta → Couserans (Guzet)",
        ["~120–140 km", "P4N #24616", "P4N #40904", "P4N #82429", "≤15 min"],
        f"""
{day_context_html(3)}
<div class="photo-grid">{img('foix','Château de Foix')}{img('saint_lizier','Saint-Lizier')}</div>
<p>Foix corta → Saint-Lizier → base Guzet. Interés del atardecer: <strong>belvedere Guzet / Aulus</strong> (cumple ≤15 min). <strong>No #51675 de noche.</strong></p>
<h4>Dónde dormir · ≤15 min coche → Guzet Prat-Mataou</h4>
<ul>
  <li><strong>#24616 Guzet Prat-Mataou</strong> (4.54/5) — 0 min · noche OK 2024–26.</li>
  <li><strong>#40904 Ustou D68</strong> (4.37/5) — ~1 min · parking.</li>
  <li><strong>#82429 Camping le Montagnou</strong> (4.52/5, camping &gt;4) — ~14 min · Ustou / Trein.</li>
</ul>
<p><em>Descartados para este interés (&gt;15 min a Guzet):</em> #4433 Bouries (~32 min), #6527 Col de la Core (~41 min).</p>
<div class="callout"><strong>Alternativa Bethmale:</strong> si preferís lago al atardecer, dormid en <a href="https://park4night.com/es/place/200908" target="_blank" rel="noopener">#200908</a> / <a href="https://park4night.com/es/place/6527" target="_blank" rel="noopener">#6527</a> (≤15 min a Bethmale) y al día 4 relocad a Guzet/Ars por la mañana.</div>
{quote('Leptitromain','25/07/2026','Pasamos una noche tranquila en este parking con vistas a las montañas y al pueblo de Aulus-les-Bains.','P4N #24616')}

<div class="trail">
<h4>Atardecer · Guzet / Aulus (corto)</h4>
<p><strong>Tiempo coche → Guzet:</strong> #24616 0 min · #40904 ~1 min · #82429 ~14 min.</p>
{parking_routes("Guzet Prat-Mataou", ("#24616", (1.3008, 42.7876)), (1.3008, 42.7876), [("#40904", (1.3031, 42.7788)), ("#82429", (1.2562, 42.8115))], "walking", "driving")}
{wikiloc_box([("Lac de Bethmale (Fácil) — solo si base Bethmale","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944")])}
{links([
 ("P4N #24616 Guzet","https://park4night.com/es/place/24616","o"),
 ("P4N #40904 Ustou D68","https://park4night.com/es/place/40904","o"),
 ("P4N #82429 Montagnou","https://park4night.com/es/place/82429","o"),
])}
</div>
{poi_extra("Couserans", [
  "<strong>Mirador:</strong> Guzet Prat-Mataou.",
  "<strong>Pueblo termal:</strong> Aulus-les-Bains.",
  "<strong>Monumento:</strong> Saint-Lizier (catedral).",
  "<strong>Opcional lago:</strong> Bethmale (otra base P4N).",
], [
 ("Google Guzet","https://www.google.com/maps/search/?api=1&query=Guzet-Neige","g"),
 ("Google Aulus-les-Bains","https://www.google.com/maps/search/?api=1&query=Aulus-les-Bains","g"),
 ("Google Saint-Lizier","https://www.google.com/maps/search/?api=1&query=Saint-Lizier","g"),
 ("Wikipedia Saint-Lizier", WIKI['saint_lizier']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d4", "Día 4 · Domingo 9 — Cascade d'Ars (+ Cagateille opcional)",
        ["Local", "P4N #4258", "P4N #40904", "P4N #24616", "#51675 solo DÍA", "≤15 min"],
        f"""
{day_context_html(4)}
{img('cagateille','Cirque de Cagateille')}
<div class="warn"><strong>#51675 NO DORMIR</strong> (ban 20:00–6:00 desde 26/7/2026). Solo aparcamiento de día.</div>
<p>Interés que cumple ≤15 min desde pernocta: <strong>Cascade d'Ars</strong>. Cagateille desde Guzet son ~28 min → <em>fuera de criterio</em>; solo si aceptáis la excepción (parking día #51675).</p>
<h4>Dónde dormir · ≤15 min coche → Cascade d'Ars</h4>
<ul>
  <li><strong>#4258 Aulus Jouges</strong> (4.03/5, camping/pago &gt;4) — ~1 min al trailhead · noches OK en reseñas.</li>
  <li><strong>#40904 Ustou D68</strong> (4.37/5) — ~13 min.</li>
  <li><strong>#24616 Guzet Prat-Mataou</strong> (4.54/5) — ~14 min.</li>
</ul>
<p><em>Descartados (&gt;15 min a Ars):</em> #4433, #6527.</p>

<div class="trail">
<h4>Plan A · Cascade d'Ars (salida 7:30)</h4>
{wikiloc_box([("Cascada d'Ars (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596")])}
<p><strong>Tiempo coche → trailhead Ars:</strong> #4258 ~1 min · #40904 ~13 min · #24616 ~14 min.</p>
{parking_routes("Cascade d'Ars", ("#4258", (1.3357, 42.7892)), (1.3382, 42.7875), [("#40904", (1.3031, 42.7788)), ("#24616", (1.3008, 42.7876))], "driving", "driving")}
{links([
 ("Wikiloc Cascada d'Ars","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596","wiki"),
 ("Visorando Cascada d'Ars","https://www.visorando.com/randonnee-la-cascade-d-ars-2/","w"),
 ("P4N #4258","https://park4night.com/es/place/4258","o"),
 ("P4N #40904","https://park4night.com/es/place/40904","o"),
 ("P4N #24616","https://park4night.com/es/place/24616","o"),
])}
</div>
<div class="trail">
<h4>Plan B · Cirque de Cagateille (excepción ~28 min desde Guzet)</h4>
{wikiloc_box([("Cirque de Cagateille (Moderado · ~5 km)","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020")])}
<p>Parking día <strong>#51675 Coulantic</strong> (0 min al inicio). Volved a dormir a #4258 / #40904 / #24616.</p>
{links([
 ("Wikiloc Cagateille","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020","wiki"),
 ("Visorando Cagateille","https://www.visorando.com/randonnee-cirque-de-cagateille/","w"),
 ("P4N #51675 (solo día)","https://park4night.com/es/place/51675","o"),
])}
</div>
{poi_extra("Couserans / Aulus", [
  "<strong>Cascada:</strong> Cascade d'Ars.",
  "<strong>Circo (opcional):</strong> Cirque de Cagateille.",
  "<strong>Pueblo termal:</strong> Aulus-les-Bains.",
  "<strong>Mirador:</strong> Guzet.",
], [
 ("Google Cascade d'Ars","https://www.google.com/maps/search/?api=1&query=Cascade+d%27Ars+Aulus","g"),
 ("Google Cirque de Cagateille","https://www.google.com/maps/search/?api=1&query=Cirque+de+Cagateille","g"),
 ("Google Aulus-les-Bains","https://www.google.com/maps/search/?api=1&query=Aulus-les-Bains","g"),
])}
{img('aulus','Aulus-les-Bains')}
"""))

    parts.append(day_shell("d5", "Día 5 · Lunes 10 — Traslado hacia el Macizo Central",
        ["~220–260 km", "P4N #208568", "P4N #415568", "P4N #8417", "≤15 min"],
        f"""
{day_context_html(5)}
{img('entraygues','Entraygues-sur-Truyère')}
<p>Día de carretera. Interés al llegar: centro Entraygues / Lot.</p>
<h4>Dónde dormir · ≤15 min (a pie) → centro</h4>
<p><strong>#208568 Faubourg de Truyère</strong> (4.5/5) — ~2 min a pie / ~0,7 km, noche OK 2025–26. Si está lleno:</p>
<ul>
  <li><strong>#415568 Aire Lot / Pont Notre Dame</strong> (4.5/5) — ~3 min / ~1,4 km, noche OK 2024–26.</li>
  <li><strong>#8417 Camping Val de Saures***</strong> (4.36/5, camping &gt;4) — ~4 min / ~1,8 km, río + piscina, perros OK.</li>
</ul>
<p><em>Descartado:</em> #5896 Rue de la Grave (3.27/5).</p>
{quote('Pom35','21/05/2026','Nuit très calme.','P4N #208568')}

<div class="trail">
<h4>Paseo corto al llegar (3–5 km)</h4>
<p><strong>A pie → centro:</strong> #208568 ~2 min · #415568 ~3 min · #8417 ~4 min (todos ≪15 min).</p>
{parking_routes("centro Entraygues", ("#208568", (2.5667, 44.6488)), (2.5675, 44.6472), [("#415568", (2.5692, 44.6406)), ("#8417", (2.5639, 44.6421))], "walking", "walking")}
{links([
 ("P4N #208568","https://park4night.com/en/place/208568","o"),
 ("P4N #415568 Aire Lot","https://park4night.com/es/place/415568","o"),
 ("P4N #8417 Val de Saures","https://park4night.com/es/place/8417","o"),
 ("Wikipedia Entraygues", WIKI['entraygues']['wiki'], "p"),
])}
</div>
{poi_extra("Entraygues", [
  "<strong>Baño vigilado:</strong> Piscine d'Entraygues.",
  "<strong>Baño natural:</strong> Lot (Val de Saures).",
  "<strong>Paisaje:</strong> Confluence Lot–Truyère.",
  "<strong>Quesería:</strong> Fromagerie Jean Mathieu (La Borie de Banroques).",
], [
 ("Google Piscine d'Entraygues","https://www.google.com/maps/search/?api=1&query=Piscine+d%27Entraygues","g"),
 ("Google Val de Saures playa","https://www.google.com/maps/search/?api=1&query=Camping+Val+de+Saures+Entraygues+plage","g"),
 ("Google Confluence Lot–Truyère","https://www.google.com/maps/search/?api=1&query=Confluence+Lot+Truy%C3%A8re+Entraygues","g"),
 ("Google Fromagerie Jean Mathieu","https://www.google.com/maps/search/?api=1&query=Fromagerie+Jean+Mathieu+Banroques","g"),
])}
<p>Cena temprana.</p>
"""))

    parts.append(day_shell("d6", "Día 6 · Martes 11 — Llegada a Le Lioran",
        ["~120–150 km", "P4N #13709", "P4N #42476", "P4N #6003", "≤15 min"],
        f"""
{day_context_html(6)}
{img('lioran','Le Lioran')}
<h4>Dónde dormir · ≤15 min coche → inicio Bec de l'Aigle</h4>
<ul>
  <li><strong>#13709 Combe Nègre</strong> (4.11/5) — ~5 min · noche OK 2024–26.</li>
  <li><strong>#42476 Saint-Jacques D67</strong> (4.56/5) — ~4 min · noche calma en reseñas.</li>
  <li><strong>#6003 Camping des Blats</strong> (4.74/5, camping &gt;4) — ~7 min.</li>
</ul>
<p><em>Descartado (&gt;15 min):</em> #27677 Lavigerie (~30 min al Bec).</p>
{quote('SoSoPhil','24/06/2026','Bonito sitio… pasamos 2 noches en calma… hay punto de agua frente al restaurante.','P4N #13709')}
{quote('SLMFC','16/07/2026','Noche del 15 al 16 de julio: rincón agradable y tranquilo entre los abetos.','P4N #13709')}

<div class="trail">
<h4>Aclimatación · 5–8 km + localizar inicio Bec</h4>
<p><strong>Tiempo coche → Font d'Alagnon / inicio Bec:</strong> #42476 ~4 min · #13709 ~5 min · #6003 ~7 min.</p>
{parking_routes("inicio Bec", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#42476", (2.7295, 45.0804)), ("#6003", (2.7137, 45.0522))], "driving", "driving")}
{links([
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
 ("P4N #42476","https://park4night.com/es/place/42476","o"),
 ("P4N #6003","https://park4night.com/es/place/6003","o"),
 ("OT Lioran","https://www.lelioran.com/","w"),
])}
<div class="wikiloc-box">
<strong>Wikiloc · útil mañana</strong>
<div class="btns">
<a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058" target="_blank" rel="noopener">Wikiloc · Bec + Téton (~8 km)</a>
<a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228" target="_blank" rel="noopener">Wikiloc · Bec corto (~5,6 km)</a>
</div>
</div>
</div>
{poi_extra("Le Lioran / Volcanes", [
  "<strong>Salida:</strong> Font d'Alagnon.",
  "<strong>Mirador:</strong> Rocher du Bec de l'Aigle.",
  "<strong>Quesería:</strong> Fromagerie du Cantal (Le Lioran).",
  "<strong>Belvedere:</strong> Puy Mary (opcional).",
], [
 ("Google Font d'Alagnon","https://www.google.com/maps/search/?api=1&query=Font+d%27Alagnon+Le+Lioran","g"),
 ("Google Bec de l'Aigle","https://www.google.com/maps/search/?api=1&query=Rocher+du+Bec+de+l%27Aigle","g"),
 ("Google Fromagerie du Cantal","https://www.google.com/maps/search/?api=1&query=Fromagerie+du+Cantal+Le+Lioran","g"),
 ("Google Puy Mary","https://www.google.com/maps/search/?api=1&query=Puy+Mary","g"),
])}
"""))

    parts.append(day_shell("d7", "Día 7 · Miércoles 12 — Bec de l'Aigle (moderada Visorando)",
        ["0 km coche", "P4N #13709", "P4N #42476", "P4N #6003", "Meteo 7:00", "≤15 min"],
        f"""
{day_context_html(7)}
{img('puy_mary','Macizo del Cantal / Puy Mary')}
<p>Crestas <strong>Moyenne</strong>. Decisión meteo 7:00.</p>
<h4>Dónde dormir · mismos spots (≤15 min al Bec)</h4>
<p>#42476 (~4 min) → #13709 (~5 min) → #6003 (~7 min). Sin #27677.</p>

<div class="trail">
<h4>Plan A · Font d'Alagnon → Bec → Téton</h4>
{wikiloc_box([
 ("Bec + Téton (Moderado · ~8 km)","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058"),
 ("Bec corto (Fácil · ~5,6 km)","https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228"),
])}
{parking_routes("Font d'Alagnon (inicio Bec)", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#42476", (2.7295, 45.0804)), ("#6003", (2.7137, 45.0522))], "driving", "driving")}
{links([
 ("Wikiloc Bec + Téton","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058","wiki"),
 ("Visorando Téton + Bec","https://www.visorando.com/randonnee-le-teton-de-venus-au-dessus-du-lioran/","w"),
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
 ("P4N #42476","https://park4night.com/es/place/42476","o"),
 ("P4N #6003","https://park4night.com/es/place/6003","o"),
])}
</div>
<div class="trail"><h4>Plan B · meteo</h4><p>Téléphérique + paseo corto, o bosque 6–8 km. Bajad antes de tormentas.</p></div>
{poi_extra("Cantal / Bec", [
  "<strong>Mirador:</strong> Bec de l'Aigle (~1.700 m).",
  "<strong>Belvedere:</strong> Puy Mary (si no hay masificación).",
  "<strong>Quesería:</strong> Fromagerie du Cantal.",
  "<strong>Patous:</strong> correa antes del rebaño.",
], [
 ("Google Bec de l'Aigle","https://www.google.com/maps/search/?api=1&query=Bec+de+l%27Aigle+Le+Lioran","g"),
 ("Google Puy Mary","https://www.google.com/maps/search/?api=1&query=Puy+Mary","g"),
 ("Google Fromagerie Le Lioran","https://www.google.com/maps/search/?api=1&query=Fromagerie+du+Cantal+Le+Lioran","g"),
 ("Wikipedia Puy Mary", WIKI['puy_mary']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d8", "Día 8 · Jueves 13 — Piste Verte → zona Salers",
        ["~70–90 km", "P4N #271257", "P4N #144306", "P4N #114179", "≤15 min"],
        f"""
{day_context_html(8)}
{img('salers','Hacia Salers')}
<p>Piste Verte + base cerca de Salers.</p>
<h4>Dónde dormir · ≤15 min → Salers</h4>
<p><strong>#271257 Ferme Fouey</strong> (4.68/5) — ~6 min, hierba, queso, noche OK 2025–26. Si está lleno:</p>
<ul>
  <li><strong>#144306 Saint-Bonnet estadio</strong> (4.17/5) — ~6 min · noche OK 2024–26.</li>
  <li><strong>#114179 Camping Le Moulin du Teinturier</strong> (4.7/5, camping &gt;4) — ~11 min · perros OK en reseñas.</li>
</ul>
<p><em>Descartado:</em> #855 Salers D680 (3.98/5).</p>
{quote('jeremw','01/06/2026','Pasamos una noche en la granja. Acogida muy cálida… y buen queso de granja.','P4N #271257')}

<div class="trail">
<h4>Zona Salers + Piste Verte</h4>
<p><strong>Tiempo → Salers:</strong> #271257 ~6 min · #144306 ~6 min · #114179 ~11 min.</p>
{parking_routes("Salers", ("#271257", (2.4912, 45.1528)), (2.495, 45.1389), [("#144306", (2.4521, 45.1600)), ("#114179", (2.4232, 45.1162))], "walking", "driving")}
{links([
 ("P4N #271257","https://park4night.com/es/place/271257","o"),
 ("P4N #144306","https://park4night.com/es/place/144306","o"),
 ("P4N #114179 Moulin","https://park4night.com/es/place/114179","o"),
 ("OT Piste Verte","https://tourisme-sumene-artense.com/activites/velo/la-piste-verte/","w"),
])}
</div>
{poi_extra("Salers", [
  "<strong>Pueblo:</strong> Salers (basalto).",
  "<strong>Visita:</strong> Maison de la Salers.",
  "<strong>Queso:</strong> en Ferme Fouey.",
  "<strong>Paseo:</strong> Piste Verte (viaductos/túnel).",
], [
 ("Google Salers","https://www.google.com/maps/search/?api=1&query=Salers+Cantal","g"),
 ("Google Maison de la Salers","https://www.google.com/maps/search/?api=1&query=Maison+de+la+Salers","g"),
 ("Google Piste Verte","https://www.google.com/maps/search/?api=1&query=Piste+Verte+Sum%C3%A8ne+Artense","g"),
])}
"""))

    parts.append(day_shell("d9", "Día 9 · Viernes 14 — Bocage de Salers",
        ["Local", "P4N #271257", "P4N #144306", "P4N #114179", "≤15 min"],
        f"""
{day_context_html(9)}
{img('salers','Salers')}
<p>Salers <strong>temprano</strong> + bocage. Misma base (todos ≤15 min al pueblo).</p>
<h4>Dónde dormir</h4>
<p>#271257 (~6 min) → #144306 (~6 min) → #114179 (~11 min).</p>

<div class="trail">
<h4>Boucle La Montagnoune (~4 km) + pueblo</h4>
{wikiloc_box([("Rutas fáciles cerca de Salers","https://es.wikiloc.com/rutas/senderismo/francia/auvergne-rhone-alpes/salers")])}
{parking_routes("Salers (pueblo)", ("#271257", (2.4912, 45.1528)), (2.495, 45.1389), [("#144306", (2.4521, 45.1600)), ("#114179", (2.4232, 45.1162))], "walking", "driving")}
{links([
 ("Visorando La Montagnoune","https://www.visorando.com/randonnee-la-montagnoune-depuis-salers/","w"),
 ("OT Salers","https://www.salers-tourisme.fr/","w"),
 ("P4N #271257","https://park4night.com/es/place/271257","o"),
])}
</div>
<div class="callout">Mediodía en Salers = masificación.</div>
{poi_extra("Salers / bocage", [
  "<strong>Pueblo monumento:</strong> Salers.",
  "<strong>Maison de la Salers:</strong> degustación.",
  "<strong>Queso:</strong> Ferme Fouey.",
  "<strong>Bocage:</strong> caminos rurales.",
], [
 ("Google Salers","https://www.google.com/maps/search/?api=1&query=Salers+Cantal","g"),
 ("Google Maison de la Salers","https://www.google.com/maps/search/?api=1&query=Maison+de+la+Salers","g"),
 ("Wikipedia Salers", WIKI['salers']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d10", "Día 10 · Sábado 15 — Hacia el Aubrac",
        ["~100–130 km", "P4N #5073", "P4N #48703", "P4N #90343", "#98143 CANCELADO", "≤15 min"],
        f"""
{day_context_html(10)}
{img('aubrac','Meseta del Aubrac')}
<div class="warn"><strong>#98143 cancelado</strong> (privado + perros). <strong>#35527 Camping Nasbinals descartado</strong> (3.89/5 &lt; umbral camping).</div>
<h4>Dónde dormir · ≤15 min → Cascada del Déroc</h4>
<ul>
  <li><strong>#5073 Cascada del Déroc</strong> (4.07/5) — 0 min (cascada a pie ~5–10 min), noche OK 2024–26. Llegad tarde.</li>
  <li><strong>#48703 Buron du Ché</strong> (4.57/5) — ~7 min · parking restaurante, noche en reseñas.</li>
  <li><strong>#90343 Marchastel / Rieutort</strong> (4.76/5) — ~9 min · noche OK 2024–26.</li>
</ul>
{quote('AlbericBoissier','16/07/2025','Sitio ideal, bonitas vistas, parking de hierba… El paseo corto hasta el pie de la cascada merece la pena.','P4N #5073')}
{quote('Ars','15/04/2025','Ideal si vais con compañero de cuatro patas.','P4N #5073')}

<div class="trail">
<h4>Paseo corto · Cascada del Déroc</h4>
<p><strong>Tiempo → cascada:</strong> #5073 a pie · #48703 ~7 min coche · #90343 ~9 min coche.</p>
{parking_routes("Cascada del Déroc", ("#5073", (3.0649, 44.6476)), (3.0649, 44.6476), [("#48703", (3.0735, 44.6723)), ("#90343", (3.1080, 44.6736))], "walking", "driving")}
{links([
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
 ("P4N #48703 Buron du Ché","https://park4night.com/es/place/48703","o"),
 ("P4N #90343 Marchastel","https://park4night.com/es/place/90343","o"),
 ("Wikipedia Déroc", WIKI['deroc']['wiki'], "p"),
])}
</div>
{poi_extra("Aubrac", [
  "<strong>Cascada:</strong> Cascade du Déroc.",
  "<strong>Pueblo:</strong> Nasbinals.",
  "<strong>Lago:</strong> Lac des Salhiens.",
  "<strong>Gastronomía:</strong> aligot / tome.",
], [
 ("Google Cascade du Déroc","https://www.google.com/maps/search/?api=1&query=Cascade+du+Deroc","g"),
 ("Google Nasbinals","https://www.google.com/maps/search/?api=1&query=Nasbinals","g"),
 ("Google Lac des Salhiens","https://www.google.com/maps/search/?api=1&query=Lac+des+Salhiens","g"),
])}
"""))

    parts.append(day_shell("d11", "Día 11 · Domingo 16 — Aubrac a fondo",
        ["Local", "P4N #5073", "P4N #48703", "P4N #90343", "≤15 min"],
        f"""
{day_context_html(11)}
<div class="photo-grid">{img('deroc','Cascada del Déroc')}{img('nasbinals','Nasbinals')}</div>
<p>Meseta: Déroc + Nasbinals / Salhiens. Misma base (interés cascada ≤15 min).</p>
<h4>Dónde dormir</h4>
<p>#5073 (0 min) → #48703 (~7 min) → #90343 (~9 min).</p>

<div class="trail">
<h4>Plan A · Bucle Déroc</h4>
{wikiloc_box([("Cascada del Déroc (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479")])}
<p>Mejor salir a pie desde #5073 a la cascada. Nasbinals pueblo: #5073 ~3 min coche.</p>
{parking_routes("Cascada del Déroc", ("#5073", (3.0649, 44.6476)), (3.0649, 44.6476), [("#48703", (3.0735, 44.6723)), ("#90343", (3.1080, 44.6736))], "walking", "driving")}
{links([
 ("Wikiloc Cascada del Déroc","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479","wiki"),
 ("Visorando Déroc","https://www.visorando.com/randonnee-nasbinals-cascade-du-deroc/","w"),
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
 ("P4N #48703","https://park4night.com/es/place/48703","o"),
 ("P4N #90343","https://park4night.com/es/place/90343","o"),
])}
</div>
<div class="trail"><h4>Plan B · viento / patous</h4><p>Nasbinals + descanso. Abortar si tormenta.</p></div>
{poi_extra("Aubrac / Nasbinals", [
  "<strong>Cascada:</strong> Déroc.",
  "<strong>Lago:</strong> Salhiens.",
  "<strong>Pueblo:</strong> Nasbinals.",
  "<strong>Aligot:</strong> plato típico.",
], [
 ("Google Nasbinals","https://www.google.com/maps/search/?api=1&query=Nasbinals","g"),
 ("Google Lac des Salhiens","https://www.google.com/maps/search/?api=1&query=Lac+des+Salhiens","g"),
])}
"""))

    parts.append(day_shell("d12", "Día 12 · Lunes 17 — Aubrac → Capcir",
        ["~280–320 km", "salir <9:00", "P4N #294842", "P4N #14142", "P4N #2547", "≤15 min"],
        f"""
{day_context_html(12)}
{img('formigueres','Formiguères')}
<p>Traslado largo. Interés al llegar: <strong>Formiguères / Calmazeille</strong> (todos los P4N ≤15 min).</p>
<h4>Dónde dormir · ≤15 min coche → Formiguères</h4>
<ul>
  <li><strong>#294842 Matemale lago</strong> (4.29/5) — ~6 min a Formiguères · 0 min al lago · ojo barrera altura ~2,0–2,2 m.</li>
  <li><strong>#14142 Camping La Devèze***</strong> (4.41/5, camping &gt;4) — ~9 min.</li>
  <li><strong>#2547 Calmazeille</strong> (4.54/5) — ~12 min · parking tierra, noche OK 2024–26.</li>
</ul>
{quote('RouilleP','28/02/2025','Pernocta posible… Gracias al ayuntamiento.','P4N #2547')}

{links([
 ("P4N #294842 Matemale","https://park4night.com/es/place/294842","o"),
 ("P4N #14142 La Devèze","https://park4night.com/es/place/14142","o"),
 ("P4N #2547 Calmazeille","https://park4night.com/es/place/2547","o"),
])}

<div class="trail">
<h4>Excursión suave al llegar</h4>
<p><strong>Opción A:</strong> bosque desde #2547 (~0–12 min según base).</p>
<p><strong>Opción B:</strong> lago Matemale. <strong>Tiempo coche → Matemale:</strong> #294842 0 · #14142 ~13 min · #2547 ~16 min (este último solo si el interés del día es Formiguères, no el lago).</p>
{parking_routes("Formiguères", ("#294842", (2.1044, 42.5655)), (2.1000, 42.5850), [("#14142", (2.0914, 42.6096)), ("#2547", (2.0711, 42.6241))], "driving", "driving")}
{wikiloc_box([("Formiguères · Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412")])}
</div>
{poi_extra("Capcir / Matemale", [
  "<strong>Baño:</strong> zona Ourson (temporada).",
  "<strong>Lago:</strong> Matemale.",
  "<strong>Quesería:</strong> Le Calmadou (Formiguères).",
  "<strong>Granja:</strong> Ferme Pérarnaud.",
], [
 ("Google Ourson Matemale","https://www.google.com/maps/search/?api=1&query=Base+nautique+Ourson+Matemale","g"),
 ("Google Lac de Matemale","https://www.google.com/maps/search/?api=1&query=Lac+de+Matemale","g"),
 ("Google Le Calmadou","https://www.google.com/maps/search/?api=1&query=Le+Calmadou+Formigu%C3%A8res","g"),
 ("Google Ferme Pérarnaud","https://www.google.com/maps/search/?api=1&query=Ferme+P%C3%A9rarnaud+Formigu%C3%A8res","g"),
])}
"""))

    parts.append(day_shell("d13", "Día 13 · Martes 18 — Capcir / Matemale (moderado)",
        ["Local", "P4N #294842", "P4N #348514", "P4N #14142", "día colchón", "≤15 min"],
        f"""
{day_context_html(13)}
{img('matemale','Lago de Matemale')}
<p>Interés del día = <strong>Lac de Matemale</strong>. Solo P4N ≤15 min al lago.</p>
<h4>Dónde dormir</h4>
<ul>
  <li><strong>#294842 Matemale</strong> (4.29/5) — 0 min · barrera altura.</li>
  <li><strong>#348514 La Llagonne D32</strong> (4.33/5) — ~7 min · noche OK en reseñas.</li>
  <li><strong>#14142 La Devèze</strong> (4.41/5 camping) — ~13 min.</li>
</ul>
<p><em>Descartado para este interés:</em> #2547 Calmazeille (~16 min &gt;15).</p>

<div class="trail">
<h4>Plan A · Matemale + Forêt de la Matte</h4>
{wikiloc_box([("Formiguères · Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412")])}
<p><strong>Tiempo coche → Lac de Matemale:</strong> #294842 0 · #348514 ~7 min · #14142 ~13 min.</p>
{parking_routes("Lac de Matemale", ("#294842", (2.1044, 42.5655)), (2.1044, 42.5655), [("#348514", (2.1006, 42.5411)), ("#14142", (2.0914, 42.6096))], "walking", "driving")}
{links([
 ("Wikiloc Lac de l'Olive","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412","wiki"),
 ("Visorando Matemale","https://www.visorando.com/randonnee-boucle-depuis-le-lac-de-matemale/","w"),
 ("P4N #294842","https://park4night.com/es/place/294842","o"),
 ("P4N #348514","https://park4night.com/es/place/348514","o"),
 ("P4N #14142","https://park4night.com/es/place/14142","o"),
 ("Wikipedia Matemale", WIKI['matemale']['wiki'], "p"),
])}
</div>
{poi_extra("Capcir / Matemale", [
  "<strong>Baño:</strong> Ourson.",
  "<strong>Lago:</strong> Matemale.",
  "<strong>Quesos:</strong> Le Calmadou + Ferme Pérarnaud.",
  "<strong>Cancelado:</strong> Camporells (Difficile).",
], [
 ("Google Ourson","https://www.google.com/maps/search/?api=1&query=Base+nautique+Ourson+Matemale","g"),
 ("Google Le Calmadou","https://www.google.com/maps/search/?api=1&query=Le+Calmadou+Formigu%C3%A8res","g"),
 ("Google Ferme Pérarnaud","https://www.google.com/maps/search/?api=1&query=Ferme+P%C3%A9rarnaud+Formigu%C3%A8res","g"),
])}
"""))

    parts.append(day_shell("d14", "Día 14 · Miércoles 19 — Capcir → Teià",
        ["~180–200 km / 2h30–3h", "Regreso"],
        f"""
{day_context_html(14)}
<p>Regreso por Cerdanya / Puigcerdà. Parada cercana recomendada: <strong>Puigcerdà</strong> (café + paseo).</p>
<div class="trail">
<h4>Ruta de regreso</h4>
{links([
 ("Google Formiguères → Teià","https://www.google.com/maps/dir/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain","g"),
 ("Google parada Puigcerdà","https://www.google.com/maps/search/?api=1&query=Puigcerd%C3%A0+centro","g"),
])}
</div>
{poi_extra("Regreso Cerdanya", [
  "<strong>Pueblo:</strong> Puigcerdà.",
  "<strong>Compra:</strong> quesos/embutidos Cerdanya.",
  "<strong>Picnic:</strong> ríos del valle.",
  "<strong>Opcional:</strong> Bellver de Cerdanya.",
], [
 ("Google Puigcerdà","https://www.google.com/maps/search/?api=1&query=Puigcerd%C3%A0","g"),
 ("Google fromagerie Cerdanya","https://www.google.com/maps/search/?api=1&query=fromagerie+Cerdanya","g"),
 ("Google Bellver de Cerdanya","https://www.google.com/maps/search/?api=1&query=Bellver+de+Cerdanya","g"),
])}
<p>Fin de ruta.</p>
"""))


    parts.append("</section>")

    # P4N section
    parts.append("""
<section class="section" id="p4n"><h2>Park4Night · FRANCIA AGOSTO 2026</h2>
<div class="card prose">
<div class="warn"><strong>Login:</strong> <a href="https://park4night.com/es" target="_blank" rel="noopener">park4night.com/es</a> → Mi cuenta → Conectarse. Cuando entre: estrella → carpeta <code>FRANCIA AGOSTO 2026</code>.</div>
<div class="callout"><strong>Criterio:</strong> parking ≥4★ · camping/pago &gt;4★ · pernocta OK en comentarios ≤2 años · <strong>≤15 min en coche</strong> del P4N al interés del día.</div>
<h4>Añadir (noche OK · ≤15 min al interés · auditados)</h4>
<ul>
<li><a href="https://park4night.com/es/place/297295" target="_blank" rel="noopener">#297295</a> Savignac (4.38) · Ax</li>
<li><a href="https://park4night.com/es/place/94127" target="_blank" rel="noopener">#94127</a> Orgeix Payssière (4.47) · Ax/Orgeix</li>
<li><a href="https://park4night.com/es/place/22287" target="_blank" rel="noopener">#22287</a> Tournals (4.35) · Ax</li>
<li><a href="https://park4night.com/es/place/20472" target="_blank" rel="noopener">#20472</a> Les Ioules (4.39) · Orgeix</li>
<li><a href="https://park4night.com/es/place/22280" target="_blank" rel="noopener">#22280</a> Orlu D22 (4.40) · Orgeix</li>
<li><a href="https://park4night.com/es/place/24616" target="_blank" rel="noopener">#24616</a> Guzet (4.54) · Guzet/Ars</li>
<li><a href="https://park4night.com/es/place/40904" target="_blank" rel="noopener">#40904</a> Ustou D68 (4.37) · Guzet/Ars</li>
<li><a href="https://park4night.com/es/place/82429" target="_blank" rel="noopener">#82429</a> Montagnou (4.52) · Guzet</li>
<li><a href="https://park4night.com/es/place/4258" target="_blank" rel="noopener">#4258</a> Aulus Jouges (4.03) · Ars</li>
<li><a href="https://park4night.com/en/place/208568" target="_blank" rel="noopener">#208568</a> Entraygues Faubourg (4.5)</li>
<li><a href="https://park4night.com/es/place/415568" target="_blank" rel="noopener">#415568</a> Aire Lot Entraygues (4.5)</li>
<li><a href="https://park4night.com/es/place/8417" target="_blank" rel="noopener">#8417</a> Val de Saures (4.36)</li>
<li><a href="https://park4night.com/es/place/13709" target="_blank" rel="noopener">#13709</a> Combe Nègre (4.11) · Bec</li>
<li><a href="https://park4night.com/es/place/42476" target="_blank" rel="noopener">#42476</a> St-Jacques D67 (4.56) · Bec</li>
<li><a href="https://park4night.com/es/place/6003" target="_blank" rel="noopener">#6003</a> Camping des Blats (4.74) · Bec</li>
<li><a href="https://park4night.com/es/place/271257" target="_blank" rel="noopener">#271257</a> Ferme Fouey (4.68) · Salers</li>
<li><a href="https://park4night.com/es/place/144306" target="_blank" rel="noopener">#144306</a> Saint-Bonnet (4.17) · Salers</li>
<li><a href="https://park4night.com/es/place/114179" target="_blank" rel="noopener">#114179</a> Moulin du Teinturier (4.7) · Salers</li>
<li><a href="https://park4night.com/es/place/5073" target="_blank" rel="noopener">#5073</a> Cascada del Déroc (4.07)</li>
<li><a href="https://park4night.com/es/place/48703" target="_blank" rel="noopener">#48703</a> Buron du Ché (4.57) · Déroc</li>
<li><a href="https://park4night.com/es/place/90343" target="_blank" rel="noopener">#90343</a> Marchastel (4.76) · Déroc</li>
<li><a href="https://park4night.com/es/place/294842" target="_blank" rel="noopener">#294842</a> Matemale (4.29)</li>
<li><a href="https://park4night.com/es/place/348514" target="_blank" rel="noopener">#348514</a> La Llagonne (4.33) · Matemale</li>
<li><a href="https://park4night.com/es/place/14142" target="_blank" rel="noopener">#14142</a> La Devèze (4.41) · Capcir</li>
<li><a href="https://park4night.com/es/place/2547" target="_blank" rel="noopener">#2547</a> Formiguères (4.54) · Formiguères (no Matemale día 13)</li>
</ul>
<p><strong>No añadir / descartados:</strong> #51675 (ban noche), #98143 (privado+perros), #17010, #3781, <strong>#7266</strong> (2.4), <strong>#5896</strong> (3.27), <strong>#855</strong> (3.98), <strong>#35527</strong> (3.89), #701477 (sin nota), <strong>#101924</strong> Ascou (~21 min Ax), <strong>#152052</strong> Bonascre (~15–16 min Ax), <strong>#27677</strong> Lavigerie (~30 min Bec), <strong>#4433</strong>/<strong>#6527</strong> (lejos de Guzet/Ars).</p>
<p>Opcional carpeta “solo día”: #51675 Cagateille. Opcional Bethmale: #200908 / #6527 (solo si el interés es el lago).</p>
</div></section>
""")

    parts.append("""
<section class="section" id="practico"><h2>Práctico</h2>
<div class="card prose">
<h3>Horario anti-calor</h3>
<ul><li>7:00–7:30 decisión meteo (días 7 y 11)</li>
<li>7:30–11:30 ventana hike</li>
<li>11:30–17:00 camper sombra/cota</li>
<li>17:30–20:00 salida corta</li></ul>
<h3>Patous</h3>
<p>Correa antes del rebaño, rodear, no correr si carga, no fotos de cerca. Cantal y Aubrac.</p>
<h3>Agua</h3>
<p>Autonomía 2–3 días. Bidón extra perras. Llenar en pueblos.</p>
<h3>Fotos</h3>
<p>Las imágenes de esta guía proceden de Wikimedia Commons / Wikipedia (licencias libres). Enlaces a la ficha en cada pie de foto.</p>
</div></section>
<footer class="foot">
<p><strong>Guía Lonely Planet · Ruta camper refugio climático</strong> · 6–19 agosto 2026.</p>
<p>Añadid esta página a la pantalla de inicio del móvil. Abrídla desde el archivo local (doble clic), no desde la vista “código” de GitHub.</p>
</footer></main>
<div class="fab"><a class="btn btn-p" href="#dias">Días</a><a class="btn" href="#mapas">Mapas</a></div>
</body></html>
""")

    return "".join(parts)


def main() -> None:
    html_out = build()
    for name in ("guia-lonely-planet.html", "guia-movil.html"):
        (ROOT / name).write_text(html_out, encoding="utf-8")
    Path("/opt/cursor/artifacts/guia-lonely-planet-francia-agosto-2026.html").write_text(html_out, encoding="utf-8")
    print("written", len(html_out), "bytes")


if __name__ == "__main__":
    main()
