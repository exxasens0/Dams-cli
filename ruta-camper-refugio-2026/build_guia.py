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
<div class="brand">Guía camper · Francia verde<small>6–19 agosto 2026 · estilo Lonely Planet · v2026-08-05 (14 días completos)</small></div>
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
{links([("Google Entraygues","https://www.google.com/maps/search/?api=1&query=Entraygues-sur-Truy%C3%A8re","g"),("P4N #5896","https://park4night.com/es/place/5896","o")])}
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
    parts.append(day_shell("d1", "Día 1 · Jueves 6 — Teià → Ax-les-Thermes",
        ["~180 km / 2h15", "P4N #22287", "P4N #152052", "P4N #7266"],
        f"""
{img('ax','Llegada a Ax')}
<p>Salís de Teià sin prisa. El objetivo no es hacer kilómetros heroicos, sino llegar a la Haute Ariège con luz de tarde y cambiar de clima mental: de litoral a valle termal.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#22287 Tournals</strong> (hacia Bonascre): acceso estrecho que filtra autocaravanas, sombra, mesas. Cerrar el cable/hilo al entrar y salir. Si está lleno, alternativas (&gt;2 estrellas, perros OK en reseñas):</p>
<ul>
  <li><strong>#152052 Plateau de Bonascre</strong> (4.1/5) — parking alto, gratis · al centro Ax: ~2,5 km.</li>
  <li><strong>#7266 Aire municipal Ax</strong> (pago) — servicios, perros aceptados · al centro Ax: ~0,8 km.</li>
</ul>
{quote('DDlaPRALINE','06/06/2024','Hay un cartel que indica que el aparcamiento es para una sola noche.')}
{quote('jackhyde','26/06/2023','La zona está después de la barrera (el cable): recordad cerrarla al pasar.')}

<div class="trail">
<h4>Paseo al llegar · ribera Ariège + Bassin des Ladres</h4>
<p><strong>Distancia parking → centro Ax / Ladres:</strong> #22287 ~2,5 km a pie (~30 min) · #152052 ~2,5 km · #7266 ~0,8 km.</p>
<p>Paseo corto 3–5 km por la ribera. <strong>Bassin des Ladres:</strong> ritual termal; las perras se quedan fuera del vaso (paseo perimetral).</p>
{parking_routes("centro Ax / Ladres", ("#22287", (1.8216, 42.7056)), (1.8393, 42.7194), [("#152052", (1.8148, 42.7025)), ("#7266", (1.8345, 42.7215))], "walking", "walking")}
{links([
 ("P4N #22287","https://park4night.com/es/place/22287","o"),
 ("P4N #152052 Bonascre","https://park4night.com/es/place/152052","o"),
 ("P4N #7266 Aire Ax","https://park4night.com/es/place/7266","o"),
 ("Google → Tournals","https://www.google.com/maps/dir/?api=1&destination=42.7056,1.8216&travelmode=driving","g"),
])}
</div>
{poi_extra("Ax-les-Thermes", [
  "<strong>Baño termal:</strong> Bassin des Ladres (pies en agua caliente).",
  "<strong>Baño en río:</strong> Ariège (zonas de picnic aguas arriba del pueblo).",
  "<strong>Monumento:</strong> viejo casino / centro histórico termal.",
  "<strong>Compra local:</strong> panaderías y quesos del Ariège en el pueblo.",
], [
 ("Google Bassin des Ladres","https://www.google.com/maps/search/?api=1&query=Bassin+des+Ladres+Ax-les-Thermes","g"),
 ("Google Ariège (baño/picnic)","https://www.google.com/maps/search/?api=1&query=Ari%C3%A8ge+baignade+Ax-les-Thermes","g"),
 ("Google centro Ax","https://www.google.com/maps/search/?api=1&query=Ax-les-Thermes+centre","g"),
 ("Wikipedia Ladres", WIKI['ladres']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d2", "Día 2 · Viernes 7 — Bosques Ax / Orgeix (apto con perras)",
        ["Local", "P4N #22287", "P4N #152052", "P4N #7266", "Orlu CANCELADO"],
        f"""
{img('ladres','Ax y alrededores')}
<p>Día de aclimatación <strong>100 % con perras</strong>. La reserva de Orlu queda fuera: <strong>perros prohibidos</strong>. Explorad bosques y pistas hacia <strong>Orgeix / Ascou / Tournals</strong>.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p>Misma base que ayer. Si #22287 está lleno:</p>
<ul>
  <li><strong>#152052 Bonascre</strong> (4.1/5) · al inicio Orgeix: ~9 km en coche.</li>
  <li><strong>#7266 Aire Ax</strong> (pago, perros OK) · al inicio Orgeix: ~10 km en coche.</li>
</ul>

<div class="trail">
<h4>Sendero A · Ax → Orgeix (Visorando Moyenne · ~8,5 km · +318 m)</h4>
{wikiloc_box([("Orgeix (Moderado)","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983")])}
<p>Valle lateral menos masificado. Sombra de haya, torrentes. Confirmad en el track que <strong>no entra en la reserva Orlu</strong>.</p>
<p><strong>Distancia parking → inicio ruta (Ax centro):</strong> #22287 ~2,5 km a pie · #152052 ~2,5 km · #7266 ~0,8 km.</p>
<p><strong>Distancia parking → Orgeix (pueblo):</strong> #22287 ~9 km coche · #152052 ~8 km · #7266 ~10 km.</p>
{parking_routes("inicio Orgeix (pueblo)", ("#22287", (1.8216, 42.7056)), (1.768, 42.718), [("#152052", (1.8148, 42.7025)), ("#7266", (1.8345, 42.7215))], "driving", "driving")}
{links([
 ("Visorando Ax–Orgeix (Moyenne)","https://www.visorando.com/randonnee-d-ax-les-thermes-a-orgeix/","w"),
 ("Wikiloc Orgeix (Moderado)","https://es.wikiloc.com/rutas-senderismo/orgeix-142403983","wiki"),
 ("P4N #22287","https://park4night.com/es/place/22287","o"),
 ("P4N #152052","https://park4night.com/es/place/152052","o"),
 ("P4N #7266","https://park4night.com/es/place/7266","o"),
])}
</div>
<div class="trail">
<h4>Sendero B · Solo sombra (plan calor)</h4>
<p>6–8 km de pistas alrededor de Tournals / Bonascre. Siesta en camper 12–17 h. Segunda salida corta al atardecer.</p>
</div>
<div class="callout"><strong>Tip:</strong> bajad el GPX la noche anterior y leed comentarios recientes buscando la palabra <em>chien</em>.</div>
{poi_extra("Ax / Orgeix", [
  "<strong>Bosque/río:</strong> valle de Orgeix (torrentes y sombra).",
  "<strong>Baño natural:</strong> Ariège en zonas de picnic aguas arriba.",
  "<strong>Pueblo:</strong> Ascou (iglesia y paseo corto).",
  "<strong>Compra:</strong> pan y quesos en Ax antes de subir.",
], [
 ("Google Orgeix","https://www.google.com/maps/search/?api=1&query=Orgeix+Ari%C3%A8ge","g"),
 ("Google Ascou","https://www.google.com/maps/search/?api=1&query=Ascou+Ari%C3%A8ge","g"),
 ("Google Ariège picnic","https://www.google.com/maps/search/?api=1&query=Ari%C3%A8ge+picnic+Ax","g"),
])}
"""))

    parts.append(day_shell("d3", "Día 3 · Sábado 8 — Ax → Foix corta → Couserans",
        ["~120–140 km", "P4N #6527", "P4N #24616", "P4N #15419", "#51675 NO noche"],
        f"""
<div class="photo-grid">{img('foix','Château de Foix')}{img('saint_lizier','Saint-Lizier')}</div>
<p>Dejáis Haute Ariège hacia el oeste. <strong>Foix</strong>: parada corta al castillo (foto/mirador). Luego Saint-Girons / Saint-Lizier y subida a collados.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#6527 Col de la Core</strong> (altitud, fresco, noche calma). Si está lleno:</p>
<ul>
  <li><strong>#24616 Guzet Prat-Mataou</strong> (4.3/5) — parking alto, vistas · al Lac Bethmale: ~12 km.</li>
  <li><strong>#15419 Camping le Haut Salat</strong> (Seix, pago) — río Salat, sombra, perros OK · al Bethmale: ~18 km.</li>
</ul>
<p><strong>No #51675 de noche</strong> (ban 20:00–6:00).</p>
{quote('Leptitromain','25/07/2026','Pasamos una noche tranquila en este parking con vistas a las montañas y al pueblo de Aulus-les-Bains.','P4N #24616')}
{quote('nayati64','01/06/2025','Pasamos 3 noches tranquilas. El sitio está limpio: dejémoslo así.','P4N #6527')}

<div class="trail">
<h4>Atardecer · Col de la Core + Lac de Bethmale</h4>
{wikiloc_box([("Lac de Bethmale (Fácil)","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944")])}
<p>El collado (~1.395 m) es hub de GR. Paseo corto o subir al lago Bethmale al día siguiente.</p>
<p><strong>Distancia parking → Bethmale (inicio ruta):</strong> #6527 ~5 km · #24616 ~12 km · #15419 ~18 km.</p>
{parking_routes("Lac de Bethmale", ("#6527", (1.10, 42.84)), (1.25, 42.82), [("#24616", (1.3008, 42.7876)), ("#15419", (1.206, 42.8758))], "driving", "driving")}
{links([
 ("Wikiloc Lac de Bethmale (Fácil)","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944","wiki"),
 ("Visorando Étang de Bethmale (Moyenne)","https://www.visorando.com/randonnee-le-lac-de-bethmale/","w"),
 ("P4N #6527","https://park4night.com/es/place/6527","o"),
 ("P4N #24616","https://park4night.com/es/place/24616","o"),
 ("P4N #15419 Haut Salat","https://park4night.com/es/place/15419","o"),
])}
</div>
{poi_extra("Couserans", [
  "<strong>Lago:</strong> Lac de Bethmale (baño posible en verano, con prudencia).",
  "<strong>Monumento:</strong> Saint-Lizier (catedral y casco).",
  "<strong>Mirador:</strong> Col de la Core al atardecer.",
  "<strong>Compra:</strong> quesos y productos del Couserans en Seix/Saint-Girons.",
], [
 ("Google Lac de Bethmale","https://www.google.com/maps/search/?api=1&query=Lac+de+Bethmale","g"),
 ("Google Saint-Lizier","https://www.google.com/maps/search/?api=1&query=Saint-Lizier","g"),
 ("Google Col de la Core","https://www.google.com/maps/search/?api=1&query=Col+de+la+Core","g"),
 ("Wikipedia Saint-Lizier", WIKI['saint_lizier']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d4", "Día 4 · Domingo 9 — Cagateille de día + Biros / Cascade d'Ars",
        ["Local", "P4N #6527 / #24616", "P4N #15419", "#51675 solo DÍA"],
        f"""
{img('cagateille','Cirque de Cagateille')}
<div class="warn"><strong>#51675 NO DORMIR.</strong> Ban municipal 20:00–6:00 desde 26/7/2026. Id de día y volved a Guzet/Core.</div>
<h4>Dónde dormir (Park4Night)</h4>
<p>Misma base que ayer: <strong>#6527</strong> o <strong>#24616</strong>. Alternativa pago: <strong>#15419 Haut Salat</strong> (Seix, río).</p>

<div class="trail">
<h4>Plan A · Cirque de Cagateille (Facile · ~4 km · +251 m)</h4>
{wikiloc_box([("Cirque de Cagateille (Moderado · ~5 km)","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020")])}
<p>Desde el parking del circo (#51675, solo día): sendero bajo bosque hasta el anfiteatro. Pasarela al centro.</p>
<p><strong>Distancia parking noche → Cagateille:</strong> #6527 ~14 km · #24616 ~8 km · #15419 ~22 km.</p>
{parking_routes("parking Cagateille", ("#6527", (1.10, 42.84)), (1.2876, 42.7562), [("#24616", (1.3008, 42.7876)), ("#15419", (1.206, 42.8758))], "driving", "driving")}
{links([
 ("Wikiloc Cirque de Cagateille (Moderado · ~5 km)","https://es.wikiloc.com/rutas-senderismo/cirque-de-cagateille-18941020","wiki"),
 ("Visorando Circo de Cagateille (Facile)","https://www.visorando.com/randonnee-cirque-de-cagateille/","w"),
 ("P4N #51675 (solo día)","https://park4night.com/es/place/51675","o"),
])}
</div>
<div class="trail">
<h4>Plan B · Cascade d'Ars (Moyenne / Wikiloc Fácil)</h4>
{wikiloc_box([("Cascada d'Ars (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596")])}
<p>Salida <strong>7:30</strong>. Mucha gente a mediodía.</p>
<p><strong>Distancia parking noche → Cascade d'Ars:</strong> #6527 ~16 km · #24616 ~10 km · #15419 ~20 km.</p>
{parking_routes("Cascade d'Ars", ("#6527", (1.10, 42.84)), (1.31, 42.76), [("#24616", (1.3008, 42.7876)), ("#15419", (1.206, 42.8758))], "driving", "driving")}
{links([
 ("Wikiloc Cascada d'Ars (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-dars-3147596","wiki"),
 ("Visorando Cascada d'Ars (Moyenne)","https://www.visorando.com/randonnee-la-cascade-d-ars-2/","w"),
])}
</div>
<div class="trail">
<h4>Plan C · Biros / Bethmale (Moyenne / Wikiloc Fácil)</h4>
{wikiloc_box([("Lac de Bethmale (Fácil)","https://es.wikiloc.com/rutas-senderismo/lac-de-bethmale-et-etang-dayes-couserans-20519944")])}
<p>Valle y bosque con perras: Étang de Bethmale o Chapelle de l'Isard.</p>
</div>
{poi_extra("Couserans / Aulus", [
  "<strong>Circo glaciar:</strong> Cirque de Cagateille (imprescindible).",
  "<strong>Cascada:</strong> Cascade d'Ars (una de las grandes del Ariège).",
  "<strong>Lago:</strong> Lac de Bethmale (baño posible con prudencia).",
  "<strong>Pueblo termal:</strong> Aulus-les-Bains (fuente y paseo).",
], [
 ("Google Cirque de Cagateille","https://www.google.com/maps/search/?api=1&query=Cirque+de+Cagateille","g"),
 ("Google Cascade d'Ars","https://www.google.com/maps/search/?api=1&query=Cascade+d%27Ars+Aulus","g"),
 ("Google Aulus-les-Bains","https://www.google.com/maps/search/?api=1&query=Aulus-les-Bains","g"),
])}
{img('aulus','Aulus-les-Bains')}
"""))

    parts.append(day_shell("d5", "Día 5 · Lunes 10 — Traslado hacia el Macizo Central",
        ["~220–260 km", "P4N #5896", "P4N #8417", "P4N #208568"],
        f"""
{img('entraygues','Entraygues-sur-Truyère')}
<p>Día de carretera. No lo convirtáis en checklist del Lot. Objetivo: ganar latitud hacia el Cantal sin llegar reventados. Paradas cada ~1h30 por las perras.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#5896 Rue de la Grave</strong> (Entraygues) — parking tranquilo detrás del château. Si está lleno, alternativas (todas &gt;2 estrellas):</p>
<ul>
  <li><strong>#8417 Camping municipal Val de Saures***</strong> (4.36/5) — camping con acceso a río (perros ok en las reseñas) · al centro Entraygues: ~1,8 km.</li>
  <li><strong>#208568 40 Rue du Faubourg de Truyère</strong> (4.5/5) — parking con sombra y mesas de picnic · al centro Entraygues: ~0,7 km.</li>
</ul>
{quote('fronvald','17/06/2026','Muy tranquilo. Solo hay un área de picnic… el parking está vacío, es gratis y cerca del pueblo.','P4N #5896')}

<div class="trail">
<h4>Paseo corto al llegar (3–5 km)</h4>
<p><strong>Distancia parking → centro Entraygues:</strong> #5896 ~0,7 km · #8417 ~1,8 km · #208568 ~0,7 km.</p>
{parking_routes("centro Entraygues", ("#5896", (2.5628, 44.6439)), (2.5675, 44.6472), [("#8417", (2.5639, 44.6421)), ("#208568", (2.5667, 44.6488))], "walking", "walking")}
{links([
 ("P4N #5896","https://park4night.com/es/place/5896","o"),
 ("P4N #8417","https://park4night.com/es/place/8417","o"),
 ("P4N #208568","https://park4night.com/en/place/208568","o"),
 ("Wikipedia Entraygues", WIKI['entraygues']['wiki'], "p"),
])}
</div>
{poi_extra("Entraygues", [
  "<strong>Baño vigilado:</strong> Piscine d'Entraygues.",
  "<strong>Baño natural:</strong> Lot (zona Val de Saures / playa natural).",
  "<strong>Paisaje/monumento:</strong> Confluence Lot–Truyère (aire picnic).",
  "<strong>Quesería:</strong> Fromagerie Jean Mathieu (La Borie de Banroques).",
], [
 ("Google Piscine d'Entraygues","https://www.google.com/maps/search/?api=1&query=Piscine+d%27Entraygues+Entraygues-sur-Truy%C3%A8re","g"),
 ("Google Val de Saures (playa Lot)","https://www.google.com/maps/search/?api=1&query=Camping+Val+de+Saures+Entraygues+plage","g"),
 ("Google Confluence Lot–Truyère","https://www.google.com/maps/search/?api=1&query=Confluence+Lot+Truy%C3%A8re+aire+de+pique-nique+Entraygues","g"),
 ("Google Fromagerie Jean Mathieu","https://www.google.com/maps/search/?api=1&query=Fromagerie+Jean+Mathieu+Nadine+Boulant+La+Borie+de+Banroques","g"),
])}
<p>Cena temprana.</p>
"""))

    parts.append(day_shell("d6", "Día 6 · Martes 11 — Llegada a Le Lioran",
        ["~120–150 km", "P4N #13709", "P4N #6003", "P4N #27677"],
        f"""
{img('lioran','Le Lioran')}
<h4>Dónde dormir (Park4Night)</h4>
<p>Entráis en el parque de los Volcanes. El aire cambia: más seco, más alto, olor a pasto. Instalaos en <strong>Combe Nègre (#13709)</strong>, lado con árboles (haya/abeto). Llegad ≥18:30 para elegir plaza.</p>
{quote('SoSoPhil','24/06/2026','Bonito sitio… pasamos 2 noches en calma… hay punto de agua frente al restaurante.')}
{quote('SLMFC','16/07/2026','Noche del 15 al 16 de julio: rincón agradable y tranquilo entre los abetos.')}
<p><strong>Si está lleno</strong> (perros y &gt;2 estrellas):</p>
<ul>
  <li><strong>#6003 Camping des Blats</strong> (4.2/5) — camping con sombra · al inicio Bec: ~6,4 km.</li>
  <li><strong>#27677 Lavigerie - D62</strong> (4.0/5) — parking con vistas · al inicio Bec: ~29,7 km.</li>
</ul>

<div class="trail">
<h4>Aclimatación (hoy) · 5–8 km suaves</h4>
<p>5–8 km por pistas alrededor de Font de Cère / estación. Identificad el inicio del <strong>Bec de l'Aigle</strong> para mañana. Noche fresca: manta lista.</p>
<p><strong>Distancia parking → inicio Bec (referencia):</strong> #13709 ~2,8 km coche · #6003 ~6,4 km · #27677 ~29,7 km.</p>
{parking_routes("inicio Bec", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#6003", (2.7137, 45.0522)), ("#27677", (2.7026, 45.1301))], "driving", "driving")}
{links([
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
 ("P4N #6003","https://park4night.com/es/place/6003","o"),
 ("P4N #27677","https://park4night.com/es/place/27677","o"),
 ("Wikipedia Lioran", WIKI['lioran']['wiki'], "p"),
 ("OT Lioran","https://www.lelioran.com/","w"),
])}

<div class="wikiloc-box">
<strong>Si os apetece estirar (Wikiloc · útil mañana)</strong>
<div class="btns">
<a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058" target="_blank" rel="noopener">Wikiloc · Bec + Téton (Moderado · ~8 km)</a>
<a class="btn btn-wiki" href="https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228" target="_blank" rel="noopener">Wikiloc · Bec corto (Fácil · ~5,6 km)</a>
</div>
</div>
</div>
{poi_extra("Le Lioran / Volcanes", [
  "<strong>Punto de salida escénico:</strong> Font d'Alagnon.",
  "<strong>Mirador:</strong> Rocher du Bec de l'Aigle (belvédère).",
  "<strong>Quesería local:</strong> Fromagerie du Cantal / Le Lioran (Res. des Sagnes).",
  "<strong>Clásico del Cantal:</strong> Puy Mary (zona belvederes).",
], [
 ("Google Font d'Alagnon (Le Lioran)","https://www.google.com/maps/search/?api=1&query=Font+d%27Alagnon+Le+Lioran","g"),
 ("Google Rocher du Bec de l'Aigle","https://www.google.com/maps/search/?api=1&query=Rocher+du+Bec+de+l%27Aigle","g"),
 ("Google Fromagerie du Cantal (Le Lioran)","https://www.google.com/maps/search/?api=1&query=Fromagerie+du+Cantal+Le+Lioran+Residence+des+Sagnes","g"),
 ("Google Puy Mary (belvédères)","https://www.google.com/maps/search/?api=1&query=Puy+Mary+belvedere","g"),
])}
"""))

    parts.append(day_shell("d7", "Día 7 · Miércoles 12 — Bec de l'Aigle (moderada Visorando)",
        ["0 km coche", "P4N #13709", "P4N #6003", "P4N #27677", "Meteo 7:00"],
        f"""
{img('puy_mary','Macizo del Cantal / Puy Mary')}
<p>Jornada de crestas volcánicas con fichas <strong>Moyenne</strong> (no Difficile). Decisión a las <strong>7:00</strong> según cielo y viento.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p>Misma base: <strong>#13709 Combe Nègre</strong>. Alternativas si lleno: <strong>#6003</strong> · <strong>#27677</strong>.</p>

<div class="trail">
<h4>Plan A · Font d'Alagnon → Bec de l'Aigle → Téton (Moyenne)</h4>
{wikiloc_box([
 ("Bec + Téton (Moderado · ~8 km)","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058"),
 ("Bec corto (Fácil · ~5,6 km)","https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228"),
])}
<p><strong>Datos Visorando:</strong> ~8 km · +550–670 m · Moyenne. Patous posibles en pastos.</p>
<p><strong>Distancia parking → Font d'Alagnon (inicio):</strong> #13709 ~2,8 km coche · #6003 ~6,4 km · #27677 ~29,7 km.</p>
{parking_routes("Font d'Alagnon (inicio Bec)", ("#13709", (2.7330, 45.0849)), (2.74315, 45.088234), [("#6003", (2.7137, 45.0522)), ("#27677", (2.7026, 45.1301))], "driving", "driving")}
{links([
 ("Wikiloc Bec + Téton (Moderado · ~8 km)","https://es.wikiloc.com/rutas-senderismo/bec-de-laigle-et-teton-de-venus-depuis-le-lioran-225701058","wiki"),
 ("Wikiloc Bec corto (Fácil · ~5,6 km)","https://es.wikiloc.com/rutas-senderismo/le-bec-de-laigle-le-teton-de-venus-le-bataillouze-26865228","wiki"),
 ("Visorando Téton + Bec (Moyenne · ~8 km)","https://www.visorando.com/randonnee-le-teton-de-venus-au-dessus-du-lioran/","w"),
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
])}
</div>
<div class="trail">
<h4>Plan B · meteo / cansancio</h4>
<p>Téléphérique + paseo corto en alto, <strong>o</strong> solo bosque 6–8 km alrededor de la estación. Bajad antes de las tormentas de tarde.</p>
</div>
{poi_extra("Cantal / Bec", [
  "<strong>Mirador:</strong> Rocher du Bec de l'Aigle (~1.700 m).",
  "<strong>Belvedere famoso:</strong> Puy Mary (opcional, solo si no hay masificación).",
  "<strong>Quesería:</strong> Fromagerie du Cantal en Le Lioran.",
  "<strong>Pastos:</strong> vigilar patous (correa antes del rebaño).",
], [
 ("Google Rocher Bec de l'Aigle","https://www.google.com/maps/search/?api=1&query=Bec+de+l%27Aigle+Le+Lioran","g"),
 ("Google Puy Mary","https://www.google.com/maps/search/?api=1&query=Puy+Mary","g"),
 ("Google Fromagerie Le Lioran","https://www.google.com/maps/search/?api=1&query=Fromagerie+du+Cantal+Le+Lioran","g"),
 ("Wikipedia Puy Mary", WIKI['puy_mary']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d8", "Día 8 · Jueves 13 — Piste Verte → zona Salers",
        ["~70–90 km", "P4N #271257", "P4N #144306", "P4N #855"],
        f"""
{img('salers','Hacia Salers')}
<p>Día de recuperación activa: la <strong>Piste Verte Sumène-Artense</strong> (antigua vía férrea) ofrece viaductos, túnel ~600 m y sombra. Ideal perras (llano). Túnel: correa corta + linterna.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#271257 Ferme Fouey</strong> (hierba, granja, queso Cantal — comprad). Evitar aire #855 como primera opción; como plan alternativo (si está lleno), mejor #144306 o #855.</p>
{quote('jeremw','01/06/2026','Pasamos una noche en la granja. Acogida muy cálida… y buen queso de granja.','P4N #271257')}
{quote('cindy.frt','16/05/2026','Pasamos una noche en la granja: ¡fue genial!','P4N #271257')}
<p>Alternativas (2 extras) por si está lleno:</p>
<ul>
  <li><strong>#144306 Saint-Bonnet</strong> (hierba, ~4 plazas) · a Salers: ~4,9 km.</li>
  <li><strong>#855 Salers - D680</strong> (aire) · a Salers: ~1,3 km.</li>
</ul>

<div class="trail">
<h4>Zona Salers = vuestro punto de referencia</h4>
<p><strong>Distancia parking → Salers:</strong> #271257 ~3,4 km a pie · #144306 ~4,9 km · #855 ~1,3 km.</p>
{parking_routes("Salers", ("#271257", (2.4912, 45.1528)), (2.495, 45.1389), [("#144306", (2.4521, 45.1600)), ("#855", (2.4983, 45.1484))], "walking", "walking")}
{links([
 ("P4N #271257","https://park4night.com/es/place/271257","o"),
 ("P4N #144306","https://park4night.com/es/place/144306","o"),
 ("P4N #855","https://park4night.com/fr/place/855","o"),
])}

<h4 style="margin-top:.85rem">Piste Verte 8–12 km</h4>
{links([
 ("OT Sumène Artense · Piste Verte","https://tourisme-sumene-artense.com/activites/velo/la-piste-verte/","w"),
 ("Google Piste Verte","https://www.google.com/maps/search/?api=1&query=Piste+Verte+Sum%C3%A8ne+Artense","g"),
 ("P4N Fouey","https://park4night.com/es/place/271257","o"),
])}
<p>Túnel ~600 m: llevad linterna para el tramo oscuro y correa corta para el paso.</p>
</div>
<div class="trail">
<h4>Puntos de interés extra (Salers)</h4>
<ul>
  <li><strong>Monumento / pueblo:</strong> Salers (casco histórico de basalto).</li>
  <li><strong>Quesería/visita:</strong> Maison de la Salers (museo + degustación/boutique).</li>
  <li><strong>Compra de queso:</strong> Fromagerie (zona Saint-Bonnet-de-Salers / alrededores).</li>
  <li><strong>Paseo corto bonito:</strong> viaductos + tramos con sombra de la Piste Verte.</li>
</ul>
{links([
 ("Google Salers (pueblo)","https://www.google.com/maps/search/?api=1&query=Salers+Cantal","g"),
 ("Google Maison de la Salers (Le Fau)","https://www.google.com/maps/search/?api=1&query=Maison+de+la+Salers+Le+Fau+Saint-Bonnet-de-Salers","g"),
 ("Google Fromagerie Saint-Bonnet-de-Salers","https://www.google.com/maps/search/?api=1&query=fromagerie+Saint-Bonnet-de-Salers+coop%C3%A9rative","g"),
 ("Google Piste Verte viaductos","https://www.google.com/maps/search/?api=1&query=Piste+Verte+Sum%C3%A8ne+Artense+viaduc","g"),
])}
</div>
"""))

    parts.append(day_shell("d9", "Día 9 · Viernes 14 — Bocage de Salers",
        ["Local", "P4N #271257", "P4N #144306", "P4N #855"],
        f"""
{img('salers','Salers')}
<p>Salers de basalto y torres: visitad <strong>temprano</strong>. El bocage (setos, prados, caminos rurales) es el plan del día.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#271257 Ferme Fouey</strong> (hierba, granja, queso Cantal). Si está lleno:</p>
<ul>
  <li><strong>#144306 Saint-Bonnet</strong> (hierba, ~4 plazas) · a Salers: ~4,9 km.</li>
  <li><strong>#855 Salers - D680</strong> (aire) · a Salers: ~1,3 km.</li>
</ul>

<div class="trail">
<h4>Boucle La Montagnoune (~4 km, fácil) + paseo por el pueblo</h4>
{wikiloc_box([("Rutas fáciles cerca de Salers","https://es.wikiloc.com/rutas/senderismo/francia/auvergne-rhone-alpes/salers")])}
<p>Vistas al valle de la Maronne y al pueblo. Opcional: Pas de Peyrol solo para belvedere corto.</p>
<p><strong>Distancia parking → Salers (pueblo):</strong> #271257 ~3,4 km · #144306 ~4,9 km · #855 ~1,3 km.</p>
{parking_routes("Salers (pueblo)", ("#271257", (2.4912, 45.1528)), (2.495, 45.1389), [("#144306", (2.4521, 45.1600)), ("#855", (2.4983, 45.1484))], "walking", "walking")}
{links([
 ("Wikiloc La Montagnoune / Salers","https://es.wikiloc.com/rutas/senderismo/francia/auvergne-rhone-alpes/salers","wiki"),
 ("Visorando La Montagnoune (desde Salers)","https://www.visorando.com/randonnee-la-montagnoune-depuis-salers/","w"),
 ("OT Salers","https://www.salers-tourisme.fr/","w"),
 ("P4N #271257","https://park4night.com/es/place/271257","o"),
 ("P4N #144306","https://park4night.com/es/place/144306","o"),
])}
</div>
<div class="callout">Mediodía en Salers = masificación. Evitadlo.</div>
{poi_extra("Salers / bocage", [
  "<strong>Pueblo monumento:</strong> Salers (basalto, torres medievales).",
  "<strong>Quesería/visita:</strong> Maison de la Salers (degustación).",
  "<strong>Compra:</strong> queso Cantal en Ferme Fouey (en el parking).",
  "<strong>Paseo:</strong> bocage (setos, prados, caminos rurales).",
], [
 ("Google Salers","https://www.google.com/maps/search/?api=1&query=Salers+Cantal","g"),
 ("Google Maison de la Salers","https://www.google.com/maps/search/?api=1&query=Maison+de+la+Salers","g"),
 ("Google Pas de Peyrol","https://www.google.com/maps/search/?api=1&query=Pas+de+Peyrol","g"),
 ("Wikipedia Salers", WIKI['salers']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d10", "Día 10 · Sábado 15 — Hacia el Aubrac",
        ["~100–130 km", "P4N #5073", "P4N #35527", "P4N #701477", "#98143 CANCELADO"],
        f"""
{img('aubrac','Meseta del Aubrac')}
<p>Dejáis volcanes por la meseta. El paisaje se abre: menos árboles, más viento, más silencio.</p>
<div class="warn"><strong>#98143 cancelado:</strong> propiedad privada / perros prohibidos. No ir.</div>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#5073 Cascada del Déroc</strong> (parking hierba, vistas). Llegad tarde. Si está lleno:</p>
<ul>
  <li><strong>#35527 Camping municipal Nasbinals</strong> (pago, 4.0+/5) — perros OK · a Déroc: ~4 km.</li>
  <li><strong>#701477 Nasbinals D987</strong> (nature, 2026) — calma junto GR65 · a Déroc: ~3 km.</li>
</ul>
{quote('AlbericBoissier','16/07/2025','Sitio ideal, bonitas vistas, parking de hierba… El paseo corto hasta el pie de la cascada merece la pena.')}
{quote('Ars','15/04/2025','Ideal si vais con compañero de cuatro patas.')}

<div class="trail">
<h4>Paseo corto al llegar · Cascada del Déroc</h4>
<p><strong>Distancia parking → cascada (pie):</strong> #5073 ~0,3 km · #35527 ~4 km · #701477 ~3 km.</p>
{parking_routes("Cascada del Déroc", ("#5073", (3.02, 44.63)), (3.02, 44.63), [("#35527", (3.0402, 44.6703)), ("#701477", (3.0261, 44.6511))], "walking", "driving")}
{links([
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
 ("P4N #35527 Nasbinals","https://park4night.com/es/place/35527","o"),
 ("P4N #701477","https://park4night.com/en/place/701477","o"),
 ("Wikipedia Déroc", WIKI['deroc']['wiki'], "p"),
])}
</div>
{poi_extra("Aubrac", [
  "<strong>Cascada:</strong> Cascade du Déroc (órganos basálticos, cueva detrás).",
  "<strong>Pueblo:</strong> Nasbinals (GR65, panadería, épicerie).",
  "<strong>Lago:</strong> Lac des Salhiens (variante corta mañana).",
  "<strong>Queso local:</strong> aligot y tome en restaurantes del pueblo.",
], [
 ("Google Cascade du Déroc","https://www.google.com/maps/search/?api=1&query=Cascade+du+Deroc","g"),
 ("Google Nasbinals","https://www.google.com/maps/search/?api=1&query=Nasbinals","g"),
 ("Google Lac des Salhiens","https://www.google.com/maps/search/?api=1&query=Lac+des+Salhiens+Aubrac","g"),
 ("Turismo Lozère Déroc","https://www.lozere-tourisme.com/patrimoine-naturel/la-cascade-du-deroc/","w"),
])}
"""))

    parts.append(day_shell("d11", "Día 11 · Domingo 16 — Aubrac a fondo",
        ["Local", "P4N #5073", "P4N #35527", "P4N #701477"],
        f"""
<div class="photo-grid">{img('deroc','Cascada del Déroc')}{img('nasbinals','Nasbinals')}</div>
<p>Día de meseta. La cascada del Déroc merece la pena cuando la luz es buena. El GR65 pasa cerca de Nasbinals.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p>Misma base que ayer: <strong>#5073</strong> · alternativas <strong>#35527</strong> · <strong>#701477</strong>.</p>

<div class="trail">
<h4>Plan A · Bucle Déroc (moderado, perros OK con correa)</h4>
{wikiloc_box([("Cascada del Déroc (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479")])}
<p>PR Visorando «Nasbinals – Cascade du Déroc» <strong>Facile</strong> (~13 km · +205 m). Variante corta: cascada + lac Salhiens 6–8 km.</p>
<p><strong>Distancia parking → inicio Nasbinals (GR65):</strong> #5073 ~3 km a pie · #35527 ~0,5 km · #701477 ~1 km.</p>
{parking_routes("Nasbinals (inicio ruta)", ("#5073", (3.02, 44.63)), (3.0, 44.665), [("#35527", (3.0402, 44.6703)), ("#701477", (3.0261, 44.6511))], "walking", "walking")}
{links([
 ("Wikiloc Cascada del Déroc (Fácil)","https://es.wikiloc.com/rutas-senderismo/cascade-du-deroc-depuis-nasbinals-224224479","wiki"),
 ("Visorando Cascada del Déroc (Facile)","https://www.visorando.com/randonnee-nasbinals-cascade-du-deroc/","w"),
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
])}
</div>
<div class="trail">
<h4>Plan B · viento / patous densos</h4>
<p>Pueblo Nasbinals + descanso. Abortar si tormenta eléctrica (no hay abrigo en la meseta).</p>
</div>
{poi_extra("Aubrac / Nasbinals", [
  "<strong>Cascada:</strong> Déroc (icono de la meseta).",
  "<strong>Lago:</strong> Lac des Salhiens (variante corta).",
  "<strong>Pueblo:</strong> Nasbinals (comercios, GR65).",
  "<strong>Gastronomía:</strong> aligot (plato típico con tome).",
], [
 ("Google Nasbinals","https://www.google.com/maps/search/?api=1&query=Nasbinals","g"),
 ("Google Lac des Salhiens","https://www.google.com/maps/search/?api=1&query=Lac+des+Salhiens","g"),
 ("Turismo Lozère","https://www.lozere-tourisme.com/patrimoine-naturel/la-cascade-du-deroc/","w"),
])}
"""))

    parts.append(day_shell("d12", "Día 12 · Lunes 17 — Aubrac → Capcir",
        ["~280–320 km", "salir <9:00", "P4N #2547", "P4N #294842", "P4N #14142"],
        f"""
{img('formigueres','Formiguères')}
<p>El traslado más largo. Partid temprano, parad cada 1h30. El premio es volver a dormir alto y fresco en Formiguères.</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#2547 Calmazeille</strong>: elegid parking de tierra / inferior junto lago, no la fila de AC del asfalto.</p>
<p>Plan B: <strong>Matemale (#294842)</strong> — ojo barrera de altura ~2,0–2,2 m en temporada.</p>
<p>Plan C: <strong>#14142 Camping de La Devèze***</strong> — en bosque, buenas sensaciones con perros.</p>
{quote('RouilleP','28/02/2025','Pernocta posible… Gracias al ayuntamiento.')}

{links([
 ("P4N #2547","https://park4night.com/es/place/2547","o"),
 ("P4N #294842 Matemale","https://park4night.com/es/place/294842","o"),
 ("P4N #14142 La Devèze","https://park4night.com/es/place/14142","o"),
])}

<div class="trail">
<h4>Excursión suave al llegar (sin GPX)</h4>
<p><strong>Opción A (según guía):</strong> paseo de <strong>4–6 km</strong> de bosque saliendo a pie desde el propio parking.</p>
<p><strong>Distancia coche → interés:</strong> 0 km (salida directa). <strong>A pie:</strong> 4–6 km (1h15–2h, ritmo tranquilo).</p>
{links([
 ("Google paseo desde Calmazeille","https://www.google.com/maps/dir/?api=1&origin=42.6241,2.0711&destination=42.6241,2.0711&travelmode=walking","g"),
])}

<p style="margin-top:.7rem"><strong>Opción B (si os quedan piernas):</strong> ir al <strong>lago Matemale</strong> para un paseo/fotos.</p>
<p><strong>Distancia parking #2547 → Matemale #294842:</strong> ~11,6 km en coche (~15–25 min).</p>
<p><strong>Distancias al lago Matemale (#294842):</strong> #2547 ~11,6 km · #14142 ~8,3 km · #294842 = 0 km.</p>
{links([
 ("Google (coche) Calmazeille → Matemale","https://www.google.com/maps/dir/?api=1&origin=42.6241,2.0711&destination=42.5655,2.1044&travelmode=driving","g"),
 ("Google Matemale (search)","https://www.google.com/maps/search/?api=1&query=Lac+de+Matemale","g"),
])}

{links([
 ("Google coche #14142 → Matemale","https://www.google.com/maps/dir/?api=1&origin=42.6096,2.0914&destination=42.5655,2.1044&travelmode=driving","g"),
 ("Google A→B → Matemale","https://www.google.com/maps/dir/?api=1&origin=42.6241,2.0711&destination=42.5655,2.1044&waypoints=42.6096,2.0914&travelmode=driving","g"),
])}

{wikiloc_box([("Formiguères · Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412")])}
</div>

<div class="trail">
<h4>Puntos de interés extra (Lac de Matemale & quesos)</h4>
<ul>
  <li><strong>Baño supervisado:</strong> zona Ourson (cerca de la base náutica) en temporada.</li>
  <li><strong>Lugar de ocio:</strong> Espace loisirs du Lac de Matemale.</li>
  <li><strong>Quesos de compra:</strong> Le Calmadou (fromagerie / crèmerie de brebis en Formiguères).</li>
  <li><strong>Bonus:</strong> Ferme Pérarnaud (tienda de granja).</li>
</ul>
{links([
 ("Google Ourson / base nautique Matemale","https://www.google.com/maps/search/?api=1&query=Base+nautique+Ourson+Lac+de+Matemale","g"),
 ("Google Espace loisirs Lac de Matemale","https://www.google.com/maps/search/?api=1&query=Espace+loisirs+Lac+de+Matemale","g"),
 ("Google Le Calmadou (Formiguères)","https://www.google.com/maps/search/?api=1&query=Le+Calmadou+Formigu%C3%A8res+fromagerie","g"),
 ("Google Ferme Pérarnaud (Formiguères)","https://www.google.com/maps/search/?api=1&query=Ferme+P%C3%A9rarnault+Formigu%C3%A8res","g"),
])}
</div>

{links([
 ("Google Formiguères","https://www.google.com/maps/dir/?api=1&destination=42.6241,2.0711&travelmode=driving","g"),
])}
"""))

    parts.append(day_shell("d13", "Día 13 · Martes 18 — Capcir / Matemale (moderado)",
        ["Local", "P4N #2547", "P4N #294842", "P4N #14142", "día colchón"],
        f"""
{img('matemale','Lago de Matemale')}
<p>Último día pleno con perras. <strong>Camporells cancelado</strong> (Difficile). Prioridad: <strong>lago de Matemale / Forêt de la Matte</strong> (fácil, perros OK).</p>
<h4>Dónde dormir (Park4Night)</h4>
<p><strong>#2547 Calmazeille</strong> (tierra junto lago). Alternativas: <strong>#294842 Matemale</strong> · <strong>#14142 La Devèze</strong>.</p>

<div class="trail">
<h4>Plan A · Lac de Matemale + Forêt de la Matte (Facile · ~9,7 km · +130 m)</h4>
{wikiloc_box([("Formiguères · Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412")])}
<p>Bucle por el lago, Tour de Creu y pinares. Ideal con perras, casi llano, sombra.</p>
<p><strong>Distancia parking → Matemale (lago):</strong> #2547 ~11,6 km · #14142 ~8,3 km · #294842 = 0 km.</p>
{parking_routes("Lac de Matemale", ("#2547", (2.0711, 42.6241)), (2.1044, 42.5655), [("#14142", (2.0914, 42.6096)), ("#294842", (2.1044, 42.5655))], "driving", "driving")}
{links([
 ("Wikiloc Lac de l'Olive (Fácil)","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412","wiki"),
 ("Visorando bucle Matemale (Facile)","https://www.visorando.com/randonnee-boucle-depuis-le-lac-de-matemale/","w"),
 ("P4N #2547","https://park4night.com/es/place/2547","o"),
 ("P4N #294842","https://park4night.com/es/place/294842","o"),
 ("Wikipedia Matemale", WIKI['matemale']['wiki'], "p"),
])}
</div>
<div class="trail">
<h4>Plan B · bosques Formiguères / orillas del lago</h4>
<p>4–8 km suaves alrededor de Calmazeille. Verificar altura de barrera antes de entrar con la Sunlight en Matemale.</p>
</div>
{poi_extra("Capcir / Matemale", [
  "<strong>Baño supervisado:</strong> zona Ourson (base náutica) en temporada.",
  "<strong>Lago:</strong> Lac de Matemale (paseo, paddle, fotos).",
  "<strong>Quesería:</strong> Le Calmadou (brebis, Formiguères).",
  "<strong>Granja:</strong> Ferme Pérarnaud (tomme des Pyrénées).",
], [
 ("Google Ourson Matemale","https://www.google.com/maps/search/?api=1&query=Base+nautique+Ourson+Matemale","g"),
 ("Google Lac de Matemale","https://www.google.com/maps/search/?api=1&query=Lac+de+Matemale","g"),
 ("Google Le Calmadou","https://www.google.com/maps/search/?api=1&query=Le+Calmadou+Formigu%C3%A8res","g"),
 ("Google Ferme Pérarnaud","https://www.google.com/maps/search/?api=1&query=Ferme+P%C3%A9rarnaud+Formigu%C3%A8res","g"),
])}
"""))

    parts.append(day_shell("d14", "Día 14 · Miércoles 19 — Capcir → Teià",
        ["~180–200 km / 2h30–3h", "Regreso"],
        f"""
<p>Regreso por Cerdanya / Puigcerdà. Alternativa si hay retenciones. Parada café y paseo corto si hace falta.</p>
<div class="trail">
<h4>Ruta de regreso</h4>
<p>Salid temprano desde Formiguères. Parada recomendada en <strong>Puigcerdà</strong> (café + paseo 20 min).</p>
{links([
 ("Google Formiguères → Teià","https://www.google.com/maps/dir/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain","g"),
 ("Google parada Puigcerdà","https://www.google.com/maps/search/?api=1&query=Puigcerd%C3%A0+centro","g"),
])}
</div>
{poi_extra("Regreso Cerdanya", [
  "<strong>Pueblo:</strong> Puigcerdà (plaza y lago de la Seu).",
  "<strong>Compra:</strong> quesos y embutidos de la Cerdanya.",
  "<strong>Baño/picnic:</strong> ríos del valle de la Cerdanya (paradas en ruta).",
  "<strong>Monumento:</strong> bellver de Cerdanya (opcional, desvío corto).",
], [
 ("Google Puigcerdà","https://www.google.com/maps/search/?api=1&query=Puigcerd%C3%A0","g"),
 ("Google fromagerie Cerdanya","https://www.google.com/maps/search/?api=1&query=fromagerie+Cerdanya+Puigcerda","g"),
 ("Google Bellver de Cerdanya","https://www.google.com/maps/search/?api=1&query=Bellver+de+Cerdanya","g"),
])}
<p>Fin de ruta: misma casa, otras piernas.</p>
"""))

    parts.append("</section>")

    # P4N section
    parts.append("""
<section class="section" id="p4n"><h2>Park4Night · FRANCIA AGOSTO 2026</h2>
<div class="card prose">
<div class="warn"><strong>Login:</strong> <a href="https://park4night.com/es" target="_blank" rel="noopener">park4night.com/es</a> → Mi cuenta → Conectarse. Cuando entre: estrella → carpeta <code>FRANCIA AGOSTO 2026</code>.</div>
<h4>Añadir (noche OK)</h4>
<ul>
<li><a href="https://park4night.com/es/place/22287" target="_blank" rel="noopener">#22287</a> Tournals</li>
<li><a href="https://park4night.com/es/place/152052" target="_blank" rel="noopener">#152052</a> Bonascre</li>
<li><a href="https://park4night.com/es/place/7266" target="_blank" rel="noopener">#7266</a> Aire Ax</li>
<li><a href="https://park4night.com/es/place/6527" target="_blank" rel="noopener">#6527</a> Col de la Core</li>
<li><a href="https://park4night.com/es/place/24616" target="_blank" rel="noopener">#24616</a> Guzet</li>
<li><a href="https://park4night.com/es/place/15419" target="_blank" rel="noopener">#15419</a> Haut Salat (Seix)</li>
<li><a href="https://park4night.com/es/place/5896" target="_blank" rel="noopener">#5896</a> Entraygues</li>
<li><a href="https://park4night.com/es/place/8417" target="_blank" rel="noopener">#8417</a> Val de Saures</li>
<li><a href="https://park4night.com/en/place/208568" target="_blank" rel="noopener">#208568</a> Entraygues Faubourg</li>
<li><a href="https://park4night.com/es/place/13709" target="_blank" rel="noopener">#13709</a> Combe Nègre</li>
<li><a href="https://park4night.com/es/place/6003" target="_blank" rel="noopener">#6003</a> Camping des Blats</li>
<li><a href="https://park4night.com/es/place/27677" target="_blank" rel="noopener">#27677</a> Lavigerie</li>
<li><a href="https://park4night.com/es/place/271257" target="_blank" rel="noopener">#271257</a> Ferme Fouey</li>
<li><a href="https://park4night.com/es/place/144306" target="_blank" rel="noopener">#144306</a> Saint-Bonnet</li>
<li><a href="https://park4night.com/fr/place/855" target="_blank" rel="noopener">#855</a> Salers D680</li>
<li><a href="https://park4night.com/es/place/5073" target="_blank" rel="noopener">#5073</a> Cascada del Déroc</li>
<li><a href="https://park4night.com/es/place/35527" target="_blank" rel="noopener">#35527</a> Camping Nasbinals</li>
<li><a href="https://park4night.com/en/place/701477" target="_blank" rel="noopener">#701477</a> Nasbinals D987</li>
<li><a href="https://park4night.com/es/place/2547" target="_blank" rel="noopener">#2547</a> Formiguères</li>
<li><a href="https://park4night.com/es/place/294842" target="_blank" rel="noopener">#294842</a> Matemale</li>
<li><a href="https://park4night.com/es/place/14142" target="_blank" rel="noopener">#14142</a> La Devèze</li>
</ul>
<p><strong>No añadir para noche:</strong> #51675, #98143, #17010, #3781.</p>
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
