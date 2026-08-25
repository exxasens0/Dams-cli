"""Guía escapada Berguedà / Pedraforca · jue 27 – sáb 29 ago 2026 · camper + perros."""
from __future__ import annotations

import json
from pathlib import Path

from es_1524_content import (
    CSS,
    TEIA,
    btn,
    btns,
    crowd_span,
    dif_badge,
    esc,
    fmt_date,
    gmaps_dir,
    gmaps_pin,
    gmaps_route,
)

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_bergueda.json").read_text())

# Coordenadas (lon, lat) salvo parking_lat/lon en dicts (lat, lon)
BAGA = (1.865, 42.086)
SALDES = (1.670, 42.230)  # wecamp Pedraforca
MIRADOR_GRESOLET = (1.701, 42.238)
GOSOL = (1.655, 42.255)
CAL_CERDANYOLA = (1.815, 42.268)

WECAMP = "https://wecamp.net/destinos/pedraforca"
MIRADOR_CAMP = "https://miradoralpedraforca.cat/"
WIKILOC_EMPEDRATS = (
    "https://ca.wikiloc.com/rutes-senderisme/"
    "cal-cerdanyolaaula-de-natura-la-salle-bullidor-de-la-llet-els-empedrats-"
    "refugi-sant-jordi-circular-9685192"
)
WIKILOC_CUA = (
    "https://ca.wikiloc.com/rutes-senderisme/"
    "salt-de-la-cua-de-cavall-baga-empedrats-15344646"
)

GMAPS_LOOP = gmaps_route([TEIA, BAGA, SALDES, CAL_CERDANYOLA, MIRADOR_GRESOLET, TEIA])

