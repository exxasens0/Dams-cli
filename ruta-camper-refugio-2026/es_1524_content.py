"""Spain Pyrenees camper guide 16–26 Aug 2026 — D1-2 Lanuza · D3-5 Canfranc · D6-7 Baztán · D8-9 Ochagavía · D10 Teià."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_es1524.json").read_text())

TEIA = (2.319, 41.498)
SAL = (-0.336, 42.773)
CAN = (-0.525, 42.750)
OCH = (-1.079, 42.906)
BAZ = (-1.515, 43.148)

P = {
    "teia": "Teià (Barcelona)",
    "sal": "Sallent de Gállego (Huesca)",
    "lanuza": "Lanuza / Formigal (Huesca)",
    "can": "Canfranc Estación (Huesca)",
    "och": "Ochagavía (Navarra)",
    "irati": "Selva de Irati (Navarra)",
    "baztan": "Elizondo · Valle del Baztán (Navarra)",
}


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def gmaps_dir(olon: float, olat: float, dlon: float, dlat: float) -> str:
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}&travelmode=driving"
    )


def gmaps_route(stops: list[tuple[float, float]]) -> str:
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


GMAPS_LOOP = gmaps_route([TEIA, SAL, CAN, BAZ, OCH, TEIA])


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
@media(min-width:640px){.day-nav{grid-template-columns:repeat(10,1fr)}}
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
.summary-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0;border:1px solid var(--line);border-radius:12px;background:var(--card);box-shadow:var(--shadow)}
.summary-table{width:100%;border-collapse:collapse;font-size:.82rem;min-width:640px}
.summary-table th,.summary-table td{padding:.55rem .65rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.summary-table th{background:var(--pine);color:#fff;font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0}
.summary-table tr:last-child td{border-bottom:0}
.summary-table tr:hover td{background:#f5faf6}
.summary-table a{color:var(--pine);font-weight:700;text-decoration:none}
.summary-table .wx-ok{color:var(--pine);font-weight:700}
.summary-table .wx-warn{color:var(--clay);font-weight:700}
.summary-table .wx-rain{color:#2a5f8a}
.summary-meta{font-size:.78rem;color:var(--muted);margin:.35rem 0 0}
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
    did: str, title: str, subtitle: str, route_html: str, sleep_html: str,
    camp_html: str, dist_rows: list[tuple[str, str, str, str, str]],
    visits_html: str, day_num: int, notes_html: str,
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
        "d1", "D1 · Domingo 16 · Lanuza", f"{P['teia']} → {P['lanuza']} · ~350 km · ~4–5 h",
        f"""<p><strong>Lanuza primero</strong> (D1–D2). Revisar meteo <strong>7:00</strong> antes de cargar.</p>
{btns([("Google · Teià → Lanuza", gmaps_dir(*TEIA, *SAL), "g")])}
<div class="warn">⚠️ Lluvia llegada (~9 mm). <strong>Sin hike.</strong></div>""",
        (
            spot("Parking embalse Lanuza", 42.658, -0.328,
                 "Aparcamiento amplio borde embalse.", "Agosto: turistas")
            + spot("Formigal acceso (plan B)", 42.778, -0.378,
                   "Comprobar pernocta.", "Masificación")
        ),
        """<ul><li>Camping Lanuza / Formigal (emergencia)</li></ul>""",
        [("Embalse Lanuza", "0,5", "5", "OK paseo", gmaps_pin(42.658, -0.328)),
         ("Sallent pueblo", "2", "5", "OK", gmaps_pin(42.773, -0.336))],
        """<ol><li>Solo conducción + pernocta</li>
<li>Tarde lluvia: camper / gastro Sallent</li></ol>""",
        1, "<p>Noche 1/2 Lanuza.</p>",
    ))

    parts.append(day_card(
        "d2", "D2 · Lunes 17 · Lanuza", f"{P['lanuza']} · noche 2/2",
        f"""<p><strong>Sin traslado.</strong> Sensación ~25°C (límite) — hike solo <strong>mañana</strong> si OK.</p>
<div class="warn">Si sube de 25°C → cancelar hike · preparar Canfranc para mañana.</div>""",
        spot("Misma pernocta Lanuza", 42.658, -0.328, "Segunda noche.", "Calor límite"),
        """<ul><li>Camping emergencia</li></ul>""",
        [("Circular Lanuza–Búbal", "12", "18", "OK atado", gmaps_pin(42.658, -0.328)),
         ("Formigal bosques", "10", "15", "OK", gmaps_pin(42.778, -0.378))],
        """<ol><li>7:00–11:00 paseo / sendero corto si ≤25°C</li>
