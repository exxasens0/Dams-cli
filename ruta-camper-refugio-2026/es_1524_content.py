"""Spain Pyrenees camper guide 16–24 Aug 2026 — HTML builder (≤25°C bases)."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_es1524.json").read_text())

TEIA = (2.319, 41.498)
CAN = (-0.525, 42.750)   # Canfranc Estación
SAL = (-0.336, 42.773)   # Sallent de Gállego
OCH = (-1.079, 42.906)   # Ochagavía
BAZ = (-1.515, 43.148)   # Elizondo (Plan B Navarra)

P = {
    "teia": "Teià (Barcelona)",
    "can": "Canfranc Estación (Huesca)",
    "sal": "Sallent de Gállego (Huesca)",
    "och": "Ochagavía (Navarra)",
    "baztan": "Elizondo · Valle del Baztán (Navarra)",
    "irati": "Selva de Irati (Navarra)",
    "lanuza": "Lanuza / Formigal (Huesca)",
}


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def gmaps_dir(olon: float, olat: float, dlon: float, dlat: float) -> str:
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}&travelmode=driving"
    )


def gmaps_route(stops: list[tuple[float, float]]) -> str:
    """Ruta multi-parada: lista de (lon, lat); primera = origen, última = destino."""
    if len(stops) < 2:
        return ""
    olon, olat = stops[0]
    dlon, dlat = stops[-1]
    url = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}"
    )
    mid = stops[1:-1]
    if mid:
        url += "&waypoints=" + "|".join(f"{lat},{lon}" for lon, lat in mid)
    return url + "&travelmode=driving"


# Pirineo alto: únicas bases con sensación ≤25°C en las fechas del viaje
GMAPS_LOOP = gmaps_route([TEIA, CAN, SAL, OCH, TEIA])


def gmaps_pin(lat: float, lon: float, label: str = "") -> str:
    if label:
        return f"https://www.google.com/maps/search/?api=1&query={label.replace(' ', '+')}"
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"


def btn(label: str, url: str, kind: str = "g") -> str:
    cls = {"g": "btn btn-g", "o": "btn btn-o", "w": "btn btn-w", "p": "btn btn-p"}.get(kind, "btn")
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def btns(items: list[tuple[str, str, str]]) -> str:
    return '<div class="btns">' + "".join(btn(l, u, k) for l, u, k in items) + "</div>"


CSS = r"""
:root{--bg:#f2eee4;--ink:#1a221c;--muted:#4d5c52;--card:#fffdf8;--pine:#1b4a3b;--clay:#9a5528;--line:#d7cdbc;--shadow:0 14px 32px rgba(26,34,28,.09);--sec:#e8efe9}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"Source Sans 3",system-ui,sans-serif;color:var(--ink);background:radial-gradient(900px 420px at 0% 0%,#dfe8df,transparent 55%),var(--bg);line-height:1.55}
.wrap{max-width:920px;margin:0 auto;padding:0 1rem 4rem}
.top{position:sticky;top:0;z-index:50;background:rgba(242,238,228,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.6rem;padding:.55rem 0}
.brand{font-family:"Fraunces",serif;font-weight:700;color:var(--pine)}.brand small{display:block;font-family:"Source Sans 3",sans-serif;font-size:.72rem;font-weight:400;color:var(--muted)}
.btn{display:inline-block;padding:.45rem .75rem;border-radius:8px;font-size:.82rem;font-weight:600;text-decoration:none;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.btn-p{background:var(--pine);color:#fff;border-color:var(--pine)}.btn-g{background:#eef4ee}.btn-o{background:#fff3e6}.btn-w{background:#f5f0ff}
.hero{padding:1.5rem 0 1rem}.hero h1{font-family:"Fraunces",serif;font-size:clamp(1.6rem,4vw,2.2rem);margin:.4rem 0}
.lead{color:var(--muted);max-width:42rem}.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.6rem}
.chip{font-size:.72rem;font-weight:700;background:var(--sec);color:var(--pine);padding:.25rem .55rem;border-radius:999px}
.section{margin:2rem 0}.section>h2{font-family:"Fraunces",serif;color:var(--pine);border-bottom:2px solid var(--clay);padding-bottom:.35rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem;margin:1rem 0;box-shadow:var(--shadow)}
.warn{background:#fff4e6;border-left:4px solid var(--clay);padding:.75rem 1rem;border-radius:8px;margin:.75rem 0}
.callout{background:var(--sec);padding:.75rem 1rem;border-radius:8px;margin:.75rem 0}
.day-nav{position:sticky;top:52px;z-index:40;display:grid;grid-template-columns:repeat(5,1fr);gap:.25rem;background:rgba(242,238,228,.96);padding:.45rem 0;margin:0 -1rem;padding-left:1rem;padding-right:1rem;backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
@media(min-width:640px){.day-nav{grid-template-columns:repeat(9,1fr)}}
.day-nav a{font-size:.68rem;text-align:center;padding:.35rem .2rem;border-radius:6px;text-decoration:none;color:var(--pine);font-weight:700;background:var(--card);border:1px solid var(--line)}
.day-nav a:hover{background:var(--sec)}
.day-card{background:var(--card);border:1px solid var(--line);border-radius:16px;margin:1.5rem 0;overflow:hidden;box-shadow:var(--shadow)}
.day-card-head{background:linear-gradient(135deg,var(--pine),#2a6b55);color:#fff;padding:1rem 1.15rem}
.day-card-head h3{margin:0;font-family:"Fraunces",serif;font-size:1.15rem}
.day-card-head .sub{opacity:.9;font-size:.85rem;margin-top:.25rem}
.day-sec{padding:.85rem 1.15rem;border-top:1px solid var(--line)}
.day-sec h4{margin:0 0 .5rem;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--clay)}
.day-sec.route{background:#f8faf8}.day-sec.sleep{background:#f5f8f5}.day-sec.camp{background:#faf8f5}
.day-sec.dist{padding:0}.day-sec.visits{background:#fff}.day-sec.meteo{background:#f0f6fa}.day-sec.notes{background:#fafafa}
.dist-table{width:100%;border-collapse:collapse;font-size:.85rem}
.dist-table th,.dist-table td{padding:.45rem .5rem;border-bottom:1px solid var(--line);text-align:left}
.dist-table th{background:var(--sec);font-size:.72rem;text-transform:uppercase;color:var(--muted)}
.tag-dog-ok{color:var(--pine);font-weight:700}.tag-dog-no{color:#a33;font-weight:700}
.spot{margin:.5rem 0;padding:.6rem .75rem;background:var(--sec);border-radius:8px;font-size:.9rem}
.spot strong{display:block;color:var(--pine)}
.live-plan .card{margin-top:1rem}
.foot{padding:2rem 0;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line)}
details.archive{margin:2rem 0}details.archive summary{cursor:pointer;font-weight:700;color:var(--muted)}
.fab{position:fixed;bottom:1rem;right:1rem;display:flex;gap:.4rem;z-index:60}
.wx-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.5rem;font-size:.88rem}
@media(min-width:520px){.wx-grid{grid-template-columns:repeat(4,1fr)}}
"""


def weather_block(day_num: int) -> str:
    w = next((d for d in WEATHER["days"] if d["day"] == day_num), None)
    if not w:
        return "<p>Meteo no disponible.</p>"
    tips = "".join(f"<li>{esc(t)}</li>" for t in w.get("tips", []))
    return f"""<div class="wx-grid">
<div><em>Base</em><strong>{esc(w.get('place_label') or w['place'])}</strong></div>
<div><em>Temp</em><strong>{w['t_min']:.0f}–{w['t_max']:.0f}°C</strong></div>
<div><em>Sensación máx</em><strong>{w['app_max']:.0f}°C</strong></div>
<div><em>Lluvia</em><strong>{w['precip_mm']:.1f} mm · {w['precip_prob']:.0f}%</strong></div>
</div>
<ul>{tips}</ul>
<p style="font-size:.78rem;color:var(--muted)">Open-Meteo · {esc(WEATHER['fetched_at'][:10])} · revisar a las 7:00</p>"""


def dist_table(rows: list[tuple[str, str, str, str, str]]) -> str:
    trs = []
    for poi, km, mins, dogs, url in rows:
        dog_cls = "tag-dog-ok" if dogs.startswith("OK") else "tag-dog-no"
        link = f'<a href="{esc(url)}" target="_blank" rel="noopener">Maps</a>' if url else "—"
        trs.append(
            f"<tr><td>{esc(poi)}</td><td>{esc(km)}</td><td>{esc(mins)}</td>"
            f'<td class="{dog_cls}">{esc(dogs)}</td><td>{link}</td></tr>'
        )
    return f"""<table class="dist-table">
<thead><tr><th>POI</th><th>Km</th><th>Min</th><th>Perras</th><th></th></tr></thead>
<tbody>{"".join(trs)}</tbody></table>"""


def day_card(
    did: str,
    title: str,
    subtitle: str,
    route_html: str,
    sleep_html: str,
    camp_html: str,
    dist_rows: list[tuple[str, str, str, str, str]],
    visits_html: str,
    day_num: int,
    notes_html: str,
) -> str:
    return f"""<article class="day-card" id="{did}">
<div class="day-card-head"><h3>{esc(title)}</h3><div class="sub">{esc(subtitle)}</div></div>
<section class="day-sec route"><h4>🚐 Ruta al sitio</h4>{route_html}</section>
<section class="day-sec sleep"><h4>🅿️ Dónde dormir · Google Maps</h4>{sleep_html}</section>
<section class="day-sec camp"><h4>⛺ Campings / emergencia (P4N)</h4>{camp_html}</section>
<section class="day-sec dist"><h4>📏 Distancias desde pernocta</h4>{dist_table(dist_rows)}</section>
<section class="day-sec visits"><h4>🥾 Visitas posibles</h4>{visits_html}</section>
<section class="day-sec meteo"><h4>🌡️ Meteo del día</h4>{weather_block(day_num)}</section>
<section class="day-sec notes"><h4>⚠️ Notas</h4>{notes_html}</section>
</article>"""


def spot(name: str, lat: float, lon: float, why: str, risk: str = "") -> str:
    risk_html = f"<br><em>Riesgo:</em> {esc(risk)}" if risk else ""
    return f"""<div class="spot"><strong>{esc(name)}</strong>
{esc(why)}{risk_html}<br>{btn("Abrir en Google Maps", gmaps_pin(lat, lon), "g")}</div>"""


def build_days() -> str:
    parts = []

    parts.append(day_card(
        "d1", "Día 1 · Domingo 16 agosto", f"{P['teia']} → {P['can']} · ~350 km · ~4–5 h",
        f"""<p><strong>Salida domingo</strong> — revisar meteo a las <strong>7:00</strong> antes de cargar. Tramo largo permitido (ida).</p>
{btns([("Google · Teià → Canfranc", gmaps_dir(*TEIA, *CAN), "g")])}
<div class="warn"><strong>⚠️ Lluvia en llegada (Open-Meteo):</strong> llovizna ~11–22 h (89% prob, ≈5 mm). <strong>Sin hike.</strong> Salid cuando la carretera esté seca; llegada ~12–14 h.</div>
<p>Plan B al llegar: estación + pueblo · sensación ~22°C.</p>""",
        (
            spot("Parking Canfranc Estación", 42.751, -0.516,
                 "Pueblo fronterizo: aparcamientos amplios junto a la estación. Satélite: sin salida.",
                 "Agosto: turismo día")
            + spot("Área servicio A-136", 42.745, -0.530,
                   "Alternativa si estación llena.", "Carretera")
        ),
        """<ul><li>Camping pequeños valle (emergencia)</li></ul>""",
        [("Estación Canfranc (exterior)", "0,2", "3", "OK paseo", gmaps_pin(42.751, -0.516)),
         ("Villa de Canfranc", "0", "3", "OK", gmaps_pin(42.751, -0.516))],
        f"""<ol><li><strong>7:00</strong> — consultar meteo; si OK → salir de Teià</li>
<li><strong>Solo conducción + pernocta</strong> — sin senderismo</li>
<li>Tarde lluvia: estación / museo / gastro pueblo</li></ol>
{btns([("Museo estación Canfranc", "https://www.canfranc.es/turismo/estacion-internacional/", "w")])}""",
        1, "<p>Sábado 15 en casa (evitáis lluvia sáb + conducción bajo tormenta). Primer hike → <strong>lunes 17</strong>.</p>",
    ))

    parts.append(day_card(
        "d2", "Día 2 · Lunes 17", f"{P['can']} · Ibón de Estanes",
        f"""<p><strong>Sin traslado.</strong> Meteo mejora (≈0,7 mm, 29% prob) — <strong>primer hike del viaje</strong>.</p>""",
        spot("Misma pernocta D1", 42.751, -0.516, "Segunda noche Canfranc.", ""),
        """<ul><li>—</li></ul>""",
        [("Ibón de Estanes", "12", "20", "OK atado", gmaps_pin(42.78, -0.48)),
         ("Valle de Canfranc", "5", "10", "OK", gmaps_pin(42.751, -0.516)),
         ("Bosque de la Mina", "8", "15", "OK", gmaps_pin(42.76, -0.50))],
        """<ol><li><strong>7:00–12:00 · Ibón de Estanes</strong> (ibón, sombra)</li>
<li>Tarde: si llueve → valle / pueblo</li></ol>""",
        2, "<p>Patous posibles — correa antes del rebaño.</p>",
    ))

    parts.append(day_card(
        "d3", "Día 3 · Martes 18", f"{P['can']} · Selva de Oza",
        f"<p><strong>Sin traslado.</strong> Día seco (0 mm) · sensación ~24°C.</p>",
        spot("Base Canfranc", 42.751, -0.516, "Tercera noche.", ""),
        """<ul><li>—</li></ul>""",
        [("Selva de Oza / Respomuso", "15", "25", "OK atado", gmaps_pin(42.82, -0.45)),
         ("Ruta Bosque de la Mina", "10", "15", "OK", gmaps_pin(42.76, -0.50)),
         ("Sallent de Gállego (recce)", "25", "35", "OK", gmaps_pin(42.773, -0.336))],
        """<ol><li><strong>7:00–12:00 · Selva de Oza</strong> (pinar, ibones)</li>
<li>Tarde: reconocer ruta mañana a Sallent</li></ol>""",
        3, "<p>No dejar perras en furgoneta.</p>",
    ))

    parts.append(day_card(
        "d4", "Día 4 · Miércoles 19", f"{P['can']} · último día base",
        f"<p><strong>Sin traslado.</strong> Cuarta noche Canfranc · sensación ~25°C (límite — hike solo mañana).</p>",
        spot("Base Canfranc", 42.751, -0.516, "Última noche antes de Tena.", "Corte hike si ≥25°C"),
        """<ul><li>—</li></ul>""",
        [("Ibón de Estanes (2ª ruta)", "12", "20", "OK", gmaps_pin(42.78, -0.48)),
         ("Canfranc pueblo", "0", "3", "OK", gmaps_pin(42.751, -0.516))],
        """<ol><li>7:00–11:00 hike corto si sensación OK</li>
<li>Tarde: preparar traslado D5</li></ol>""",
        4, "<p>Revisar meteo a las 7:00 — abortar si sube.</p>",
    ))

    parts.append(day_card(
        "d5", "Día 5 · Jueves 20", f"{P['can']} → {P['sal']} · ~45 km · ~1 h",
        f"""<p>Traslado corto al valle de Tena — sensación ~21°C.</p>
{btns([("Google · Canfranc → Sallent de Gállego", gmaps_dir(*CAN, *SAL), "g")])}""",
        (
            spot("Parking embalse Lanuza", 42.658, -0.328,
                 "Vistas ibón, aparcamiento amplio. Satélite: borde embalse.", "Agosto: turistas")
            + spot("Formigal acceso (plan B)", 42.778, -0.378,
                   "Zona estación, comprobar pernocta.", "Masificación")
        ),
        """<ul><li>Camping Lanuza / Formigal (emergencia)</li></ul>""",
        [("Embalse Lanuza", "0,5", "5", "OK paseo", gmaps_pin(42.658, -0.328)),
         ("Formigal bosques", "10", "15", "OK atado", gmaps_pin(42.778, -0.378)),
         ("Sallent pueblo", "2", "5", "OK", gmaps_pin(42.773, -0.336))],
        """<ol><li>Paseo Lanuza tarde (perros)</li>
<li>Gastro: trucha, migas</li></ol>""",
        5, "<p>Mejor clima del tramo Tena — aprovechar D6 AM.</p>",
    ))

    parts.append(day_card(
        "d6", "Día 6 · Viernes 21", f"{P['sal']} · {P['lanuza']}",
        f"<p><strong>Sin traslado.</strong> ~21°C sensación · lluvia posible tarde (≈17 mm).</p>",
        spot("Misma base Lanuza", 42.658, -0.328, "Repetir parking.", ""),
        """<ul><li>Camping emergencia</li></ul>""",
        [("Circular Lanuza–Búbal", "12", "18", "OK atado", gmaps_pin(42.658, -0.328)),
         ("Formigal senderos", "10", "15", "OK", gmaps_pin(42.778, -0.378)),
         ("Piedrafita lago", "15", "20", "OK", gmaps_pin(42.698, -0.315))],
        """<ol><li><strong>7:00–12:00 · Lanuza / Formigal</strong> (bosque, ibón) — ventana seca</li>
<li>Tarde: mover mañana hacia Navarra</li></ol>""",
        6, "<p>Preparar D7 traslado a Roncal (~2 h).</p>",
    ))

    parts.append(day_card(
        "d7", "Día 7 · Sábado 22", f"{P['sal']} → {P['och']} · ~120 km · ~2 h",
        f"""<p>Subida a Navarra — tramo ≤2 h. <strong>Noche 1/2</strong> Roncal (~20°C).</p>
{btns([("Google · Sallent → Ochagavía", gmaps_dir(*SAL, *OCH), "g")])}""",
        (
            spot("Aparcamiento borde Ochagavía", 42.908, -1.082,
                 "Fuera casco empedrado.", "AC 7 m — no entrar pueblo")
            + spot(f"Plan B · {P['baztan']}", 43.148, -1.515,
                   "Si Irati lluvia: Elizondo (Valle del Baztán, Navarra) — comprobar meteo (suele ser más caluroso).",
                   "Baztán a veces >25°C")
        ),
        """<ul><li><a href="https://www.campingelrobledo.com/">Camping Robledo</a></li></ul>""",
        [("Casco Ochagavía", "0,3", "3", "OK paseo", gmaps_pin(42.906, -1.079)),
         ("Selva de Irati", "8", "12", "OK atado", gmaps_pin(42.918, -1.045))],
        """<ol><li>Paseo Roncal tarde</li>
<li>Gastro: cordero, queso Roncal</li></ol>""",
        7, "<p>Lluvia posible tarde — paseo corto pueblo.</p>",
    ))

    parts.append(day_card(
        "d8", "Día 8 · Domingo 23", f"{P['och']} · {P['irati']} · noche 2/2",
        f"""<p><strong>Sin traslado.</strong> Cierre en {P['irati']} (~22°C sensación).</p>
<p>≥2 noches Navarra cumplidas (D7–8).</p>""",
        spot("Misma pernocta D7", 42.908, -1.082, "Repetir parking.", "Domingo: más gente"),
        """<ul><li>Camping Robledo</li></ul>""",
        [("Selva de Irati · Abodi", "8", "12", "OK atado", gmaps_pin(42.918, -1.045)),
         ("Isaba / Burgui", "15", "20", "OK", gmaps_pin(42.925, -1.005)),
         ("Senda río Zatoia", "5", "8", "OK", gmaps_pin(42.910, -1.070))],
        f"""<ol><li><strong>7:00–12:00 · Selva de Irati</strong> — hike AM (lluvia posible tarde)</li>
<li>Tarde: siesta — salida lun 24 temprano</li></ol>
{btns([("Turismo Roncal", "https://www.turismo.navarra.es/es/ver/valle-del-roncal/", "w")])}""",
        8, "<p>Patous — correa. Última noche.</p>",
    ))

    parts.append(day_card(
        "d9", "Día 9 · Lunes 24", f"{P['och']} → {P['teia']} · ~400 km · ~5 h",
        f"""<p><strong>Tramo largo</strong> (vuelta). Solo conducción — costa ~34°C sensación, no hike.</p>
{btns([("Google · Ochagavía → Teià", gmaps_dir(*OCH, *TEIA), "g")])}""",
        "<p><strong>Llegada a casa.</strong></p>",
        "<p>—</p>",
        [],
        "<p>Paradas sombra cada 2 h · AC para perras · salir temprano.</p>",
        9, "<p>Camper al sol en costa = interior 35°C+ — no parar sin sombra.</p>",
    ))

    return "".join(parts)


def live_summary() -> str:
    return f"""
<section class="section live-plan" id="plan-rapido">
<h2>Plan activo · 16–24 agosto 2026 · Pirineo ≤25°C</h2>
<div class="card prose">
<div class="warn"><strong>Cambio de ruta:</strong> Albarracín, Escucha, Morella y Jaca <strong>descartados</strong> — sensación 28–32°C (camper interior ~35°C con perras). Solo bases Pirineo alto ≤25°C.</div>
<div class="callout"><strong>Salida domingo 16</strong> — sábado 15 en casa. Revisar meteo a las 7:00 antes de cargar. Evitáis lluvia sáb + conducción bajo tormenta.</div>
<div class="warn"><strong>Reglas:</strong> hike solo si sensación ≤25°C · ≥2 noches Navarra (D7–8) · tramos ≤2 h (D1/D9 ~5 h).</div>
<div class="callout"><strong>Eje:</strong> {P['can']} (4 noches) → {P['sal']} → {P['och']}/{P['irati']} → {P['teia']}.</div>
<p>{btns([("🗺️ Ruta Google Maps · loop completo", GMAPS_LOOP, "g")])}</p>
<p style="font-size:.85rem;color:var(--muted)">Paradas: {P['teia']} → {P['can']} → {P['sal']} → {P['och']} → {P['teia']}</p>
<ol>
<li><strong>16–19</strong> {P['can']} (Canfranc · ~22–25°C) · primer hike lun 17</li>
<li><strong>20–21</strong> {P['sal']} / {P['lanuza']} (~21°C)</li>
<li><strong>22–23</strong> {P['och']} / {P['irati']} (~20°C) · ≥2 noches</li>
<li><strong>24</strong> → {P['teia']} (solo conducción)</li>
</ol>
</div></section>"""


def gmaps_howto() -> str:
    return """
<section class="section" id="dormir-gmaps"><h2>Buscar pernocta sin Park4Night</h2>
<div class="card prose">
<ol>
<li>Google Maps <strong>satélite</strong> → zoom borde pueblo/bosque.</li>
<li>Buscar: parking sin salida, mirador, acceso forestal ancho (&gt;2,10 m).</li>
<li>Street View / reseñas si existen.</li>
<li>Al llegar: cartel prohibido pernocta → siguiente candidato del día.</li>
<li>Estacionar ≠ acampar: sin toldo, mesa, sillas fuera.</li>
</ol>
<div class="warn">P4N en agosto = masificado. Preferid spots no listados.</div>
</div></section>"""


def rules_section() -> str:
    return f"""
<section class="section" id="perras"><h2>Reglas del viaje</h2>
<div class="card prose">
<div class="warn"><strong>Perras:</strong> solo actividades donde entren con vosotros. Visita sin perros = <strong>cancelada</strong>.</div>
<div class="warn"><strong>Calor:</strong> solo pernocta donde Open-Meteo sensación ≤25°C. Si sube → cancelar hike.</div>
<ul>
<li>Sunlight 600 (&gt;2,10 m) · 2 perras siempre</li>
<li>Conducción ≤2 h entre bases · D1 y D9 ~5 h</li>
<li>≥2 noches Navarra Irati/Baztán (D7–8)</li>
<li><strong>Descartado por calor:</strong> Albarracín, Escucha, Morella, Jaca, interior (28–32°C sensación)</li>
</ul>
</div></section>"""


def day_nav() -> str:
    links = "".join(f'<a href="#d{i}">D{i}</a>' for i in range(1, 10))
    return f'<nav class="day-nav wrap">{links}</nav>'


def render_spain_guide() -> str:
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Guía camper · Pirineo ≤25°C · 16–24 ago 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap top-in">
<div class="brand">Guía camper · Pirineo ≤25°C<small>16–24 agosto 2026 · Salida dom · Huesca · Navarra · Sunlight 600 + 2 perras</small></div>
<div class="btns">
<a class="btn btn-p" href="#plan-rapido">Plan 16–24</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#dormir-gmaps">Dormir GMaps</a>
</div></div></header>
{day_nav()}
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Salida dom 16</span><span class="chip">≤25°C sensación</span><span class="chip">Canfranc · Irati</span><span class="chip">≥2 noches Navarra</span><span class="chip">Perras siempre</span></div>
<h1>Canfranc · Lanuza · Irati</h1>
<p class="lead">Ruta <strong>100 % Pirineo alto</strong>: pernoctas ≤25°C sensación. Salida <strong>domingo 16</strong> tras consultar meteo · vuelta lun 24.</p>
{btns([
    ("🗺️ Ruta completa · Google Maps", GMAPS_LOOP, "g"),
    ("Google · D1 Teià → Canfranc", gmaps_dir(*TEIA, *CAN), "g"),
])}
</section>
{live_summary()}
{gmaps_howto()}
{rules_section()}
<section class="section" id="dias"><h2>Día a día</h2>
{build_days()}
</section>
<details class="archive wrap"><summary>Viaje anterior · Francia 6–19 ago (archivo)</summary>
<p class="card">La guía Francia está en el historial git del repo. Este viaje reemplaza el plan activo.</p>
</details>
<footer class="foot">
<p><strong>Guía camper Pirineo ≤25°C</strong> · 16–24 agosto 2026 · Open-Meteo · Google Maps</p>
<p>Abrir vía raw.githack en el móvil (ver ABRIR-GUIA.md).</p>
</footer>
</main>
<div class="fab"><a class="btn btn-p" href="#d1">D1</a><a class="btn" href="#plan-rapido">Plan</a></div>
</body></html>"""


def main() -> None:
    html_out = render_spain_guide()
    for name in ("guia-movil.html", "guia-lonely-planet.html"):
        (ROOT / name).write_text(html_out, encoding="utf-8")
    print("written", len(html_out), "bytes")
    print("loop:", GMAPS_LOOP)


if __name__ == "__main__":
    main()