DAYS = [
    dict(
        day=1,
        date="2026-08-27",
        zona="Teià → Bagà → Saldes (Pedraforca)",
        parking_name="wecamp Pedraforca · B-400 km 13,5 · Saldes",
        parking_lat=42.230,
        parking_lon=1.670,
        camping_url=WECAMP,
        camping_alt=("Mirador al Pedraforca (alternativa)", MIRADOR_CAMP),
        drive_from="Teià → Bagà → Saldes",
        drive_km="~145 km",
        drive_h="~2 h",
        hike="Bagà casco medieval (paseo PM)",
        hike_lat=42.086,
        hike_lon=1.865,
        hike_km="~2 km",
        hike_dif="Fácil",
        hike_desn="~50 m",
        hike_h="45 min",
        hike_parking="Aparcar en Bagà y caminar por el casco",
        wikiloc_url="",
        concurrencia="Media",
        interes=[
            "Portal del Regomir (s. XIII)",
            "Plaça Porxada",
            "Muralla y torre",
            "Museo Càmara Obscura (opcional)",
        ],
        historia=(
            "Bagà fue capital del antiguo <strong>Berga de Bagà</strong>, señorío "
            "de los Cabrera. El casco medieval conserva la muralla, el portal "
            "del Regomir y la plaza porticada. Desde aquí partían las masoverías "
            "hacia el Cadí-Moixeró y las rutas de contrabando hacia la Cerdanya."
        ),
        observaciones=(
            "🚐 Salid de Teià ~10:00–11:00 para llegar a mediodía. "
            "Parada en Bagà 1–1,5 h (comer + paseo con perros por el casco). "
            "Subid a <strong>Saldes</strong> (~25 min) para pernoctar más fresco "
            "(~1.200 m vs ~770 m en Bagà). "
            "🐾 <strong>wecamp Pedraforca</strong>: perros admitidos (suplemento posible). "
            "Alternativa pequeña: <strong>Mirador al Pedraforca</strong> — solo ~9 parcelas camper, "
            "reservar con antelación. "
            "⚠️ Comprobad nivelación de parcela al llegar (como en El Arrebol: exigir cambio si no es habitable)."
        ),
        planb="Si lluvia: quedaros en el camping (piscina/spa wecamp) o museo de Bagà.",
    ),
    dict(
        day=2,
        date="2026-08-28",
        zona="Camí dels Empedrats · Salt de la Cua de Cavall ⭐",
        parking_name="wecamp Pedraforca (misma noche)",
        parking_lat=42.230,
        parking_lon=1.670,
        camping_url=WECAMP,
        drive_from="Saldes → Cal Cerdanyola (trailhead)",
        drive_km="~18 km",
        drive_h="~25 min",
        hike="Empedrats + Salt de la Cua de Cavall (PR-C 125)",
        hike_lat=42.268,
        hike_lon=1.815,
        hike_km="~8,5 km i/v",
        hike_dif="Moderado",
        hike_desn="~350 m",
        hike_h="3–3,5 h",
        hike_parking="Cal Cerdanyola / Aula de Natura La Salle — pista desde Bagà→Gisclareny",
        wikiloc_url=WIKILOC_CUA,
        concurrencia="Media",
        interes=[
            "Bullidor de la Llet (cascada)",
            "Gorges dels Empedrats",
            "Salt de la Cua de Cavall",
            "Paredes de conglomerado",
        ],
        historia=(
            "El <strong>Camí dels Empedrats</strong> era la ruta histórica entre "
            "Bagà y la Cerdanya, cruzando el río a pie en tramos de roca "
            "(«empedrats»). El Bullidor de la Llet y la Cua de Cavall son saltos "
            "de agua en el Parque Natural del Cadí-Moixeró."
        ),
        observaciones=(
            "⏰ Salida <strong>7:00–7:30</strong> — volver ~12:00–13:00 antes de calor/tormenta. "
            "Acceso: Bagà → Gisclareny → antes del pont de Sant Joan, pista a la derecha "
            "hacia Cal Cerdanyola (Aula de Natura La Salle). Parking en la casa de colonias. "
            "Tras cruzar el pont sobre el riu dels Empedrats, PR-C 125 (marques blanc/groc). "
            "Cruces de río sobre piedras — las perras se mojan; llevar toalla. "
            "🐾 Perros con <strong>correa</strong> en parque natural; sueltos solo donde no haya ganado. "
            "PM libre: piscina wecamp o pozas del río Saldes (cerca del camping)."
        ),
        planb=(
            "Lluvia/tormenta: ruta corta por Bagà o visita a la mina de Cercs / "
            "Museu de la Ciència y de la Tècnica de Catalunya (cerca de Manresa, ~45 min)."
        ),
    ),
    dict(
        day=3,
        date="2026-08-29",
        zona="Mirador de Gresolet · vuelta Teià",
        parking_name="Salida wecamp → Teià",
        parking_lat=41.498,
        parking_lon=2.319,
        drive_from="Saldes → Gresolet → Teià",
        drive_km="~145 km",
        drive_h="~2 h + parada",
        hike="Mirador de Gresolet (Pedraforca)",
        hike_lat=42.238,
        hike_lon=1.701,
        hike_km="~1 km i/v",
        hike_dif="Fácil",
        hike_desn="~80 m",
        hike_h="30–40 min",
        hike_parking="Parking Mirador de Gresolet (B-400, junto a Saldes/Gósol)",
        wikiloc_url="",
        concurrencia="Media-alta",
        interes=[
            "Vista clásica del Pedraforca (Enamorats + Pollegó)",
            "Gósol pueblo (opcional, 10 min)",
            "Compra quesos/embutidos Berguedà",
        ],
        historia=(
            "El <strong>Pedraforca</strong> (2.506 m) es el emblema del Berguedà: "
            "dos cimas (Enamorats y Pollegó Superior) unidas por un collado en forma de «forca». "
            "El mirador de Gresolet ofrece la postal más fotografiada sin subir a alta montaña."
        ),
        observaciones=(
            "⏰ Mirador ~8:00–9:00 (parking se llena en agosto). "
            "Paseo corto, ideal con perros. Opcional: parada en <strong>Gósol</strong> "
            "(pueblo de Picasso) 15 min. "
            "Vuelta directa a Teià ~2 h por C-16 / C-58. "
            "Parada sombra cada ~90 min si hace calor en el Llobregat."
        ),
        planb="Si niebla en Gresolet: ir directo a Teià; parada en Manresa o Montserrat (solo mirador desde abajo).",
    ),
]