<li>Tarde: sombra · carga para Canfranc</li></ol>""",
        2, "<p>Mañana D3 → Canfranc (~75 km · ~1h15).</p>",
    ))

    parts.append(day_card(
        "d3", "D3 · Martes 18 · Canfranc", f"{P['lanuza']} → {P['can']} · ~75 km · ~1h15",
        f"""<p>Subida a Canfranc — base fresca D3–D5 (noches 18–21).</p>
{btns([("Google · Sallent → Canfranc", gmaps_dir(*SAL, *CAN), "g")])}
<p>Día seco · <strong>primer hike</strong> Ibón si llegáis con tiempo.</p>""",
        (
            spot("Parking Canfranc Estación", 42.751, -0.516,
                 "Aparcamientos junto a la estación.", "Agosto: turismo")
            + spot("Área A-136", 42.745, -0.530, "Si estación llena.", "Carretera")
        ),
        """<ul><li>Camping valle (emergencia)</li></ul>""",
        [("Ibón de Estanes", "12", "20", "OK atado", gmaps_pin(42.78, -0.48)),
         ("Bosque de la Mina", "8", "15", "OK", gmaps_pin(42.76, -0.50)),
         ("Estación", "0,2", "3", "OK paseo", gmaps_pin(42.751, -0.516))],
        """<ol><li>Traslado AM</li>
<li>Tarde: Ibón de Estanes o valle</li></ol>""",
        3, "<p>Patous — correa. Noche 1 Canfranc.</p>",
    ))

    parts.append(day_card(
        "d4", "D4 · Miércoles 19 · Canfranc", f"{P['can']} · Selva de Oza",
        f"<p><strong>Sin traslado.</strong> Día seco · sensación ~25°C — hike AM.</p>",
        spot("Base Canfranc", 42.751, -0.516, "Noche 2 Canfranc.", ""),
        """<ul><li>—</li></ul>""",
        [("Selva de Oza", "15", "25", "OK atado", gmaps_pin(42.82, -0.45)),
         ("Bosque de la Mina", "10", "15", "OK", gmaps_pin(42.76, -0.50))],
        """<ol><li><strong>7:00–12:00 · Selva de Oza</strong></li>
<li>Tarde: valle</li></ol>""",
        4, "<p>Revisar meteo 7:00.</p>",
    ))

    parts.append(day_card(
        "d5", "D5 · Jueves 20–viernes 21 · Canfranc", f"{P['can']} · cierre base (2 noches)",
        f"""<p><strong>Sin traslado.</strong> Jue 20 fresco (~20°C) · vie 21 lluvia posible (~15 mm).</p>
<div class="warn"><strong>Por qué 2 noches en D5:</strong> el vie 21 Baztán está a ~32°C. Dormís Canfranc jue+vie; <strong>sáb 22</strong> salís a Baztán (ya ≤25°C).</div>""",
        spot("Base Canfranc", 42.751, -0.516, "Noches 3–4 Canfranc (20 y 21).", "Lluvia vie"),
        """<ul><li>—</li></ul>""",
        [("Ibón / valle corto", "12", "20", "OK", gmaps_pin(42.78, -0.48)),
         ("Estación / museo", "0", "3", "OK", gmaps_pin(42.751, -0.516))],
        f"""<ol><li><strong>Jue 20:</strong> hike AM valle / Ibón</li>
