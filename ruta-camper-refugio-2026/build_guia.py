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
    """items: (label, url, kind)"""
    btns = []
    for label, url, kind in items:
        cls = {"g": "btn btn-g", "o": "btn btn-o", "w": "btn btn-w", "p": "btn btn-p"}.get(kind, "btn")
        btns.append(f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>')
    return '<div class="btns">' + "".join(btns) + "</div>"


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
<div class="brand">Guía camper · Francia verde<small>6–19 agosto 2026 · Lonely Planet style</small></div>
<div class="btns">
<a class="btn btn-g" href="https://www.google.com/maps/dir/Tei%C3%A0,+Spain/Ax-les-Thermes,+France/Seix,+France/Entraygues-sur-Truy%C3%A8re,+France/Le+Lioran,+France/Salers,+France/Nasbinals,+France/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain" target="_blank" rel="noopener">Google Maps ruta</a>
<a class="btn btn-o" href="https://park4night.com/es" target="_blank" rel="noopener">Park4Night</a>
</div></div></header>
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Refugio climático</span><span class="chip">Sunlight 600 + 2 perras</span><span class="chip">P4N recondito</span><span class="chip">Solo rutas con perras</span></div>
<h1>Del Pirineo ariégeois al Capcir</h1>
<p class="lead">Guía de viaje completa: literatura de cada zona, fotos, opiniones reales de Park4Night, rutas Wikiloc/AllTrails/Visorando explicadas, lugares de interés y mapas Google.</p>
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
 ("Crear Google My Maps","https://www.google.com/maps/d/","g"),
 ("Descargar ruta.kml","ruta.kml","p"),
])}
<div class="callout"><strong>Google My Maps en 5 min:</strong> Crear mapa → nombre <em>FRANCIA AGOSTO 2026</em> → Importar <code>ruta.kml</code> → abrir en el móvil (Maps → Tus mapas) y descargar offline.</div>
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
 ("OT Ax", "https://www.valleesdaxtourisme.com/", "w"),
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
 ("Outdooractive Cagateille fácil", "https://www.outdooractive.com/es/route/ruta-de-senderismo/ariege/el-circo-de-cagateille/808515720/", "w"),
 ("AllTrails Cagateille", "https://www.alltrails.com/trail/france/ariege/cirque-de-cagateille", "w"),
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
 ("Topo Bec de l'Aigle", "https://cantalpassion.com/sports-et-loisirs/randonnees/les-randos-entre-vallees-et-sommets/633-haute-vallee-de-l-alagnon/5278-le-bec-de-l-aigle", "w"),
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
 ("Lozère Tourisme Déroc", "https://www.lozere-tourisme.com/patrimoine-naturel/cascade-du-deroc/", "w"),
 ("AllTrails bucle Déroc", "https://www.alltrails.com/trail/france/lozere/boucle-de-la-cascade-du-deroc", "w"),
 ("PNR Aubrac", "https://www.parc-naturel-aubrac.fr/", "w"),
])}
</div>