def weather_block(day_num: int) -> str:
    w = next((d for d in WEATHER["days"] if d["day"] == day_num), None)
    if not w:
        return "<p>—</p>"
    tips = "".join(f"<li>{esc(t)}</li>" for t in w.get("tips", []))
    cls = "wx-ok" if w["app_max"] <= 25 else "wx-warn"
    return f"""<div class="wx-grid">
<div><em>Zona</em><strong style="font-size:.78rem">{esc(w.get("place_label") or w["place"])}</strong></div>
<div><em>Temp día</em><strong>{w["t_min"]:.0f}–{w["t_max"]:.0f}°C</strong></div>
<div><em>Sensación máx</em><strong class="{cls}">{w["app_max"]:.0f}°C</strong></div>
<div><em>Lluvia</em><strong>{w["precip_mm"]:.1f} mm · {w["precip_prob"]:.0f}%</strong></div>
</div><ul style="margin:.4rem 0;padding-left:1.2rem;font-size:.83rem">{tips}</ul>
<p style="font-size:.72rem;color:var(--muted);margin:.3rem 0 0">Open-Meteo · {esc(WEATHER["fetched_at"][:10])} · confirmar a las 7:00</p>"""


def _drive_url(d: dict) -> str:
    n = d["day"]
    if n == 1:
        return gmaps_route([TEIA, BAGA, SALDES])
    if n == 2:
        return gmaps_dir(*SALDES, *CAL_CERDANYOLA)
    if n == 3:
        return gmaps_route([SALDES, MIRADOR_GRESOLET, TEIA])
    return gmaps_pin(d["parking_lat"], d["parking_lon"])


def summary_table() -> str:
    wx = {d["day"]: d for d in WEATHER["days"]}
    cards = []
    for d in DAYS:
        n = d["day"]
        w = wx.get(n)
        wx_html = "—"
        if w:
            cls = "wx-ok" if w["app_max"] <= 25 else "wx-warn"
            wx_html = (
                f'<span class="{cls}">{w["app_max"]:.0f}°C</span> · '
                f'{w["precip_mm"]:.0f} mm ({w["precip_prob"]:.0f}%)'
            )
        star = " ⭐" if n == 2 else ""
        hike_html = (
            f'{esc(d["hike"])} · {dif_badge(d["hike_dif"])} · '
            f'{esc(d["hike_km"])} · {esc(d["hike_h"])}'
        )
        camp_btns = [("Web camping", d["camping_url"], "o")] if d.get("camping_url") else []
        if d.get("camping_alt"):
            label, url = d["camping_alt"]
            camp_btns.append((label, url, "o"))
        cards.append(f"""<article class="sum-card" id="e{n}">
<div class="k"><a href="#d{n}">E{n}{star}</a></div>
<h3>{fmt_date(d["date"])} · {esc(d["zona"])}</h3>
<div class="row"><b>Km</b><span>{esc(d["drive_km"])} · {esc(d["drive_h"])}</span></div>
<div class="row"><b>Pernocta</b><span>{esc(d["parking_name"])}</span></div>
<div class="row"><b>Ruta</b><span>{hike_html}</span></div>
<div class="row"><b>Gente</b><span>{crowd_span(d["concurrencia"])}</span></div>
<div class="row"><b>Clima</b><span>{wx_html}</span></div>
{btns([("Conducir", _drive_url(d), "g"), ("Detalle", f"#d{n}", "p")] + camp_btns)}
</article>""")
    return f"""
<p>{btns([("🗺️ Loop escapada", GMAPS_LOOP, "g"), ("Teià → Saldes", gmaps_route([TEIA, BAGA, SALDES]), "g")])}</p>
{"".join(cards)}
<p style="font-size:.75rem;color:var(--muted)">Open-Meteo {esc(WEATHER["fetched_at"][:10])} · ⭐ E2 día estrella (Empedrats).</p>
"""