<li><strong>Vie 21:</strong> hike corto solo si seco · tarde preparar Baztán</li></ol>
{btns([("Museo estación Canfranc", "https://www.canfranc.es/turismo/estacion-internacional/", "w")])}""",
        5, "<p>Sáb 22: Canfranc → Elizondo ~181 km · ~2h20 (único tramo &gt;2 h entre bases).</p>",
    ))

    parts.append(day_card(
        "d6", "D6 · Sábado 22 · Baztán", f"{P['can']} → {P['baztan']} · ~181 km · ~2h20",
        f"""<p><strong>Valle del Baztán noche 1/2.</strong> Ventana ≤25°C solo 22–23.</p>
{btns([("Google · Canfranc → Elizondo", gmaps_dir(*CAN, *BAZ), "g")])}
<div class="warn">Tramo ~2h20 — excepción Navarra. Salid temprano.</div>""",
        (
            spot("Parking borde Elizondo", 43.148, -1.515,
                 "Fuera casco · satélite valle.", "Agosto: gente")
            + spot("Señorío de Bertiz (exterior)", 43.14, -1.61,
                   "Confirmar perros / horarios.", "Normativa")
        ),
        """<ul><li>Camping / área valle (emergencia)</li></ul>""",
        [("Elizondo casco", "0,3", "5", "OK paseo", gmaps_pin(43.148, -1.515)),
         ("Senderos Baztán", "5", "10", "OK atado", gmaps_pin(43.16, -1.52)),
         ("Bertiz acceso", "12", "15", "Confirmar", gmaps_pin(43.14, -1.61))],
        f"""<ol><li>Traslado AM</li>
<li>Tarde: paseo valle / Elizondo (lluvia posible)</li></ol>
{btns([("Turismo Baztán", "https://www.turismo.navarra.es/es/ver/valle-del-baztan/", "w")])}""",
        6, "<p>Navarra 1/4 noches.</p>",
    ))

    parts.append(day_card(
        "d7", "D7 · Domingo 23 · Baztán", f"{P['baztan']} · noche 2/2",
        f"""<p><strong>Sin traslado.</strong> Última noche fresca en Baztán (~23°C).</p>
<div class="warn">Lun 24 Elizondo ~29°C → mañana a Ochagavía.</div>""",
        spot("Misma pernocta Elizondo", 43.148, -1.515, "Repetir parking.", ""),
        """<ul><li>—</li></ul>""",
        [("Senderos valle", "5", "10", "OK atado", gmaps_pin(43.16, -1.52)),
         ("Elizondo", "0", "5", "OK", gmaps_pin(43.148, -1.515)),
         ("Bertiz", "12", "15", "Confirmar", gmaps_pin(43.14, -1.61))],
        """<ol><li><strong>7:00–12:00</strong> hike / paseo valle</li>
<li>Tarde: siesta · preparar D8</li></ol>""",
        7, "<p>Navarra 2/4. Mañana → Ochagavía ~121 km · ~1h55.</p>",
    ))

    parts.append(day_card(
        "d8", "D8 · Lunes 24 · Ochagavía", f"{P['baztan']} → {P['och']} · ~121 km · ~1h55",
        f"""<p>Escape calor Baztán · <strong>Irati noche 1/2</strong> (~22°C).</p>
{btns([("Google · Elizondo → Ochagavía", gmaps_dir(*BAZ, *OCH), "g")])}
<div class="warn">⚠️ Lluvia fuerte posible (~34 mm) — hike solo si ventana seca; si no, pueblo.</div>""",
        (
            spot("Aparcamiento borde Ochagavía", 42.908, -1.082,
                 "Fuera casco empedrado.", "AC 7 m")
            + spot("Camping Robledo", 42.91, -1.09, "Emergencia con servicios.", "")
        ),
        """<ul><li><a href="https://www.campingelrobledo.com/">Camping Robledo</a></li></ul>""",
        [("Casco Ochagavía", "0,3", "3", "OK", gmaps_pin(42.906, -1.079)),
         ("Selva de Irati", "8", "12", "OK atado", gmaps_pin(42.918, -1.045))],
        """<ol><li>Salir Elizondo temprano</li>
<li>Si seco: Irati tarde corta</li>
<li>Si lluvia: Roncal / gastro</li></ol>""",
        8, "<p>Navarra 3/4.</p>",
    ))

    parts.append(day_card(
        "d9", "D9 · Martes 25 · Ochagavía", f"{P['och']} · {P['irati']} · noche 2/2",
        f"""<p><strong>Sin traslado.</strong> Cierre Irati (~21°C). Lluvia posible — hike AM.</p>""",
        spot("Misma pernocta D8", 42.908, -1.082, "Última noche viaje.", "Lluvia"),
        """<ul><li>Camping Robledo</li></ul>""",
        [("Selva de Irati · Abodi", "8", "12", "OK atado", gmaps_pin(42.918, -1.045)),
         ("Senda río Zatoia", "5", "8", "OK", gmaps_pin(42.910, -1.070)),
         ("Isaba / Burgui", "15", "20", "OK", gmaps_pin(42.925, -1.005))],
        f"""<ol><li><strong>7:00–12:00 · Irati</strong> si seco</li>
