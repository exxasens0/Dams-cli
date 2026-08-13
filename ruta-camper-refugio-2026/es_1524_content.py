"""Spain interior camper guide 15–24 Aug 2026 — HTML builder."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_es1524.json").read_text())

TEIA = (2.319, 41.498)
ALB = (-1.444, 40.407)
ESC = (-1.065, 40.765)
MOR = (-0.100, 40.619)
VEO = (-0.280, 39.950)


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def gmaps_dir(olon: float, olat: float, dlon: float, dlat: float) -> str:
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={olat},{olon}&destination={dlat},{dlon}&travelmode=driving"
    )


def gmaps_pin(lat: float, lon: float, label: str = "") -> str:
    q = f"{lat},{lon}"
    if label:
        q = label.replace(" ", "+")
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
"""


def weather_block(day_num: int) -> str:
    w = next((d for d in WEATHER["days"] if d["day"] == day_num), None)
    if not w:
        return "<p>Meteo no disponible.</p>"
    tips = "".join(f"<li>{esc(t)}</li>" for t in w.get("tips", []))
    return f"""<div class="wx-grid">
<div><em>Base</em><strong>{esc(w['place'])}</strong></div>
<div><em>Temp</em><strong>{w['t_min']:.0f}–{w['t_max']:.0f}°C</strong></div>
<div><em>Sensación máx</em><strong>{w['app_max']:.0f}°C</strong></div>
<div><em>Lluvia</em><strong>{w['precip_mm']:.1f} mm · {w['precip_prob']:.0f}%</strong></div>
</div>
<ul>{tips}</ul>
<p style="font-size:.78rem;color:var(--muted)">Open-Meteo · {esc(WEATHER['fetched_at'][:10])} · revisar a las 7:00</p>"""