def day_card(d: dict) -> str:
    n = d["day"]
    tit = f"E{n} · {fmt_date(d['date'])} · {d['zona']}"
    sub = f"{d['drive_from']} · {d['drive_km']}"

    if n == 1:
        ruta_html = (
            "<p>Salida desde <strong>Teià</strong> (~145 km · ~2 h). "
            "Parada en <strong>Bagà</strong> (comer + casco medieval). "
            "Subida a <strong>Saldes</strong> para pernoctar en el camping.</p>"
            + btns([
                ("Teià → Bagà", gmaps_dir(*TEIA, *BAGA), "g"),
                ("Bagà → wecamp Saldes", gmaps_dir(*BAGA, *SALDES), "g"),
            ])
        )
    elif n == 2:
        ruta_html = (
            "<p>🥾 Día estrella: <strong>Empedrats + Cua de Cavall</strong> desde Cal Cerdanyola. "
            "Salida temprano desde el camping (~25 min en coche).</p>"
            + btns([
                ("Saldes → Cal Cerdanyola", gmaps_dir(*SALDES, *CAL_CERDANYOLA), "g"),
                ("Wikiloc · Cua de Cavall", WIKILOC_CUA, "o"),
                ("Wikiloc · circular Empedrats", WIKILOC_EMPEDRATS, "o"),
            ])
        )
    else:
        ruta_html = (
            "<p>Mañana: <strong>Mirador de Gresolet</strong> (postal del Pedraforca). "
            "Vuelta directa a Teià (~2 h).</p>"
            + btns([
                ("Saldes → Mirador Gresolet", gmaps_dir(*SALDES, *MIRADOR_GRESOLET), "g"),
                ("Gresolet → Teià", gmaps_dir(*MIRADOR_GRESOLET, *TEIA), "g"),
                ("Parada Gósol", gmaps_dir(*MIRADOR_GRESOLET, *GOSOL), "g"),
            ])
        )

    camp_badge = (
        '<span style="background:#d4edda;color:#155724;font-size:.72rem;font-weight:700;'
        'padding:.2rem .5rem;border-radius:999px">🐾 wecamp Pedraforca · perros OK</span>'
    )
    alt_camp = ""
    if d.get("camping_alt"):
        label, url = d["camping_alt"]
        alt_camp = (
            f'<p style="font-size:.82rem;margin:.35rem 0">Alternativa: '
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a> '
            f"(~9 parcelas camper, reservar ya).</p>"
        )
    parking_html = f"""<div class="spot"><strong>{esc(d["parking_name"])}</strong>
{camp_badge}
{alt_camp}
{btns([("Conducir al camping", gmaps_pin(d["parking_lat"], d["parking_lon"]), "g")]
      + ([("Reservar wecamp", d["camping_url"], "o")] if d.get("camping_url") else []))}</div>"""

    hlat = d.get("hike_lat") or d["parking_lat"]
    hlon = d.get("hike_lon") or d["parking_lon"]
    wl_btn = (
        f'\n{btn("📍 Wikiloc", d["wikiloc_url"], "o")}' if d.get("wikiloc_url") else ""
    )
    hike_html = f"""<p><strong>{esc(d["hike"])}</strong> · {dif_badge(d["hike_dif"])} · \
{esc(d["hike_km"])} · {esc(d["hike_desn"])} desnivel · {esc(d["hike_h"])}</p>
<em style="font-size:.8rem;color:var(--muted)">{esc(d.get("hike_parking", ""))}</em>
{btns([("🗺️ Navegar al trailhead", gmaps_pin(hlat, hlon), "g")])}{wl_btn}"""

    poi_html = ", ".join(f"<strong>{esc(p)}</strong>" for p in d["interes"])
    hist_html = f"<p>{d['historia']}</p>" if d["historia"] else ""
    obs_html = f"<p>{d['observaciones']}</p>" if d["observaciones"] else ""
    planb_html = (
        f"<p><strong>Plan B:</strong> {esc(d['planb'])}</p>"
        if d.get("planb") and d["planb"] != "—"
        else ""
    )

    return f"""<article class="day-card" id="d{n}">
<div class="day-card-head"><h3>{esc(tit)}</h3><div class="sub">{esc(sub)}</div></div>
<section class="day-sec ruta"><h4>🚐 Ruta del día</h4>{ruta_html}</section>
<section class="day-sec parking"><h4>🅿️ Parking · pernocta</h4>{parking_html}</section>
<section class="day-sec hike"><h4>🥾 Excursión del día</h4>{hike_html}<p style="font-size:.82rem;color:var(--muted)">Interés: {poi_html}</p></section>
{f'<section class="day-sec historia"><h4>🏛️ Historia y contexto</h4>{hist_html}</section>' if hist_html else ""}
<section class="day-sec obs"><h4>👥 Observaciones</h4>{obs_html}<p>Concurrencia: {crowd_span(d["concurrencia"])}</p></section>
<section class="day-sec meteo"><h4>🌡️ Meteo del día</h4>{weather_block(n)}</section>
{f'<section class="day-sec planb"><h4>🌧️ Plan B</h4>{planb_html}</section>' if planb_html else ""}
</article>"""


