#!/usr/bin/env python3
"""Generate Lonely Planet–style HTML travel guide."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIKI = json.loads((ROOT / "_wiki_cache.json").read_text())


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
<div class="brand">Guía camper · Francia verde<small>6–19 agosto 2026 · estilo Lonely Planet · v2026-08-05b (P4N audit ≥4 · cercanía)</small></div>
<div class="btns">
<a class="btn btn-g" href="https://www.google.com/maps/dir/Tei%C3%A0,+Spain/Ax-les-Thermes,+France/Seix,+France/Entraygues-sur-Truy%C3%A8re,+France/Le+Lioran,+France/Salers,+France/Nasbinals,+France/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain" target="_blank" rel="noopener">Google Maps ruta</a>
<a class="btn btn-o" href="https://park4night.com/es" target="_blank" rel="noopener">Park4Night</a>
</div></div></header>
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Refugio climático</span><span class="chip">Sunlight 600 + 2 perras</span><span class="chip">P4N recondito</span><span class="chip">Solo rutas con perras</span></div>
<h1>Del Pirineo ariégeois al Capcir</h1>
<p class="lead">Guía de viaje completa: literatura de cada zona, fotos, opiniones reales de Park4Night, rutas <strong>Wikiloc</strong> y Visorando/Komoot fáciles o moderadas, lugares de interés y mapas Google.</p>
{img('ax', 'Ax-les-Thermes', 'hero-img')}
<div class="btns">
<a class="btn btn-p" href="#dias">Día a día</a>
<a class="btn" href="#regiones">Regiones</a>
<a class="btn" href="#mapas">Mapas</a>
<a class="btn" href="#p4n">Park4Night</a>
<a class="btn" href="#perras">Regla perras</a>
</div>
</section>
""")

    # reglas
    parts.append("""
<section class="section" id="perras"><h2>Reglas del viaje</h2>
<div class="card prose">
<div class="warn"><strong>Perras:</strong> cualquier sitio con <em>perros prohibidos</em> (chiens interdits) está cancelado. No se deja a las perras en la furgoneta para “hacer la visita”.</div>
<div class="warn"><strong>Pernocta:</strong> leed siempre el último comentario de Park4Night. Si dice noche prohibida / 20h–6h / propiedad privada → no dormir ahí.</div>
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
<p>El <strong>Cirque de Cagateille</strong> es un anfiteatro glaciar clasificado: agua, verde, paredes. Ideal de día. <strong>No dormir en #51675</strong> (ban municipal 20h–6h desde julio 2026). Noche en <strong>Guzet (#24616)</strong> o <strong>Col de la Core (#6527)</strong>.</p>
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

    # Criterio P4N: parking ≥4 · camping/pago >4 · pernocta OK en comentarios ≤2 años · orden por cercanía al interés
    parts.append(day_shell("d1", "Día 1 · Jueves 6 — Teià → Ax-les-Thermes",
        ["~180 km / 2h15", "P4N #22287", "P4N #152052", "P4N #101924"],
        f"""
{img('ax','Llegada a Ax')}
<p>Salís de Teià sin prisa. Objetivo: Haute Ariège con luz de tarde.</p>
<div class="callout"><strong>Filtro P4N:</strong> solo spots con nota ≥4 (camping/pago &gt;4), pernocta confirmada en comentarios ≤2 años, priorizando cercanía al interés del día.</div>
<h4>Dónde dormir (Park4Night) · ordenados por cercanía a Ax / Ladres</h4>
<p><strong>#22287 Tournals</strong> (4.35/5) — nature, acceso estrecho, noche OK 2024–26. Si está lleno:</p>
<ul>
  <li><strong>#152052 Plateau de Bonascre</strong> (4.14/5) — parking alto, noche OK 2024–26 · a Ax: ~9 km coche.</li>
  <li><strong>#101924 Ascou D25</strong> (4.73/5) — parking picnic alto, noche OK 2025–26 · a Ax: ~19 km (más lejos, nota excelente).</li>
</ul>
<p><em>Descartado:</em> #7266 Aire Ax (2.4/5, ruido, muchos 1★ 2026).</p>
{quote('DDlaPRALINE','06/06/2024','Hay un cartel que indica que el aparcamiento es para una sola noche.')}
{quote('jackhyde','26/06/2023','La zona está después de la barrera (el cable): recordad cerrarla al pasar.')}

<div class="trail">
<h4>Paseo al llegar · ribera Ariège + Bassin des Ladres</h4>
<p><strong>Distancia (coche) → Ax / Ladres:</strong> #22287 ~7,6 km · #152052 ~9,1 km · #101924 ~18,7 km.</p>
{parking_routes("Ax / Ladres", ("#22287", (1.8216, 42.7056)), (1.8393, 42.7194), [("#152052", (1.8148, 42.7025)), ("#101924", (1.9875, 42.7330))], "driving", "driving")}
{links([
 ("P4N #22287","https://park4night.com/es/place/22287","o"),
 ("P4N #152052 Bonascre","https://park4night.com/es/place/152052","o"),
 ("P4N #101924 Ascou D25","https://park4night.com/es/place/101924","o"),
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

    parts.append(day_shell("d2", "Día 2 · Viernes 7 — Bosques Ax / Orgeix (apto con perras)",
        ["Local", "P4N #22287", "P4N #152052", "P4N #101924", "Orlu CANCELADO"],
        f"""
{img('ladres','Ax y alrededores')}
<p>Día 100 % con perras. <strong>Orlu cancelado</strong> (perros prohibidos). Interés: bosques Orgeix / Ascou.</p>
<h4>Dónde dormir · cercanos al valle Orgeix / Ascou</h4>
<p>Misma base. Orden por cercanía práctica a Orgeix:</p>
<ul>
  <li><strong>#22287 Tournals</strong> (4.35/5) · a Orgeix: ~15 km coche.</li>
  <li><strong>#152052 Bonascre</strong> (4.14/5) · similar / un poco más lejos por carretera.</li>
  <li><strong>#101924 Ascou D25</strong> (4.73/5) · más alto hacia Ascou/Pailhères (~18+ km a Orgeix), ideal si queréis dormir en altura.</li>
</ul>

<div class="trail">
<h4>Sendero A · Ax → Orgeix (Moyenne · ~8,5 km)</h4>
{wikiloc_box([("Orgeix (Moderado)","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983")])}
<p>Confirmad que el track <strong>no entra en reserva Orlu</strong>.</p>
<p><strong>Distancia (coche) → Orgeix pueblo:</strong> #22287 ~15 km · #152052 ~15–16 km · #101924 ~18+ km.</p>
{parking_routes("Orgeix (pueblo)", ("#22287", (1.8216, 42.7056)), (1.768, 42.718), [("#152052", (1.8148, 42.7025)), ("#101924", (1.9875, 42.7330))], "driving", "driving")}
{links([
 ("Visorando Ax–Orgeix","https://www.visorando.com/randonnee-d-ax-les-thermes-a-orgeix/","w"),
 ("Wikiloc Orgeix","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983","wiki"),
 ("P4N #22287","https://park4night.com/es/place/22287","o"),
 ("P4N #152052","https://park4night.com/es/place/152052","o"),
 ("P4N #101924","https://park4night.com/es/place/101924","o"),
])}
</div>
<div class="trail">
<h4>Sendero B · Solo sombra (calor)</h4>
<p>6–8 km pistas Tournals / Bonascre. Siesta 12–17 h.</p>
</div>
{poi_extra("Ax / Orgeix", [
  "<strong>Bosque/río:</strong> valle de Orgeix.",
  "<strong>Baño natural:</strong> Ariège picnic.",
  "<strong>Pueblo:</strong> Ascou.",
  "<strong>Compra:</strong> pan/quesos en Ax antes de subir.",
], [
 ("Google Orgeix","https://www.google.com/maps/search/?api=1&query=Orgeix+Ari%C3%A8ge","g"),
 ("Google Ascou","https://www.google.com/maps/search/?api=1&query=Ascou+Ari%C3%A8ge","g"),
 ("Google Ariège picnic","https://www.google.com/maps/search/?api=1&query=Ari%C3%A8ge+picnic+Ax","g"),
])}
"""))

    parts.append(day_shell("d3", "Día 3 · Sábado 8 — Ax → Foix corta → Couserans",
        ["~120–140 km", "P4N #24616", "P4N #4433", "P4N #6527", "#51675 NO noche"],
        f"""
<div class="photo-grid">{img('foix','Château de Foix')}{img('saint_lizier','Saint-Lizier')}</div>
<p>Foix corta → Saint-Lizier → collados. <strong>No #51675 de noche.</strong></p>
<h4>Dónde dormir · priorizando cercanía a Cagateille / Ars (mañana)</h4>
<p>Orden por cercanía al Cirque de Cagateille (interés del día 4):</p>
<ul>
  <li><strong>#24616 Guzet Prat-Mataou</strong> (4.54/5) — el más cercano · a Cagateille: ~20 km · noche OK 2024–26.</li>
  <li><strong>#4433 Camping Bouries Couflens</strong> (4.71/5, camping &gt;4) · a Cagateille: ~21 km · río, perros OK.</li>
  <li><strong>#6527 Col de la Core</strong> (4.35/5) — fresco/altitud · a Cagateille: ~33 km (más lejos).</li>
</ul>
{quote('Leptitromain','25/07/2026','Pasamos una noche tranquila en este parking con vistas a las montañas y al pueblo de Aulus-les-Bains.','P4N #24616')}
{quote('nayati64','01/06/2025','Pasamos 3 noches tranquilas. El sitio está limpio: dejémoslo así.','P4N #6527')}

<div class="trail">
<h4>Atardecer · Col / Bethmale</h4>
{wikiloc_box([("Lac de Bethmale (Fácil)","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944")])}
<p><strong>Distancia (coche) → Lac Bethmale:</strong> #24616 ~12 km · #4433 ~12 km · #6527 ~23 km.</p>
{parking_routes("Lac de Bethmale", ("#24616", (1.3008, 42.7876)), (1.25, 42.82), [("#4433", (1.1779, 42.7902)), ("#6527", (1.1049, 42.8590))], "driving", "driving")}
{links([
 ("Wikiloc Lac de Bethmale","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944","wiki"),
 ("P4N #24616","https://park4night.com/es/place/24616","o"),
 ("P4N #4433 Bouries","https://park4night.com/es/place/4433","o"),
 ("P4N #6527","https://park4night.com/es/place/6527","o"),
])}
</div>
{poi_extra("Couserans", [
  "<strong>Lago:</strong> Lac de Bethmale.",
  "<strong>Monumento:</strong> Saint-Lizier (catedral).",
  "<strong>Mirador:</strong> Col de la Core.",
  "<strong>Compra:</strong> productos Couserans en Seix.",
], [
 ("Google Lac de Bethmale","https://www.google.com/maps/search/?api=1&query=Lac+de+Bethmale","g"),
 ("Google Saint-Lizier","https://www.google.com/maps/search/?api=1&query=Saint-Lizier","g"),
 ("Wikipedia Saint-Lizier", WIKI['saint_lizier']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d4", "Día 4 · Domingo 9 — Cagateille de día + Biros / Cascade d'Ars",
        ["Local", "P4N #24616", "P4N #4433", "P4N #6527", "#51675 solo DÍA"],
        f"""
{img('cagateille','Cirque de Cagateille')}
<div class="warn"><strong>#51675 NO DORMIR</strong> (ban 20:00–6:00 desde 26/7/2026). Solo día → volver a Guzet/Couflens/Core.</div>
<h4>Dónde dormir · más cercanos a Cagateille / Cascade d'Ars</h4>
<ul>
  <li><strong>#24616 Guzet</strong> (4.54/5) · a Cagateille ~20 km · a Cascade d'Ars ~4 km.</li>
  <li><strong>#4433 Bouries Couflens</strong> (4.71/5 camping) · a Cagateille ~21 km.</li>
  <li><strong>#6527 Col de la Core</strong> (4.35/5) · a Cagateille ~33 km.</li>
</ul>

<div class="trail">
<h4>Plan A · Cirque de Cagateille</h4>
{wikiloc_box([("Cirque de Cagateille (Moderado · ~5 km)","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020")])}
<p><strong>Distancia (coche) → parking Cagateille:</strong> #24616 ~20 km · #4433 ~21 km · #6527 ~33 km.</p>
{parking_routes("parking Cagateille", ("#24616", (1.3008, 42.7876)), (1.2876, 42.7562), [("#4433", (1.1779, 42.7902)), ("#6527", (1.1049, 42.8590))], "driving", "driving")}
{links([
 ("Wikiloc Cagateille","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020","wiki"),
 ("Visorando Cagateille","https://www.visorando.com/randonnee-cirque-de-cagateille/","w"),
 ("P4N #51675 (solo día)","https://park4night.com/es/place/51675","o"),
])}
</div>
<div class="trail">
<h4>Plan B · Cascade d'Ars (salida 7:30)</h4>
{wikiloc_box([("Cascada d'Ars (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596")])}
<p><strong>Distancia (coche) → Cascade d'Ars:</strong> #24616 ~4 km · #4433 ~21 km · #6527 ~40 km.</p>
{parking_routes("Cascade d'Ars", ("#24616", (1.3008, 42.7876)), (1.31, 42.76), [("#4433", (1.1779, 42.7902)), ("#6527", (1.1049, 42.8590))], "driving", "driving")}
{links([
 ("Wikiloc Cascada d'Ars","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596","wiki"),
 ("Visorando Cascada d'Ars","https://www.visorando.com/randonnee-la-cascade-d-ars-2/","w"),
])}
</div>
{poi_extra("Couserans / Aulus", [
  "<strong>Circo:</strong> Cirque de Cagateille.",
  "<strong>Cascada:</strong> Cascade d'Ars.",
  "<strong>Lago:</strong> Lac de Bethmale.",
  "<strong>Pueblo termal:</strong> Aulus-les-Bains.",
], [
 ("Google Cirque de Cagateille","https://www.google.com/maps/search/?api=1&query=Cirque+de+Cagateille","g"),
 ("Google Cascade d'Ars","https://www.google.com/maps/search/?api=1&query=Cascade+d%27Ars+Aulus","g"),
 ("Google Aulus-les-Bains","https://www.google.com/maps/search/?api=1&query=Aulus-les-Bains","g"),
])}
{img('aulus','Aulus-les-Bains')}
"""))

    parts.append(day_shell("d5", "Día 5 · Lunes 10 — Traslado hacia el Macizo Central",
        ["~220–260 km", "P4N #208568", "P4N #415568", "P4N #8417"],
        f"""
{img('entraygues','Entraygues-sur-Truyère')}
<p>Día de carretera. Interés al llegar: centro Entraygues / Lot.</p>
<h4>Dónde dormir · más cercanos al centro (nota ≥4)</h4>
<p><strong>#208568 Faubourg de Truyère</strong> (4.5/5) — el más cercano (~0,7 km a pie), noche OK 2025–26. Si está lleno:</p>
<ul>
  <li><strong>#415568 Aire Lot / Pont Notre Dame</strong> (4.5/5) — ~1,4 km a pie, noche OK 2024–26 (más plazas/gente).</li>
  <li><strong>#8417 Camping Val de Saures***</strong> (4.36/5, camping &gt;4) — ~1,8 km a pie, río + piscina, perros OK.</li>
</ul>
<p><em>Descartado:</em> #5896 Rue de la Grave (3.27/5, por debajo del umbral).</p>
{quote('Pom35','21/05/2026','Nuit très calme.','P4N #208568')}

<div class="trail">
<h4>Paseo corto al llegar (3–5 km)</h4>
<p><strong>Distancia a pie → centro:</strong> #208568 ~0,7 km · #415568 ~1,4 km · #8417 ~1,8 km.</p>
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
        ["~120–150 km", "P4N #13709", "P4N #6003", "P4N #27677"],
        f"""
{img('lioran','Le Lioran')}
<h4>Dónde dormir · cercanos al inicio Bec de l'Aigle</h4>
<p><strong>#13709 Combe Nègre</strong> (4.11/5) — el más cercano al trailhead (~2,8 km), noche OK 2024–26. Si está lleno:</p>
<ul>
  <li><strong>#6003 Camping des Blats</strong> (4.74/5, camping &gt;4) · a Bec: ~6,4 km — mejor alternativa cercana.</li>
  <li><strong>#27677 Lavigerie D62</strong> (4.29/5) · a Bec: ~30 km — solo si los dos anteriores están llenos (lejos).</li>
</ul>
{quote('SoSoPhil','24/06/2026','Bonito sitio… pasamos 2 noches en calma… hay punto de agua frente al restaurante.')}
{quote('SLMFC','16/07/2026','Noche del 15 al 16 de julio: rincón agradable y tranquilo entre los abetos.')}

<div class="trail">
<h4>Aclimatación · 5–8 km + localizar inicio Bec</h4>
<p><strong>Distancia (coche) → Font d'Alagnon / inicio Bec:</strong> #13709 ~2,8 km · #6003 ~6,4 km · #27677 ~29,7 km.</p>
{parking_routes("inicio Bec", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#6003", (2.7137, 45.0522)), ("#27677", (2.7026, 45.1301))], "driving", "driving")}
{links([
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
 ("P4N #6003","https://park4night.com/es/place/6003","o"),
 ("P4N #27677","https://park4night.com/es/place/27677","o"),
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
        ["0 km coche", "P4N #13709", "P4N #6003", "P4N #27677", "Meteo 7:00"],
        f"""
{img('puy_mary','Macizo del Cantal / Puy Mary')}
<p>Crestas <strong>Moyenne</strong>. Decisión meteo 7:00.</p>
<h4>Dónde dormir · mismos spots (cercanía al Bec)</h4>
<p>#13709 (2,8 km) → #6003 (6,4 km) → #27677 (29,7 km, último recurso).</p>

<div class="trail">
<h4>Plan A · Font d'Alagnon → Bec → Téton</h4>
{wikiloc_box([
 ("Bec + Téton (Moderado · ~8 km)","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058"),
 ("Bec corto (Fácil · ~5,6 km)","https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228"),
])}
{parking_routes("Font d'Alagnon (inicio Bec)", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#6003", (2.7137, 45.0522)), ("#27677", (2.7026, 45.1301))], "driving", "driving")}
{links([
 ("Wikiloc Bec + Téton","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058","wiki"),
 ("Visorando Téton + Bec","https://www.visorando.com/randonnee-le-teton-de-venus-au-dessus-du-lioran/","w"),
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
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
        ["~70–90 km", "P4N #271257", "P4N #144306", "P4N #114179"],
        f"""
{img('salers','Hacia Salers')}
<p>Piste Verte + base cerca de Salers.</p>
<h4>Dónde dormir · cercanos a Salers (nota OK)</h4>
<p><strong>#271257 Ferme Fouey</strong> (4.68/5) — el más cercano razonable (~3,4 km a pie), hierba, queso, noche OK 2025–26. Si está lleno:</p>
<ul>
  <li><strong>#144306 Saint-Bonnet estadio</strong> (4.17/5) · a Salers: ~4,9 km · noche OK 2024–26.</li>
  <li><strong>#114179 Camping Le Moulin du Teinturier</strong> (4.7/5, camping &gt;4) · a Salers: ~10,8 km · perros gratis en reseñas.</li>
</ul>
<p><em>Descartado:</em> #855 Salers D680 (3.98/5, por debajo del umbral).</p>
{quote('jeremw','01/06/2026','Pasamos una noche en la granja. Acogida muy cálida… y buen queso de granja.','P4N #271257')}

<div class="trail">
<h4>Zona Salers + Piste Verte</h4>
<p><strong>Distancia → Salers:</strong> #271257 ~3,4 km a pie · #144306 ~4,9 km coche · #114179 ~10,8 km coche.</p>
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
        ["Local", "P4N #271257", "P4N #144306", "P4N #114179"],
        f"""
{img('salers','Salers')}
<p>Salers <strong>temprano</strong> + bocage. Misma base, orden por cercanía al pueblo.</p>
<h4>Dónde dormir</h4>
<p>#271257 (~3,4 km) → #144306 (~4,9 km) → #114179 (~10,8 km).</p>

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
        ["~100–130 km", "P4N #5073", "P4N #90343", "#98143 CANCELADO"],
        f"""
{img('aubrac','Meseta del Aubrac')}
<div class="warn"><strong>#98143 cancelado</strong> (privado + perros). <strong>#35527 Camping Nasbinals descartado</strong> (3.89/5 &lt; umbral camping).</div>
<h4>Dónde dormir · más cercanos a la Cascada del Déroc</h4>
<p><strong>#5073 Cascada del Déroc</strong> (4.07/5) — 0 km al interés (cascada a ~300–500 m a pie), noche OK 2024–26. Llegad tarde. Si está lleno:</p>
<ul>
  <li><strong>#90343 Marchastel / Rieutort</strong> (4.76/5) — nature · a Déroc: ~5,4 km · noche OK 2024–26.</li>
</ul>
<p>No proponemos un 2º camping lejano: los cercanos con nota suficiente escasean; si ambos llenos, buscad en P4N spots ≥4 a &lt;15 km (evitar #98143).</p>
{quote('AlbericBoissier','16/07/2025','Sitio ideal, bonitas vistas, parking de hierba… El paseo corto hasta el pie de la cascada merece la pena.')}
{quote('Ars','15/04/2025','Ideal si vais con compañero de cuatro patas.')}

<div class="trail">
<h4>Paseo corto · Cascada del Déroc</h4>
<p><strong>Distancia → cascada:</strong> #5073 ~0,3–0,5 km a pie · #90343 ~5,4 km coche + paseo.</p>
{parking_routes("Cascada del Déroc", ("#5073", (3.0649, 44.6476)), (3.0649, 44.6476), [("#90343", (3.1080, 44.6736))], "walking", "driving")}
{links([
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
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
        ["Local", "P4N #5073", "P4N #90343"],
        f"""
<div class="photo-grid">{img('deroc','Cascada del Déroc')}{img('nasbinals','Nasbinals')}</div>
<p>Meseta: Déroc + Nasbinals / Salhiens. Misma base priorizando cercanía a la cascada.</p>
<h4>Dónde dormir</h4>
<p>#5073 (al pie) → #90343 (~5,4 km).</p>

<div class="trail">
<h4>Plan A · Bucle Déroc</h4>
{wikiloc_box([("Cascada del Déroc (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479")])}
<p><strong>Distancia → Nasbinals (inicio GR):</strong> #5073 ~12 km coche / paseo largo · #90343 ~16 km · mejor salir a pie desde #5073 a la cascada.</p>
{parking_routes("Nasbinals", ("#5073", (3.0649, 44.6476)), (3.0, 44.665), [("#90343", (3.1080, 44.6736))], "driving", "driving")}
{links([
 ("Wikiloc Cascada del Déroc","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479","wiki"),
 ("Visorando Déroc","https://www.visorando.com/randonnee-nasbinals-cascade-du-deroc/","w"),
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
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
        ["~280–320 km", "salir <9:00", "P4N #2547", "P4N #14142", "P4N #294842"],
        f"""
{img('formigueres','Formiguères')}
<p>Traslado largo. Interés al llegar: Formiguères / Matemale.</p>
<h4>Dónde dormir · cercanos a Formiguères / lago</h4>
<p>Orden por cercanía a Calmazeille / Formiguères y luego Matemale:</p>
<ul>
  <li><strong>#2547 Calmazeille</strong> (4.54/5) — parking tierra junto lago, noche OK 2024–26 · a Matemale: ~11,6 km.</li>
  <li><strong>#14142 Camping La Devèze***</strong> (4.41/5, camping &gt;4) · a Matemale: ~8,3 km (más cerca del lago).</li>
  <li><strong>#294842 Matemale lago</strong> (4.29/5) — 0 km al lago · ojo barrera altura ~2,0–2,2 m.</li>
</ul>
{quote('RouilleP','28/02/2025','Pernocta posible… Gracias al ayuntamiento.')}

{links([
 ("P4N #2547","https://park4night.com/es/place/2547","o"),
 ("P4N #14142 La Devèze","https://park4night.com/es/place/14142","o"),
 ("P4N #294842 Matemale","https://park4night.com/es/place/294842","o"),
])}

<div class="trail">
<h4>Excursión suave al llegar</h4>
<p><strong>Opción A:</strong> 4–6 km bosque desde #2547 (0 km coche).</p>
<p><strong>Opción B:</strong> lago Matemale. <strong>Distancias coche → Matemale:</strong> #294842 = 0 · #14142 ~8,3 km · #2547 ~11,6 km.</p>
{parking_routes("Lac de Matemale", ("#2547", (2.0711, 42.6241)), (2.1044, 42.5655), [("#14142", (2.0914, 42.6096)), ("#294842", (2.1044, 42.5655))], "driving", "driving")}
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
        ["Local", "P4N #294842", "P4N #14142", "P4N #2547", "día colchón"],
        f"""
{img('matemale','Lago de Matemale')}
<p>Interés del día = <strong>Lac de Matemale</strong>. Orden P4N por cercanía al lago:</p>
<h4>Dónde dormir</h4>
<ul>
  <li><strong>#294842 Matemale</strong> (4.29/5) — 0 km · barrera altura.</li>
  <li><strong>#14142 La Devèze</strong> (4.41/5 camping) · ~8,3 km.</li>
  <li><strong>#2547 Calmazeille</strong> (4.54/5) · ~11,6 km.</li>
</ul>

<div class="trail">
<h4>Plan A · Matemale + Forêt de la Matte</h4>
{wikiloc_box([("Formiguères · Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412")])}
{parking_routes("Lac de Matemale", ("#294842", (2.1044, 42.5655)), (2.1044, 42.5655), [("#14142", (2.0914, 42.6096)), ("#2547", (2.0711, 42.6241))], "walking", "driving")}
{links([
 ("Wikiloc Lac de l'Olive","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412","wiki"),
 ("Visorando Matemale","https://www.visorando.com/randonnee-boucle-depuis-le-lac-de-matemale/","w"),
 ("P4N #294842","https://park4night.com/es/place/294842","o"),
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
<div class="callout"><strong>Criterio:</strong> parking ≥4★ · camping/pago &gt;4★ · pernocta OK en comentarios ≤2 años · priorizar cercanía al interés del día.</div>
<h4>Añadir (noche OK · auditados)</h4>
<ul>
<li><a href="https://park4night.com/es/place/22287" target="_blank" rel="noopener">#22287</a> Tournals (4.35)</li>
<li><a href="https://park4night.com/es/place/152052" target="_blank" rel="noopener">#152052</a> Bonascre (4.14)</li>
<li><a href="https://park4night.com/es/place/101924" target="_blank" rel="noopener">#101924</a> Ascou D25 (4.73)</li>
<li><a href="https://park4night.com/es/place/24616" target="_blank" rel="noopener">#24616</a> Guzet (4.54)</li>
<li><a href="https://park4night.com/es/place/4433" target="_blank" rel="noopener">#4433</a> Bouries Couflens (4.71)</li>
<li><a href="https://park4night.com/es/place/6527" target="_blank" rel="noopener">#6527</a> Col de la Core (4.35)</li>
<li><a href="https://park4night.com/en/place/208568" target="_blank" rel="noopener">#208568</a> Entraygues Faubourg (4.5)</li>
<li><a href="https://park4night.com/es/place/415568" target="_blank" rel="noopener">#415568</a> Aire Lot Entraygues (4.5)</li>
<li><a href="https://park4night.com/es/place/8417" target="_blank" rel="noopener">#8417</a> Val de Saures (4.36)</li>
<li><a href="https://park4night.com/es/place/13709" target="_blank" rel="noopener">#13709</a> Combe Nègre (4.11)</li>
<li><a href="https://park4night.com/es/place/6003" target="_blank" rel="noopener">#6003</a> Camping des Blats (4.74)</li>
<li><a href="https://park4night.com/es/place/27677" target="_blank" rel="noopener">#27677</a> Lavigerie (4.29 · lejos del Bec)</li>
<li><a href="https://park4night.com/es/place/271257" target="_blank" rel="noopener">#271257</a> Ferme Fouey (4.68)</li>
<li><a href="https://park4night.com/es/place/144306" target="_blank" rel="noopener">#144306</a> Saint-Bonnet (4.17)</li>
<li><a href="https://park4night.com/es/place/114179" target="_blank" rel="noopener">#114179</a> Moulin du Teinturier (4.7)</li>
<li><a href="https://park4night.com/es/place/5073" target="_blank" rel="noopener">#5073</a> Cascada del Déroc (4.07)</li>
<li><a href="https://park4night.com/es/place/90343" target="_blank" rel="noopener">#90343</a> Marchastel (4.76)</li>
<li><a href="https://park4night.com/es/place/2547" target="_blank" rel="noopener">#2547</a> Formiguères (4.54)</li>
<li><a href="https://park4night.com/es/place/14142" target="_blank" rel="noopener">#14142</a> La Devèze (4.41)</li>
<li><a href="https://park4night.com/es/place/294842" target="_blank" rel="noopener">#294842</a> Matemale (4.29)</li>
</ul>
<p><strong>No añadir / descartados:</strong> #51675 (ban noche), #98143 (privado+perros), #17010, #3781, <strong>#7266</strong> (2.4), <strong>#5896</strong> (3.27), <strong>#855</strong> (3.98), <strong>#35527</strong> (3.89), #701477 (sin nota).</p>
<p>Opcional carpeta “solo día”: #51675 Cagateille.</p>
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