def dist_table(rows: list[tuple[str, str, str, str, str, str]]) -> str:
    """poi, km, min, dogs, url"""
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
        "d1", "Día 1 · Sábado 15 agosto", "Teià → Albarracín · ~280 km · ~5 h",
        f"""<p><strong>Tramo largo permitido</strong> (solo ida/vuelta).</p>
{btns([("Google · Teià → Albarracín", gmaps_dir(*TEIA, *ALB), "g")])}
<p>Llegada tarde: sin hike. Sombra, agua, paseo corto pueblo si sensación baja.</p>""",
        (
            spot("Parking Tejería / borde Guadalaviar", 40.412, -1.443,
                 "Sin salida junto al río, sombra de pinos. Mirad satélite: evitar casco muy estrecho.",
                 "Agosto: algo de tráfico pescadores AM")
            + spot("Mirador murallas (atardecer)", 40.405, -1.448,
                   "Aparcamiento ancho junto a muralla — solo estacionar, no acampar.",
                   "Pendiente leve en algunas plazas")
        ),
        """<p><em>P4N suele ir lleno en agosto.</em></p>
<ul><li><strong>Plan B:</strong> <a href="https://park4night.com/es/place/390083">P4N #390083</a> Tejería</li>
<li><strong>Plan C:</strong> <a href="https://www.campingalbarracin.com/">Camping Ciudad de Albarracín</a></li></ul>""",
        [("Casco Albarracín", "1", "5", "OK paseo", gmaps_pin(40.407, -1.444)),
         ("Pinares Rodeno", "8", "12", "OK atado", gmaps_pin(40.45, -1.38)),
         ("Guadalaviar río", "2", "5", "OK", gmaps_pin(40.408, -1.442))],
        """<ol><li>Paseo murallas / Guadalaviar (tarde/noche si fresco)</li>
<li>Gastro: mesón cordero (reserva)</li></ol>""",
        1, "<p>Perras atadas. Estacionar ≠ acampar (sin toldo/mesas fuera).</p>",
    ))

    parts.append(day_card(
        "d2", "Día 2 · Domingo 16", "Albarracín · Rodeno",
        "<p><strong>Sin traslado.</strong> Base Albarracín.</p>",
        (
            spot("Mismo parking D1 o Rodeno acceso", 40.45, -1.38,
                 "Acceso Pinares: aparcamientos forestales amplios, sombra de pino rodeno.",
                 "Finde: más coches de día — pernocta mejor en Tejería")
            + spot("Alternativa: Camping Albarracín", 40.401, -1.435,
                   "Sombra y duchas si GMaps falla.", "Reserva agosto")
        ),
        """<ul><li><a href="https://park4night.com/es/place/390083">#390083</a> (saturado)</li>
<li><a href="https://www.campingalbarracin.com/">Camping Albarracín</a></li></ul>""",
        [("Pinares de Rodeno", "8", "12", "OK atado", gmaps_pin(40.45, -1.38)),
         ("Sendero PR-TE-08", "10", "15", "OK", gmaps_pin(40.44, -1.37)),
         ("Albarracín casco", "1", "5", "OK exterior", gmaps_pin(40.407, -1.444))],
        f"""<ol><li><strong>7:00–11:00 · Pinares de Rodeno</strong> (corte si sensación ≥25°C)</li>
<li>Tarde: siesta / pueblo / Guadalaviar</li>
<li>Gastro: cordero, setas (temporada)</li></ol>
{btns([("Turismo Albarracín mascotas", "https://albarracinturismo.com/viajar-con-mascotas-albarracin-teruel/", "w")])}""",
        2, "<p>Día caluroso tarde. Hike solo mañana.</p>",
    ))

    parts.append(day_card(
        "d3", "Día 3 · Lunes 17", "Albarracín → Escucha · ~90 km · ~1,5 h",
        f"""<p>Traslado ≤2 h. Salida mañana post-Rodeno o mediodía.</p>
{btns([("Google · Albarracín → Escucha", gmaps_dir(*ALB, *ESC), "g")])}""",
        (
            spot("Parking N-420 borde Escucha", 40.762, -1.068,
                 "Zona industrial/minera, aparcamiento amplio sin salida. Comprobar cartel.",
                 "Día: camiones mineros")
            + spot("Barrio sur pueblo minero", 40.758, -1.062,
                   "Calles amplias, poco tráfico nocturno.", "Pendiente")
        ),
        """<ul><li>Área CC junto museo (reseñas camper; confirmar al llegar)</li>
<li><a href="https://www.museomineroescucha.es/">Museo Minero</a> parking</li></ul>""",
        [("Museo Minero Escucha", "0,5", "3", "Confirmar", "https://www.museomineroescucha.es/"),
         ("Ruta digital pueblo minero", "1", "5", "OK", gmaps_pin(40.765, -1.065)),
         ("Maquinaria exterior mina", "0,3", "2", "OK", gmaps_pin(40.764, -1.067))],
        """<ol><li>Patrimonio minero <strong>exterior</strong> + ruta digital (perros OK)</li>
<li><strong>Mina bajo tierra:</strong> solo si museo confirma perros — si no, <span class="tag-dog-no">cancelada</span></li>
<li>Reserva: <a href="https://www.museomineroescucha.es/">museomineroescucha.es</a> · 978 756 705</li></ol>""",
        3, "<p>No dejar perras en furgoneta para visita mina.</p>",
    ))

    parts.append(day_card(
        "d4", "Día 4 · Martes 18", "Escucha → Morella · ~130 km · ~2 h",
        f"""<p>Traslado ~2 h (límite). Salida temprano.</p>
{btns([("Google · Escucha → Morella", gmaps_dir(*ESC, *MOR), "g")])}""",
        (
            spot("Parking N-232 mirador castillo", 40.621, -0.095,
                 "Vistas castillo, sin salida, ancho para AC 7 m.", "Agosto: turistas día")
            + spot("Camí vell acceso sur", 40.615, -0.105,
                   "Zona más tranquila que CCP oficial.", "Comprobar cartel pernocta")
        ),
        """<ul><li><a href="https://park4night.com/es/place/6766">P4N #6766</a> CCP Morella (suele lleno)</li></ul>""",
        [("Murallas Morella", "0,5", "5", "OK exterior", gmaps_pin(40.619, -0.100)),
         ("Castillo (exterior)", "0,6", "5", "OK mirador", gmaps_pin(40.620, -0.098)),
         ("Ports Vilafranca", "25", "35", "OK senda", gmaps_pin(40.83, -0.18))],
        """<ol><li>Atardecer murallas / castillo (exterior, perros)</li>
<li>Gastro: flaó, llonganissa, truita de patata</li></ol>""",
        4, "<p>Interior Castellón — mejor ventana hike mié–jue.</p>",
    ))

    parts.append(day_card(
        "d5", "Día 5 · Miércoles 19", "Morella · Ports de Morella",
        "<p><strong>Día estrella senderismo.</strong> Sin traslado.</p>",
        spot("Misma base D4", 40.621, -0.095, "Repetir parking N-232 si funcionó.", ""),
        """<ul><li>#6766 CCP</li><li>Camping Sant Cristòfol (emergencia)</li></ul>""",
        [("Ports de Morella", "15", "20", "OK bosque", gmaps_pin(40.75, -0.15)),
         ("Vilafranca", "20", "25", "OK", gmaps_pin(40.83, -0.18)),
         ("Parrizal Beceite", "—", "—", "Cancelar si ban", "")],
        f"""<ol><li><strong>7:00–12:00 · Ports / Vilafranca</strong> (sombra bosque)</li>
<li>Evitar <strong>Parrizal</strong> si perros prohibidos — alternativa senda forestal</li></ol>
{btns([("Turismo Morella", "https://www.morella.net/", "w"), ("Ports senderismo", gmaps_pin(40.75, -0.15), "g")])}""",
        5, "<p>Sensación cómoda todo el día vs costa.</p>",
    ))

    parts.append(day_card(
        "d6", "Día 6 · Jueves 20", "Morella · segundo día Ports o pueblo",
        "<p>Sin traslado. Lluvia posible (~3 mm) — bosque OK.</p>",
        spot("Base Morella (D4/D5)", 40.621, -0.095, "Misma pernocta.", ""),
        """<ul><li>#6766 · Camping emergencia</li></ul>""",
        [("Ruta circular Ports", "18", "25", "OK", gmaps_pin(40.76, -0.16)),
         ("Morella casco AM", "0", "3", "OK", gmaps_pin(40.619, -0.100))],
        """<ol><li>Segundo día Ports (ruta distinta) o pueblo si lluvia</li>
<li>Gastro: restaurante mesón (reserva)</li></ol>""",
        6, "<p>Plan B lluvia: casco + museo (confirmar perros).</p>",
    ))

    parts.append(day_card(
        "d7", "Día 7 · Viernes 21", "Morella → Sierra Espadán (Veo) · ~80 km · ~1,5 h",
        f"""<p>Traslado ≤2 h hacia Castellón interior montañoso.</p>
{btns([("Google · Morella → Alcudia de Veo", gmaps_dir(*MOR, *VEO), "g")])}""",
        (
            spot("Parking Camí vell Veo", 39.948, -0.278,
                 "Acceso senderos Espadán, aparcamiento día — comprobar pernocta cartel PN.",
                 "PN: pernocta libre prohibida — discreción")
            + spot("Aín aparcamiento pueblo", 39.915, -0.265,
                   "Alternativa más tranquila que Veo.", "Acceso estrecho")
        ),
        """<ul><li><a href="https://www.campingaltomira.com/">Camping Altomira</a> (legal, sombra)</li></ul>""",
        [("Camí vell Veo–Aín", "0", "5", "OK atado", gmaps_pin(39.948, -0.278)),
         ("Castillo Espadán", "12", "20", "OK", gmaps_pin(39.93, -0.29))],
        """<ol><li><strong>AM día 8:</strong> Camí vell Veo–Aín (11 km, sombra pinar)</li>
<li>Llegada tarde: reconocimiento parking</li></ol>""",
        7, "<p>Parque Natural: perros atados. No acampar (toldo/mesas).</p>",
    ))

    parts.append(day_card(
        "d8", "Día 8 · Sábado 22", "Sierra Espadán",
        "<p>Local. Calor subiendo (AppMax ~34) — solo mañana.</p>",
        spot("Base Veo/Aín", 39.948, -0.278, "Misma noche.", "Calor mediodía"),
        """<ul><li>Camping Altomira</li></ul>""",
        [("Circular Veo–Aín", "11", "15", "OK", gmaps_pin(39.948, -0.278)),
         ("Fuentes sombra Basseta", "8", "12", "OK", gmaps_pin(39.94, -0.27))],
        """<ol><li>7:00–11:00 hike Espadán</li><li>Tarde: siesta / mover hacia vuelta mañana</li></ol>""",
        8, "<p>Evitar costa y valles bajos.</p>",
    ))

    parts.append(day_card(
        "d9", "Día 9 · Domingo 23", "Hacia Catalunya · tramo ≤2 h",
        f"""<p>Acercamiento a Teià en saltos ≤2 h. Objetivo: ~2 h conducción max.</p>
{btns([("Ejemplo · Veo → Montanejos", gmaps_dir(-0.280, 39.950, -0.517, 40.067), "g")])}""",
        (
            spot("Montanejos / Embalse Arenoso borde", 40.058, -0.524,
                 "Zona termal/río, parkings amplios — satélite: sin salida lejos del pueblo.",
                 "Domingo: más gente día")
            + spot("Segorbe / entorno", 39.852, -0.489,
                   "Plan B más hacia sur.", "")
        ),
        """<ul><li>Camping zona Castellón interior si hace falta</li></ul>""",
        [("Chorreras Montanejos", "2", "5", "OK paseo", gmaps_pin(40.067, -0.517))],
        """<ol><li>Paseo corto AM si fresco</li><li>Resto: conducción hacia casa</li></ol>""",
        9, "<p>Día puente. Prioridad llegar bien para salida lun 24.</p>",
    ))

    parts.append(day_card(
        "d10", "Día 10 · Lunes 24", "→ Teià · ~4–5 h",
        f"""<p><strong>Tramo largo permitido</strong> (vuelta a casa).</p>
{btns([("Google · Montanejos → Teià", gmaps_dir(-0.517, 40.067, *TEIA), "g"),
       ("Google · Veo → Teià", gmaps_dir(*VEO, *TEIA), "g")])}""",
        "<p><strong>Llegada a casa.</strong> Sin pernocta en ruta.</p>",
        "<p>—</p>",
        [],
        "<p>Solo conducción. Paradas sombra cada 2 h para perras.</p>",
        10, "<p>Costa caliente — no hike. AC en marcha.</p>",
    ))

    return "".join(parts)