<li>Tarde: siesta · salida mié 26 temprano</li></ol>
{btns([("Turismo Roncal", "https://www.turismo.navarra.es/es/ver/valle-del-roncal/", "w")])}""",
        9, "<p>Navarra 4/4 · ≥2 noches cumplidas (Baztán + Irati).</p>",
    ))

    parts.append(day_card(
        "d10", "D10 · Miércoles 26 · Teià", f"{P['och']} → {P['teia']} · ~435 km · ~5–6 h",
        f"""<p><strong>Vuelta.</strong> Solo conducción — costa ~30°C+ sensación.</p>
{btns([("Google · Ochagavía → Teià", gmaps_dir(*OCH, *TEIA), "g")])}""",
        "<p><strong>Llegada a casa.</strong></p>",
        "<p>—</p>",
        [],
        "<p>Paradas sombra cada 2 h · AC perras · salir temprano.</p>",
        10, "<p>No parar al sol sin sombra — interior camper 35°C+.</p>",
    ))

    return "".join(parts)


WEEKDAYS_ES = {
    0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
    4: "viernes", 5: "sábado", 6: "domingo",
}


def _weekday_es(date_iso: str) -> str:
    from datetime import date
    y, m, d = map(int, date_iso.split("-"))
    return WEEKDAYS_ES[date(y, m, d).weekday()]


def _fmt_fecha(date_iso: str) -> str:
    y, m, d = date_iso.split("-")
    return f"{_weekday_es(date_iso)} {int(d)} ago"


# Filas del cuadro resumen: (día, fecha_iso, lugar corto, tramo, km, maps_url)
SUMMARY_ROWS = [
    (1, "2026-08-16", "Lanuza (Huesca)", "Teià → Lanuza", "350 km · 4–5 h", gmaps_dir(*TEIA, *SAL)),
    (2, "2026-08-17", "Lanuza (Huesca)", "Sin traslado", "—", gmaps_pin(42.658, -0.328)),
    (3, "2026-08-18", "Canfranc (Huesca)", "Lanuza → Canfranc", "75 km · 1h15", gmaps_dir(*SAL, *CAN)),
    (4, "2026-08-19", "Canfranc (Huesca)", "Sin traslado", "—", gmaps_pin(42.751, -0.516)),
    (5, "2026-08-20", "Canfranc (Huesca)", "Sin traslado · noches 20+21", "—", gmaps_pin(42.751, -0.516)),
    (6, "2026-08-22", "Elizondo / Baztán (Navarra)", "Canfranc → Elizondo", "181 km · 2h20", gmaps_dir(*CAN, *BAZ)),
    (7, "2026-08-23", "Elizondo / Baztán (Navarra)", "Sin traslado", "—", gmaps_pin(43.148, -1.515)),
    (8, "2026-08-24", "Ochagavía / Irati (Navarra)", "Elizondo → Ochagavía", "121 km · 1h55", gmaps_dir(*BAZ, *OCH)),
    (9, "2026-08-25", "Ochagavía / Irati (Navarra)", "Sin traslado", "—", gmaps_pin(42.906, -1.079)),
    (10, "2026-08-26", "Teià (Barcelona)", "Ochagavía → Teià", "435 km · 5–6 h", gmaps_dir(*OCH, *TEIA)),
]


def summary_table() -> str:
    wx_by_day = {d["day"]: d for d in WEATHER["days"]}
    rows_html = []
    for day, date_iso, lugar, tramo, dist, maps_url in SUMMARY_ROWS:
        w = wx_by_day.get(day)
        if w:
            app = w["app_max"]
            mm = w["precip_mm"]
            prob = w["precip_prob"]
            wx_cls = "wx-ok" if app <= 25 else "wx-warn"
            clima = (
                f'<span class="{wx_cls}">sens. {app:.0f}°C</span><br>'
                f'<span class="wx-rain">{mm:.0f} mm · {prob:.0f}%</span>'
            )
        else:
            clima = "—"
        fecha = _fmt_fecha(date_iso)
        fecha_extra = ""
        if day == 5:
            fecha = "jueves 20–viernes 21 ago"
            fecha_extra = ""
        rows_html.append(
            f"<tr>"
            f'<td><a href="#d{day}">D{day}</a></td>'
            f"<td>{esc(fecha)}{fecha_extra}</td>"
            f"<td><strong>{esc(lugar)}</strong></td>"
            f"<td>{esc(tramo)}<br><span style=\"color:var(--muted)\">{esc(dist)}</span></td>"
            f"<td>{clima}</td>"
            f'<td><a href="{esc(maps_url)}" target="_blank" rel="noopener">Maps</a></td>'
            f"</tr>"
        )
    return f"""