def render() -> str:
    days_html = "".join(day_card(d) for d in DAYS)
    day_nav = "".join(f'<a href="#d{i}">E{i}</a>' for i in range(1, 4))
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Escapada Berguedà · Pedraforca · 27–29 ago 2026</title>
<style>{CSS}</style>
</head><body>
<div class="chrome"><div class="wrap">
<header class="top-in">
<div class="brand">Berguedà · Pedraforca<small>27–29 ago · camper + 2 perras · Teià</small></div>
<div class="btns">
<a class="btn btn-p" href="#resumen">Resumen</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#campings">Campings</a>
</div>
</header>
<nav class="day-nav">{day_nav}</nav>
</div></div>
<main class="wrap">
<section class="hero">
<div class="chips">
<span class="chip">Jue 27 llegada</span>
<span class="chip">Vie 28 Empedrats ⭐</span>
<span class="chip">Sáb 29 Gresolet</span>
<span class="chip">≤25°C</span>
</div>
<h1>Berguedà · Pedraforca</h1>
<p class="lead">Escapada 2 noches desde Teià. Frescura de prepirineo (~24°C), ruta estrella Empedrats + Cua de Cavall, postal del Pedraforca en Gresolet. Camper + perros.</p>
{btns([("🗺️ Loop completo", GMAPS_LOOP, "g"), ("Reservar wecamp", WECAMP, "o")])}
</section>

<section class="section" id="resumen">
<h2>Resumen · 3 días</h2>
{summary_table()}
</section>

<section class="section" id="campings">
<h2>🅿️ Pernocta camper (reservar)</h2>
<div class="card">
<h3 style="margin-top:0;color:var(--pine)">wecamp Pedraforca · Saldes</h3>
<p style="font-size:.88rem">B-400 km 13,5 · parcelas con electricidad · piscina · perros admitidos. ~200 plazas pero reservar en agosto.</p>
{btns([("Reservar wecamp", WECAMP, "o"), ("Conducir", gmaps_pin(42.230, 1.670), "g")])}
</div>
<div class="card">
<h3 style="margin-top:0;color:var(--pine)">Mirador al Pedraforca · Saldes (alternativa)</h3>
<p style="font-size:.88rem">Camping pequeño (~9 parcelas camper) · pet-friendly · vistas al Pedraforca. Reservar imprescindible.</p>
{btns([("Web camping", MIRADOR_CAMP, "o"), ("Conducir", gmaps_dir(*BAGA, 1.625, 42.225), "g")])}
</div>
<div class="warn">⚠️ Al hacer check-in, comprobad <strong>nivelación y sombra</strong> de la parcela antes de pagar extras. Exigir cambio si no es habitable.</div>
</section>

<section class="section" id="dias"><h2>Día a día</h2>
{days_html}
</section>

<section class="section" id="reglas">
<h2>Reglas del viaje</h2>
<div class="card">
<div class="warn"><strong>Perras:</strong> correa en Parque Natural Cadí-Moixeró; sueltos solo sin ganado.</div>
<ul style="font-size:.9rem;padding-left:1.3rem">
<li>Hikes 7:00–13:00 — tarde libre o piscina</li>
<li>Patous / rebaños: correa obligatoria</li>
<li>Empedrats: cruces de río — calzado que se pueda mojar</li>
</ul>
</div>
</section>

<footer class="foot wrap">
<p><strong>Escapada Berguedà · Pedraforca</strong> · 27–29 agosto 2026 · Open-Meteo</p>
<p>Guía principal Pirineo: <code>guia-movil.html</code></p>
</footer>
</main>
<div class="fab">
<a class="btn btn-p" href="#resumen">Resumen</a>
<a class="btn" href="#d2">E2 ⭐</a>
</div>
</body></html>"""


def main() -> None:
    html_out = render()
    out = ROOT / "guia-bergueda.html"
    out.write_text(html_out, encoding="utf-8")
    print("written", len(html_out), "bytes →", out.name)


if __name__ == "__main__":
    main()