def live_summary() -> str:
    return """
<section class="section live-plan" id="plan-rapido">
<h2>Plan activo · 15–24 agosto 2026</h2>
<div class="card prose">
<div class="warn"><strong>Reglas:</strong> Teià loop · tramos ≤2 h (solo D1 y D10 ~5 h) · perras en todas las visitas · hike si sensación &lt;25°C · dormir vía <strong>Google Maps</strong> (P4N = emergencia).</div>
<div class="callout"><strong>Eje:</strong> Albarracín → Escucha (minas) → Morella/Ports → Sierra Espadán → Teià. <em>Navarra/Irati excluido</em> (incompatible con regla 2 h).</div>
<ol>
<li><strong>15–16</strong> Albarracín / Rodeno</li>
<li><strong>17</strong> Escucha patrimonio minero</li>
<li><strong>18–20</strong> Morella / Ports (días estrella)</li>
<li><strong>21–22</strong> Sierra Espadán</li>
<li><strong>23–24</strong> vuelta Teià</li>
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
    return """
<section class="section" id="perras"><h2>Reglas del viaje</h2>
<div class="card prose">
<div class="warn"><strong>Perras:</strong> solo actividades donde entren con vosotros. Visita sin perros = <strong>cancelada</strong>.</div>
<div class="warn"><strong>Calor:</strong> hike solo sensación &lt;25°C (Open-Meteo). Tip. 7:00–11:00.</div>
<ul>
<li>Sunlight 600 (&gt;2,10 m)</li>
<li>Conducción ≤2 h entre bases · D1 y D10 hasta ~5 h</li>
<li>POI ≤15 min coche desde pernocta</li>
<li>Descartados: Peñíscola/costa, Valderrobres valle, Parrizal si ban perros</li>
</ul>
</div></section>"""


def day_nav() -> str:
    links = "".join(f'<a href="#d{i}">D{i}</a>' for i in range(1, 11))
    return f'<nav class="day-nav wrap">{links}</nav>'


def render_spain_guide() -> str:
    ruta_gmaps = gmaps_dir(*TEIA, *ALB)  # simplified; full loop manual
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Guía camper · Interior ES · 15–24 ago 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap top-in">
<div class="brand">Guía camper · Interior España<small>15–24 agosto 2026 · Teruel · Cuencas Mineras · Castellón · Sunlight 600 + 2 perras</small></div>
<div class="btns">
<a class="btn btn-p" href="#plan-rapido">Plan 15–24</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#dormir-gmaps">Dormir GMaps</a>
</div></div></header>
{day_nav()}
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Sensación &lt;25°C</span><span class="chip">GMaps first</span><span class="chip">≤2 h tramos</span><span class="chip">Minas · gastro · Ports</span><span class="chip">Perras siempre</span></div>
<h1>Albarracín · Escucha · Morella · Espadán</h1>
<p class="lead">Loop fresco interior: minas de carbón, pinares de rodeno, Ports de Morella y Sierra Espadán. Cada día con la misma estructura: ruta, dormir, campings, distancias, visitas, meteo.</p>
{btns([("Google · inicio Teià → Albarracín", gmaps_dir(*TEIA, *ALB), "g")])}
</section>
{live_summary()}
{gmaps_howto()}
{rules_section()}
<section class="section" id="dias"><h2>Día a día</h2>
{build_days()}
</section>
<details class="archive wrap"><summary>Viaje anterior · Francia 6–19 ago (archivo)</summary>
<p class="card">La guía Francia está en el historial git del repo (<code>build_guia.py</code> rama anterior). Este viaje reemplaza el plan activo.</p>
</details>
<footer class="foot">
<p><strong>Guía camper interior ES</strong> · 15–24 agosto 2026 · Open-Meteo · Google Maps</p>
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