<div class="summary-wrap">
<table class="summary-table">
<thead>
<tr>
<th>Día</th>
<th>Fecha</th>
<th>Lugar</th>
<th>Tramo · km</th>
<th>Clima</th>
<th>Ruta</th>
</tr>
</thead>
<tbody>
{"".join(rows_html)}
</tbody>
</table>
</div>
<p class="summary-meta">Clima = sensación máx + lluvia (Open-Meteo · {esc(WEATHER['fetched_at'][:10])}). Revisar a las 7:00.</p>
<p>{btns([("🗺️ Ruta completa · todo el loop", GMAPS_LOOP, "g")])}</p>
"""


def live_summary() -> str:
    return f"""
<section class="section live-plan" id="plan-rapido">
<h2>Cuadro resumen · 16–26 agosto 2026</h2>
{summary_table()}
<div class="warn"><strong>D5 = jue 20 + vie 21</strong> en Canfranc: el vie 21 Baztán ~32°C; Baztán fresco solo <strong>22–23</strong>.</div>
<div class="callout">Hike solo si sensación ≤25°C · perras siempre · D6 ~2h20 excepción.</div>
</section>"""


def gmaps_howto() -> str:
    return """
<section class="section" id="dormir-gmaps"><h2>Buscar pernocta sin Park4Night</h2>
<div class="card prose">
<ol>
<li>Google Maps <strong>satélite</strong> → zoom borde pueblo/bosque.</li>
<li>Parking sin salida, mirador, acceso &gt;2,10 m.</li>
<li>Cartel prohibido → siguiente candidato.</li>
<li>Estacionar ≠ acampar (sin toldo/mesa fuera).</li>
</ol>
</div></section>"""


def rules_section() -> str:
    return f"""
<section class="section" id="perras"><h2>Reglas</h2>
<div class="card prose">
<div class="warn"><strong>Perras:</strong> solo donde entren con vosotros.</div>
<div class="warn"><strong>Calor:</strong> pernocta solo si sensación ≤25°C.</div>
<ul>
<li>Sunlight 600 · 2 perras</li>
<li>≤2 h entre bases (D6 ~2h20 excepción · D1/D10 largos)</li>
<li>Navarra: Baztán D6–D7 + Irati D8–D9</li>
</ul>
</div></section>"""


def day_nav() -> str:
    links = "".join(f'<a href="#d{i}">D{i}</a>' for i in range(1, 11))
    return f'<nav class="day-nav wrap">{links}</nav>'


def render_spain_guide() -> str:
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Guía camper · 16–26 ago 2026 · Lanuza · Canfranc · Baztán · Irati</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap top-in">
<div class="brand">Guía camper · ≤25°C<small>16–26 ago · D1-2 Lanuza · D3-5 Canfranc · D6-7 Baztán · D8-9 Irati · D10 Teià</small></div>
<div class="btns">
<a class="btn btn-p" href="#plan-rapido">Plan</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#dormir-gmaps">Dormir</a>
</div></div></header>
{day_nav()}
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">D1–2 Lanuza</span><span class="chip">D3–5 Canfranc</span><span class="chip">D6–7 Baztán</span><span class="chip">D8–9 Ochagavía</span><span class="chip">D10 Teià</span></div>
<h1>Lanuza · Canfranc · Baztán · Irati</h1>
<p class="lead">Salida <strong>dom 16</strong> · vuelta <strong>mié 26</strong>. Orden inteligente: Lanuza primero, Baztán en su ventana fresca (22–23), Irati 24–25.</p>
{btns([("🗺️ Ruta completa", GMAPS_LOOP, "g"), ("D1 Teià → Lanuza", gmaps_dir(*TEIA, *SAL), "g")])}
</section>
{live_summary()}
{gmaps_howto()}
{rules_section()}
<section class="section" id="dias"><h2>Día a día</h2>
{build_days()}
</section>
<footer class="foot">
<p><strong>Guía camper</strong> · 16–26 agosto 2026 · Open-Meteo · Google Maps</p>
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