<div class="card prose"><h3>6. Capcir · Formiguères, Matemale, Camporells</h3>
<div class="photo-grid">{img('formigueres','Formiguères')}{img('matemale','Lac de Matemale')}</div>
<p>{esc(WIKI['formigueres']['extract'])}</p>
<p>{esc(WIKI['capcir']['extract'])} Los <strong>lagos de Camporells</strong> (espacio natural clasificado): perros <em>autorizados con correa</em>. Evitad entrar en reservas naturales catalanas vecinas (perros prohibidos). Versión suave: vuelta al lago de Matemale bajo pinares.</p>
{links([
 ("Wikipedia Formiguères", WIKI['formigueres']['wiki'], "p"),
 ("Visorando Camporells", "https://www.visorando.com/randonnee-boucle-des-camporells-par-la-vallee-de-l/", "w"),
 ("Wikiloc Formiguères lago Olive", "https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412", "w"),
 ("OT Capcir", "https://www.capcir-pyrenees.com/", "w"),
])}
</div>
</section>
""")

    # day nav
    parts.append('<nav class="day-nav">' + "".join(
        f'<a href="#d{i}">{i}<span>día</span></a>' for i in range(1, 15)
    ) + '</nav><section class="section" id="dias"><h2>Itinerario día a día</h2>')

    # DAYS
    parts.append(day_shell("d1", "Día 1 · Jueves 6 — Teià → Ax-les-Thermes",
        ["~180 km / 2h15", "P4N #22287 Tournals"],
        f"""
{img('ax','Llegada a Ax')}
<p>Salís de Teià sin prisa. El objetivo no es hacer kilómetros heroicos, sino llegar a la Haute Ariège con luz de tarde y cambiar de clima mental: de litoral a valle termal. La N-20 / túneles de Puymorens o la ruta por Andorra según tráfico; mirad el mapa antes de salir.</p>
<h4>Dónde dormir</h4>
<p><strong>#22287 Tournals</strong> (hacia Bonascre): acceso estrecho que filtra autocaravanas, sombra, mesas, a veces WC seco. Cerrar el cable/hilo al entrar y salir. Si hay vacas/valla → rincón tranquilo en Bonascre.</p>
{quote('DDlaPRALINE','06/06/2024','Hay un cartel que indica que el aparcamiento es para una sola noche.')}
{quote('jackhyde','26/06/2023','La zona está después de la barrera (el cable): recordad cerrarla al pasar.')}
<h4>Qué hacer al llegar</h4>
<ul>
<li>Paseo corto ribera del Ariège (3–5 km máximo).</li>
<li><strong>Bassin des Ladres:</strong> ritual termal; las perras se quedan fuera del vaso (paseo perimetral).</li>
<li>Pan, fruta, llenar agua. Evitar pernocta ilegal en orillas del pueblo.</li>
</ul>
{links([
 ("Google → Tournals","https://www.google.com/maps/dir/?api=1&destination=42.7056,1.8216&travelmode=driving","g"),
 ("Park4Night #22287","https://park4night.com/es/place/22287","o"),
 ("Bassin des Ladres","https://www.google.com/maps/search/?api=1&query=Bassin+des+Ladres+Ax-les-Thermes","g"),
 ("Wikipedia Ladres", WIKI['ladres']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d2", "Día 2 · Viernes 7 — Bosques Ax / Orgeix (apto con perras)",
        ["Local", "P4N #22287", "Orlu CANCELADO"],
        f"""
{img('ladres','Ax y alrededores')}
<p>Día de aclimatación <strong>100 % con perras</strong>. La reserva de Orlu queda fuera: <strong>perros prohibidos</strong>. Explorad bosques y pistas hacia <strong>Orgeix / Ascou / Tournals</strong>: sombra de haya, torrentes, poca gente comparado con Orlu.</p>
<div class="trail">
<h4>Sendero A · Vallée d'Orgeix / Lac d'Ayguelongue (recomendado)</h4>
<p>Valle lateral menos masificado. Aparcamiento al final de la pista forestal de Orgeix. Camino claro hacia el lago: prados, bosque, agua. Ideal 3–5 h ida y vuelta según ritmo. Confirmad en el track que <strong>no entra en la reserva Orlu</strong>.</p>
<p><strong>Datos orientativos:</strong> 10–14 km · D+ moderado · horario salida 7:30–8:00.</p>
{links([
 ("France-Randos Ayguelongue","http://www.france-randos.com/randonnee/orgeix/ariege-09/le-lac-dayguelongue","w"),
 ("Wikiloc · buscar Ayguelongue Orgeix","https://es.wikiloc.com/wikiloc/view.do?q=Ayguelongue+Orgeix","w"),
 ("AllTrails zona Orgeix","https://www.alltrails.com/explore?q=Orgeix%20Ari%C3%A8ge","w"),
 ("Google Orgeix","https://www.google.com/maps/search/?api=1&query=Orgeix+Ari%C3%A8ge","g"),
])}
</div>
<div class="trail">
<h4>Sendero B · Solo sombra (plan calor)</h4>
<p>6–8 km de pistas alrededor de Tournals / Bonascre. Siesta en camper 12–17 h. Segunda salida corta al atardecer.</p>
</div>
<div class="callout"><strong>Tip:</strong> bajad el GPX la noche anterior y leed comentarios recientes buscando la palabra <em>chien</em>.</div>
{links([
 ("P4N #22287","https://park4night.com/es/place/22287","o"),
 ("Google Tournals","https://www.google.com/maps/dir/?api=1&destination=42.7056,1.8216","g"),
])}
"""))

    parts.append(day_shell("d3", "Día 3 · Sábado 8 — Ax → Foix corta → Couserans",
        ["~120–140 km", "P4N #6527 o #24616", "#51675 NO noche"],
        f"""
<div class="photo-grid">{img('foix','Château de Foix')}{img('saint_lizier','Saint-Lizier')}</div>
<p>Dejáis Haute Ariège hacia el oeste. <strong>Foix</strong>: parada corta al castillo (foto/mirador), no os comáis la mañana en cola. Luego Saint-Girons / Saint-Lizier y subida a collados.</p>
<h4>Dónde dormir</h4>
<p>Prioridad <strong>#6527 Col de la Core</strong> (altitud, fresco, noche calma tras el bullicio diurno) o <strong>#24616 Guzet Prat-Mataou</strong> (vistas, parking alto). <strong>No #51675 de noche.</strong></p>
{quote('Leptitromain','25/07/2026','Pasamos una noche tranquila en este parking con vistas a las montañas y al pueblo de Aulus-les-Bains.','P4N #24616')}
{quote('nayati64','01/06/2025','Pasamos 3 noches tranquilas. El sitio está limpio: dejémoslo así.','P4N #6527')}
<div class="trail">
<h4>Atardecer en Col de la Core</h4>
<p>El collado (~1.395 m) es hub de GR y paseos cortos. No hace falta una cima: la luz sobre Bethmale y el Castillonnais basta. Si queréis una ruta larga al día siguiente, descargad track esta noche.</p>
{links([
 ("Wikiloc Col de la Core (ruta)","https://es.wikiloc.com/rutas-senderismo/col-de-la-core-7866059","w"),
 ("Wikiloc view id 7866059","https://es.wikiloc.com/wikiloc/view.do?id=7866059","w"),
 ("Google Col de la Core","https://www.google.com/maps/search/?api=1&query=Col+de+la+Core","g"),
 ("P4N #6527","https://park4night.com/es/place/6527","o"),
 ("P4N #24616 Guzet","https://park4night.com/es/place/24616","o"),
])}
</div>
{links([("Google → Guzet","https://www.google.com/maps/dir/?api=1&destination=42.7876,1.3008&travelmode=driving","g"),("Wikipedia Saint-Lizier",WIKI['saint_lizier']['wiki'],"p")])}
"""))

    parts.append(day_shell("d4", "Día 4 · Domingo 9 — Cagateille de día + Biros / Cascade d'Ars",
        ["Local", "Dormir Guzet/Core", "#51675 solo DÍA"],
        f"""
{img('cagateille','Cirque de Cagateille')}
<div class="warn"><strong>#51675 NO DORMIR.</strong> Comentario escalador1 27/07/2026: desde 26/7/2026, orden municipal, sin campers/autos de 20:00 a 6:00. Id de día y volved a Guzet/Core.</div>
<div class="trail">
<h4>Plan A · Cirque de Cagateille (fácil, familia, perras OK con correa)</h4>
<p>Desde el parking del circo: sendero marcado bajo bosque, arroyos, y el fondo del anfiteatro. <strong>~4,3 km A/R · 1h30 · D+ ~140 m</strong>. Pasarela al centro del circo. Es el “wow” del Couserans sin trampas técnicas.</p>
<p><strong>No prolonguéis</strong> a Hillette/Alet si no queréis pasos con cadenas y exposición (eso es otra categoría).</p>
{links([
 ("Outdooractive topo oficial fácil","https://www.outdooractive.com/es/route/ruta-de-senderismo/ariege/el-circo-de-cagateille/808515720/","w"),
 ("AllTrails Cirque de Cagateille","https://www.alltrails.com/trail/france/ariege/cirque-de-cagateille","w"),
 ("Visorando (versión lagos, dura)","https://www.visorando.com/en/walk-cirque-de-cagateille-etang-de-la-hilette/","w"),
 ("OT Couserans Cagateille","https://www.haut-couserans.com/randonnees/detail-de-la-randonnee-cirque-de-cagateille-1-fr-8.html","w"),
 ("Google parking Cagateille","https://www.google.com/maps/dir/?api=1&destination=42.7562,1.2876","g"),
 ("P4N #51675 (solo día)","https://park4night.com/es/place/51675","o"),
])}
</div>
<div class="trail">
<h4>Plan B · Cascade d'Ars desde Aulus (temprano)</h4>
<p>Una de las grandes cascadas del Ariège. Bosque, GR10, mucha gente a mediodía → <strong>salida 7:30</strong>. Variante corta ida-vuelta a la cascada, o bucle con el lago de Guzet (más largo).</p>
{links([
 ("Wikiloc Cascades d'Ars","https://es.wikiloc.com/rutas-senderismo/cascades-dars-56772088","w"),
 ("Wikiloc Aulus–Guzet–Ars","https://es.wikiloc.com/rutas-senderismo/aulus-les-bains-letang-de-guzet-cascade-dars-65871487","w"),
 ("Wikiloc view 56772088","https://es.wikiloc.com/wikiloc/view.do?id=56772088","w"),
 ("Google Cascade d'Ars","https://www.google.com/maps/search/?api=1&query=Cascade+d%27Ars+Aulus-les-Bains","g"),
])}
</div>
<div class="trail">
<h4>Plan C · Vallée de Biros (exploratorio)</h4>
<p>10–15 km por pistas/caminos, ruinas mineras, bosque. Vigilad socavones y ganado. Correa cerca de rebaños.</p>
{links([("Wikiloc Biros / Sentein","https://es.wikiloc.com/wikiloc/view.do?q=vall%C3%A9e+de+Biros+Sentein","w"),("Google Sentein","https://www.google.com/maps/search/?api=1&query=Sentein","g")])}
</div>
{img('aulus','Aulus-les-Bains')}
"""))

    parts.append(day_shell("d5", "Día 5 · Lunes 10 — Traslado hacia el Macizo Central",
        ["~220–260 km", "nature / #5896", "#3781 404"],
        f"""
{img('entraygues','Entraygues-sur-Truyère')}
<p>Día de carretera. No lo convirtáis en checklist del Lot. Objetivo: ganar latitud hacia el Cantal sin llegar reventados. Paradas cada ~1h30 por las perras.</p>
<h4>Dónde dormir</h4>
<p>Buscad <strong>nature</strong> en ruta con filtro P4N. Plan B: <strong>#5896 Rue de la Grave</strong> (Entraygues) — comentarios 2025–26 de noches tranquilas. Evitar aire masificada #415568 como plan A. El antiguo #3781 ya no existe.</p>
{quote('fronvald','17/06/2026','Muy tranquilo. Solo hay un área de picnic… el parking está vacío, es gratis y cerca del pueblo.','P4N #5896')}
<p>Al llegar: solo 3–5 km de paseo. Cena temprana.</p>
{links([
 ("Google Entraygues","https://www.google.com/maps/dir/?api=1&destination=44.6439,2.5628&travelmode=driving","g"),
 ("P4N #5896","https://park4night.com/es/place/5896","o"),
 ("Wikipedia Entraygues", WIKI['entraygues']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d6", "Día 6 · Martes 11 — Llegada a Le Lioran",
        ["~120–150 km", "P4N #13709 Combe Nègre"],
        f"""
{img('lioran','Le Lioran')}
<p>Entráis en el parque de los Volcanes. El aire cambia: más seco, más alto, olor a pasto. Instalaos en <strong>Combe Nègre (#13709)</strong>, lado con árboles (haya/abeto). Llegad ≥18:30 para elegir plaza.</p>
{quote('SoSoPhil','24/06/2026','Bonito sitio… pasamos 2 noches en calma… hay punto de agua frente al restaurante.')}
{quote('SLMFC','16/07/2026','Noche del 15 al 16 de julio: rincón agradable y tranquilo entre los abetos.')}
<h4>Aclimatación</h4>
<p>5–8 km por pistas alrededor de Font de Cère / estación. Identificad el inicio del Bec de l'Aigle para mañana. Noche fresca: manta lista.</p>
{links([
 ("Google Combe Nègre","https://www.google.com/maps/dir/?api=1&destination=45.0849,2.733&travelmode=driving","g"),
 ("P4N #13709","https://park4night.com/es/place/13709","o"),
 ("Wikipedia Lioran", WIKI['lioran']['wiki'], "p"),
 ("OT Lioran","https://www.lelioran.com/","w"),
])}
"""))

    parts.append(day_shell("d7", "Día 7 · Miércoles 12 — Bec de l'Aigle (jornada fuerte)",
        ["0 km coche", "P4N #13709", "Meteo 7:00"],
        f"""
{img('puy_mary','Macizo del Cantal / Puy Mary')}
<p>La jornada más exigente del viaje. Decisión a las <strong>7:00</strong> según cielo y viento. Si hay tormenta de tarde, acortad.</p>
<div class="trail">
<h4>Plan A · Font d'Alagnon → Bec de l'Aigle → (opcional) Téton de Vénus</h4>
<p>Salís de Font d'Alagnon (~1.190 m), detrás de los comercios, dirección Bec de l'Aigle. Subida constante: bosque → pastos → tramo rocoso corto (no ferrata) → rocher ~1.700 m con vistas a Peyre Arse / Seycheuse. Opcional continuar al Téton de Vénus y bajar por Combenègre.</p>
<p><strong>Datos:</strong> variantes 7,5–15 km · varias horas · D+ serio pero senda clara. Abortar con truenos o perras exhaustas. Patous posibles en pastos.</p>
{links([
 ("Topo detallado Cantal Passion","https://cantalpassion.com/sports-et-loisirs/randonnees/les-randos-entre-vallees-et-sommets/633-haute-vallee-de-l-alagnon/5278-le-bec-de-l-aigle","w"),
 ("VisuGPX boucle Bec–Peyre Arse","https://www.visugpx.com/1376487773","w"),
 ("Bergfex Lioran–Bec","https://www.bergfex.es/sommer/auvergne-rhone-alpes/touren/wanderung/3619535,plomb-du-cantal--super-lioran--bec-de-laigle--font-dalagnon/","w"),
 ("Wikiloc · Bec de l'Aigle Lioran","https://es.wikiloc.com/wikiloc/view.do?q=Bec+de+l%27Aigle+Lioran","w"),
 ("Google Font d'Alagnon","https://www.google.com/maps/search/?api=1&query=Font+d%27Alagnon+Le+Lioran","g"),
])}
</div>
<div class="trail">
<h4>Plan B · meteo / cansancio</h4>
<p>Téléphérique + paseo corto en alto y bajada temprana, <strong>o</strong> solo bosque 6–8 km alrededor de la estación. Bajad antes de las tormentas de tarde típicas del Macizo.</p>
</div>
{links([("P4N #13709","https://park4night.com/es/place/13709","o"),("Wikipedia Puy Mary",WIKI['puy_mary']['wiki'],"p")])}
"""))

    parts.append(day_shell("d8", "Día 8 · Jueves 13 — Piste Verte → zona Salers",
        ["~70–90 km", "P4N #271257 o #144306"],
        f"""
{img('salers','Hacia Salers')}
<p>Día de recuperación activa: la <strong>Piste Verte Sumène-Artense</strong> (antigua vía férrea) ofrece viaductos, túnel ~600 m y sombra. Ideal perras (llano). Túnel: correa corta + linterna.</p>
<h4>Dónde dormir</h4>
<p><strong>#271257 Ferme Fouey</strong> (hierba, granja, queso Cantal — comprad) o <strong>#144306</strong> estadio hierba (~4 plazas). Evitar aire #855.</p>
{quote('jeremw','01/06/2026','Pasamos una noche en la granja. Acogida muy cálida… y buen queso de granja.','P4N #271257')}
{quote('cindy.frt','16/05/2026','Pasamos una noche en la granja: ¡fue genial!','P4N #271257')}
<div class="trail">
<h4>Piste Verte 8–12 km</h4>
{links([
 ("Wikiloc Piste Verte Sumène Artense","https://es.wikiloc.com/wikiloc/view.do?q=Piste+Verte+Sum%C3%A8ne+Artense","w"),
 ("Google Piste Verte","https://www.google.com/maps/search/?api=1&query=Piste+Verte+Sum%C3%A8ne+Artense","g"),
 ("P4N Fouey","https://park4night.com/es/place/271257","o"),
 ("P4N #144306","https://park4night.com/es/place/144306","o"),
])}
</div>
"""))

    parts.append(day_shell("d9", "Día 9 · Viernes 14 — Bocage de Salers",
        ["Local", "P4N Fouey / #144306"],
        f"""
{img('salers','Salers')}
<p>Salers de basalto y torres: visitad <strong>temprano</strong>. El resto del día, el bocage (setos, prados, caminos rurales) es más fiel al espíritu del viaje que otra cima volcánica llena de coches.</p>
<div class="trail">
<h4>Boucle bocage 10–14 km</h4>
<p>Pueblos satélite, pistas agrícolas, queso. Opcional: subir en camper al Pas de Peyrol solo para belvedere corto si el parking no es un caos — no hace falta coronar el Puy Mary.</p>
{links([
 ("Wikiloc Salers boucle","https://es.wikiloc.com/wikiloc/view.do?q=Salers+boucle+randonn%C3%A9e","w"),
 ("AllTrails Salers","https://www.alltrails.com/explore?q=Salers%20Cantal","w"),
 ("OT Salers","https://www.salers-tourisme.fr/","w"),
 ("Google Salers","https://www.google.com/maps/search/?api=1&query=Salers+Cantal","g"),
 ("Wikipedia Salers", WIKI['salers']['wiki'], "p"),
])}
</div>
<div class="callout">Mediodía en Salers = masificación. Evitadlo.</div>
"""))

    parts.append(day_shell("d10", "Día 10 · Sábado 15 — Hacia el Aubrac",
        ["~100–130 km", "P4N #5073", "#98143 CANCELADO"],
        f"""
{img('aubrac','Meseta del Aubrac')}
<p>Dejáis volcanes por la meseta. El paisaje se abre: menos árboles, más viento, más silencio. Es el tramo más solitario del viaje — siempre con las perras.</p>
<div class="warn"><strong>#98143 cancelado:</strong> comentario 18/07/2026 — propiedad privada / prohibido acampar y furgonetas; además perros prohibidos. No ir.</div>
<h4>Dónde dormir</h4>
<p><strong>#5073 Cascada del Déroc</strong>. Llegad tarde (el parking se vacía cuando se van los visitantes de día). Apto con perros según reseñas.</p>
{quote('AlbericBoissier','16/07/2025','Sitio ideal, bonitas vistas, parking de hierba… El paseo corto hasta el pie de la cascada merece la pena.')}
{quote('Ars','15/04/2025','Ideal si vais con compañero de cuatro patas.')}
<p>Paseo corto a la cascada al llegar. Protocolo ganado/patous desde el minuto uno.</p>
{links([
 ("Google #5073","https://www.google.com/maps/dir/?api=1&destination=44.63,3.02&travelmode=driving","g"),
 ("P4N #5073","https://park4night.com/es/place/5073","o"),
 ("Wikipedia Déroc", WIKI['deroc']['wiki'], "p"),
])}
"""))

    parts.append(day_shell("d11", "Día 11 · Domingo 16 — Aubrac a fondo",
        ["Local", "P4N #5073"],
        f"""
<div class="photo-grid">{img('deroc','Cascada del Déroc')}{img('nasbinals','Nasbinals')}</div>
<p>Día de meseta. La cascada del Déroc merece la pena cuando la luz es buena: órganos basálticos, cueva detrás del agua, vistas al valle de la Gambaïse. El GR65 pasa cerca de Nasbinals.</p>
<div class="trail">
<h4>Plan A · Bucle Déroc (moderado, perros OK con correa)</h4>
<p>AllTrails y el PR «Del Déroc a la Peyrade» ofrecen bucles de ~9 km / ~2–2h30 desde Nasbinals o desde el parking de la cascada. Variante corta: solo cascada + lago Salhiens 6–8 km.</p>
{links([
 ("AllTrails bucle Cascada del Déroc","https://www.alltrails.com/trail/france/lozere/boucle-de-la-cascade-du-deroc","w"),
 ("PDF PR Déroc–Peyrade (PNR)","https://admin-pnrgca.openig.org/api/fr/treks/51051/du-deroc-a-la-peyrade.pdf","w"),
 ("Turismo Lozère","https://www.lozere-tourisme.com/patrimoine-naturel/cascade-du-deroc/","w"),
 ("Wikiloc Cascada del Déroc","https://es.wikiloc.com/wikiloc/view.do?q=Cascade+du+D%C3%A9roc+Nasbinals","w"),
 ("Ideas Decathlon Outdoor","https://www.decathlon-outdoor.com/fr-fr/inspire/france/randonnee-cascade-du-deroc-lozere","w"),
])}
</div>
<div class="trail">
<h4>Plan B · viento / patous densos</h4>
<p>Pueblo Nasbinals + descanso. Abortar si tormenta eléctrica (no hay abrigo en la meseta).</p>
</div>
{links([("P4N #5073","https://park4night.com/es/place/5073","o"),("Google Nasbinals","https://www.google.com/maps/search/?api=1&query=Nasbinals","g")])}
"""))

    parts.append(day_shell("d12", "Día 12 · Lunes 17 — Aubrac → Capcir",
        ["~280–320 km", "salir <9:00", "P4N #2547"],
        f"""
{img('formigueres','Formiguères')}
<p>El traslado más largo. Partid temprano, parad cada 1h30. El premio es volver a dormir alto y fresco en Formiguères.</p>
<h4>Dónde dormir</h4>
<p><strong>#2547 Calmazeille</strong>: elegid parking de tierra / inferior junto lago, no la fila de AC del asfalto. Plan B: Matemale (#294842) — ojo barrera de altura ~2,0–2,2 m en temporada.</p>
{quote('RouilleP','28/02/2025','Pernocta posible… Gracias al ayuntamiento.')}
<p>Al llegar: 4–6 km bosque. Nada más.</p>
{links([
 ("Google Formiguères","https://www.google.com/maps/dir/?api=1&destination=42.6241,2.0711&travelmode=driving","g"),
 ("P4N #2547","https://park4night.com/es/place/2547","o"),
 ("P4N #294842 Matemale","https://park4night.com/es/place/294842","o"),
])}
"""))

    parts.append(day_shell("d13", "Día 13 · Martes 18 — Capcir / Camporells o lago",
        ["Local", "día colchón", "P4N #2547"],
        f"""
{img('matemale','Lago de Matemale')}
<p>Último día pleno con perras. Camporells (espacio natural clasificado): <strong>perros con correa</strong>. Si un tramo hacia Carlit entra en reserva natural → cancelar y volver al lago.</p>
<div class="trail">
<h4>Plan A · Camporells (si estáis enteros)</h4>
<p>Lagos bajo los Péric, refugio, pinares de altura. Variantes de 3–5 h+. Hay bucles largos y duros (Lladure); no hace falta el más exigente.</p>
{links([
 ("Visorando Camporells por Lladure","https://www.visorando.com/randonnee-boucle-des-camporells-par-la-vallee-de-l/","w"),
 ("Visorando Esposolla–Camporells","https://www.visorando.com/randonnee-d-esposolla-aux-lacs-des-camporells/","w"),
 ("Wikiloc Formiguères lago Olive","https://es.wikiloc.com/rutas-senderismo/formigueres-lac-de-lolive-111344412","w"),
 ("Wikiloc vista 111344412","https://es.wikiloc.com/wikiloc/view.do?id=111344412","w"),
 ("Google Camporells","https://www.google.com/maps/search/?api=1&query=%C3%89tangs+des+Camporells","g"),
])}
</div>
<div class="trail">
<h4>Plan B · Lago de Matemale / bosques Formiguères</h4>
<p>8–10 km casi llanos alrededor del lago o pinares. Perfecto si necesitáis suavidad. Verificar altura de barrera antes de entrar con la Sunlight.</p>
{links([
 ("Google Matemale","https://www.google.com/maps/search/?api=1&query=Lac+de+Matemale","g"),
 ("Wikipedia Matemale", WIKI['matemale']['wiki'], "p"),
 ("AllTrails Matemale","https://www.alltrails.com/explore?q=Matemale","w"),
])}
</div>
"""))

    parts.append(day_shell("d14", "Día 14 · Miércoles 19 — Capcir → Teià",
        ["~180–200 km / 2h30–3h"],
        f"""
<p>Regreso por Cerdanya / Puigcerdà. Alternativa si hay retenciones. Parada café y paseo corto si hace falta. Fin de ruta: misma casa, otras piernas.</p>
{links([
 ("Google Formiguères → Teià","https://www.google.com/maps/dir/Formigu%C3%A8res,+France/Tei%C3%A0,+Spain","g"),
])}
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
<li><a href="https://park4night.com/es/place/6527" target="_blank" rel="noopener">#6527</a> Col de la Core</li>
<li><a href="https://park4night.com/es/place/24616" target="_blank" rel="noopener">#24616</a> Guzet</li>
<li><a href="https://park4night.com/es/place/13709" target="_blank" rel="noopener">#13709</a> Combe Nègre</li>
<li><a href="https://park4night.com/es/place/271257" target="_blank" rel="noopener">#271257</a> Ferme Fouey</li>
<li><a href="https://park4night.com/es/place/144306" target="_blank" rel="noopener">#144306</a> Saint-Bonnet</li>
<li><a href="https://park4night.com/es/place/5073" target="_blank" rel="noopener">#5073</a> Cascada del Déroc</li>
<li><a href="https://park4night.com/es/place/2547" target="_blank" rel="noopener">#2547</a> Formiguères</li>
<li><a href="https://park4night.com/es/place/294842" target="_blank" rel="noopener">#294842</a> Matemale</li>
<li><a href="https://park4night.com/es/place/5896" target="_blank" rel="noopener">#5896</a> Entraygues Rue de la Grave</li>
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
