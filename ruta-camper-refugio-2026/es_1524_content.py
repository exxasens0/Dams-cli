"""Guía camper 16–26 ago 2026 · Dom16 noche→Canfranc · D1-3 Canfranc · D4 Oza · D5 Jaca+Nav · D6-9 Navarra · D10 Teià."""
from __future__ import annotations
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_es1524.json").read_text())

# ── Coordenadas clave ────────────────────────────────────────────────────────
TEIA   = (2.319,   41.498)
SPOT1  = (-0.51183, 42.80934)  # Canal Roya · primera noche (usuario)
CAN    = (-0.525,  42.750)   # Canfranc Estación (~11 km al sur del spot)
OZA    = (-0.717,  42.822)   # Selva de Oza parking
ZUR    = (-0.832,  42.860)   # Zuriza
OCH    = (-1.079,  42.906)   # Ochagavía
ISA    = (-0.921,  42.856)   # Isaba
JACA   = (-0.549,  42.568)
YESA   = (-1.072,  42.622)   # Embalse de Yesa

WEEKDAYS = {0:"lunes",1:"martes",2:"miércoles",3:"jueves",4:"viernes",5:"sábado",6:"domingo"}
def weekday(d:str)->str:
    from datetime import date as dt; y,m,d2=map(int,d.split("-")); return WEEKDAYS[dt(y,m,d2).weekday()]
def fmt_date(d:str)->str: return f"{weekday(d)} {int(d.split('-')[2])} ago"

def esc(s:str)->str: return html.escape(s or "",quote=True)
def gmaps_dir(olon,olat,dlon,dlat)->str:
    return f"https://www.google.com/maps/dir/?api=1&origin={olat},{olon}&destination={dlat},{dlon}&travelmode=driving"
def gmaps_route(stops)->str:
    if len(stops)<2: return ""
    olon,olat=stops[0]; dlon,dlat=stops[-1]
    url=f"https://www.google.com/maps/dir/?api=1&origin={olat},{olon}&destination={dlat},{dlon}"
    mid=stops[1:-1]
    if mid: url+="&waypoints="+"|".join(f"{lat},{lon}" for lon,lat in mid)
    return url+"&travelmode=driving"
def gmaps_pin(lat,lon)->str: return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
def p4n(lat,lon,dist=8)->str: return f"https://park4night.com/es/map#{14}/{lat}/{lon}"

GMAPS_LOOP = gmaps_route([TEIA, SPOT1, OZA, OCH, ISA, TEIA])

def btn(label,url,kind="g")->str:
    cls={"g":"btn btn-g","o":"btn btn-o","w":"btn btn-w","p":"btn btn-p"}.get(kind,"btn")
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'
def btns(items)->str:
    return '<div class="btns">'+"".join(btn(l,u,k) for l,u,k in items)+"</div>"

# ── Datos completos por día ──────────────────────────────────────────────────
DAYS = [
    # (day, date, zona_titulo, parking_name, parking_lat, parking_lon,
    #  p4n_url, camping_url, drive_from, drive_km, drive_h,
    #  hike_nombre, hike_km, hike_dif, hike_desnivel, hike_h,
    #  concurrencia, interes_tags, historia, observaciones, planb)
    dict(
        day=1, date="2026-08-17",
        zona="Canal Roya · Canfranc",
        parking_name="Canal Roya · spot primera noche",
        parking_lat=42.80934, parking_lon=-0.51183,
        drive_from="Dom 16 noche, Teià → Canal Roya", drive_km="~375 km", drive_h="4,5 h",
        hike="Ibón de Estanes", hike_km="12 km", hike_dif="Moderado",
        hike_desn="~400 m", hike_h="3–4 h",
        concurrencia="Media-alta",
        interes=["Estación Internacional de Canfranc","Valle del Aragón","Río Aragón"],
        historia=(
            "La <strong>Estación Internacional de Canfranc</strong> (1928) fue la más grande de España "
            "y segunda de Europa. Su apertura conectó España y Francia por el Pirineo central. "
            "Durante la II Guerra Mundial fue paso clandestino de judíos y se cree que por aquí "
            "salió arte expoliado por los nazis hacia España. En 1970 un accidente en el puente "
            "francés cortó el servicio; lleva décadas abandonada. Actualmente en rehabilitación "
            "como hotel de lujo. El edificio modernista es impresionante incluso desde fuera."
        ),
        observaciones=(
            "Llegáis con la noche del dom 16 · sin hike ese día. "
            "El parking Canal Roya tiene varios spots P4N junto al río Aragón (agua, sombra). "
            "Ibón de Estanes: sendero bien marcado, gana ~400 m · pozas con agua para perras. "
            "Perros atados en pastizales superiores (patous presentes agosto). "
            "Canfranc pueblo tiene pan, supermercado pequeño y gastro de borda aragonesa."
        ),
        planb="Visita exterior estación Canfranc · paseo por el pueblo · río Aragón.",
    ),
    dict(
        day=2, date="2026-08-18",
        zona="Canal Roya · Canfranc",
        parking_name="Canal Roya · misma zona",
        parking_lat=42.80934, parking_lon=-0.51183,
        drive_from="Sin traslado · misma zona Canal Roya", drive_km="—", drive_h="—",
        hike="Canal Roya – Laguna de Tortiellas", hike_km="10 km", hike_dif="Fácil-Moderado",
        hike_desn="~300 m", hike_h="3 h",
        concurrencia="Media",
        interes=["Canal Roya","Llanos de la Rinconada","Frontera Francia","GR-11"],
        historia=(
            "El <strong>Canal Roya</strong> es un valle glaciar que serpentea hacia la frontera "
            "francesa. Forma parte del <strong>GR-11</strong>, el sendero que cruza los Pirineos "
            "de Cabo Higuer (Hondarribia) al Cap de Creus (Cadaqués). El valle conserva glaciares "
            "rocosos y en días claros se ven los picos fronterizos. El nombre 'Canal' viene de los "
            "barrancos rectilíneos tallados por glaciares cuaternarios."
        ),
        observaciones=(
            "Mejor día del tramo aragonés: 0 mm, 24°C. Aprovechar para hike largo. "
            "El camino de Canal Roya es un carril forestal ancho al principio, perfecto para perros. "
            "Se puede aparcar en distintos puntos según cuánto se quiera caminar. "
            "Tarde: mover camper unos km para cambiar paisaje nocturno (borde Aragón o Astún)."
        ),
        planb="Paseo corto borde río Aragón · área picnic Canfranc.",
    ),
    dict(
        day=3, date="2026-08-19",
        zona="Candanchú · Astún · Canfranc",
        parking_name="Astún (parking estación)",
        parking_lat=42.795, parking_lon=-0.458,
        drive_from="Canal Roya → Canfranc Estación → Astún", drive_km="~20 km", drive_h="~30 min",
        hike="Lagunas de Anayet (ruta baja)", hike_km="9 km", hike_dif="Moderado",
        hike_desn="~350 m", hike_h="3 h",
        concurrencia="Media-alta (zona estación)",
        interes=["Lagunas de Anayet","Pics du Midi d'Ossau (vistas)","Refugio de Anayet","Frontera Francia"],
        historia=(
            "Las <strong>Lagunas de Anayet</strong> (1960–2227 m) son ibones glaciares con "
            "vistas directas al <strong>Pic du Midi d'Ossau</strong> (2884 m, Francia), "
            "uno de los montes más fotogénicos del Pirineo por su silueta volcánica. "
            "La zona fue zona de pastoreo trashúmante durante siglos; los pastores aragoneses "
            "subían con sus rebaños cada verano desde el Somontano. El refugio de Anayet "
            "(privado) sirve bocadillos en agosto."
        ),
        observaciones=(
            "0 mm, 25°C — último día seco antes de varios días con posible lluvia. "
            "Tomar el sendero bajo de Anayet (no la variante de crestas, que es técnica). "
            "Candanchú en agosto es un cruce de ciclistas y senderistas; aparcar en Astún "
            "suele ser más tranquilo. "
            "Tarde: preparar camper y bajar a Oza mañana (mover zona D4)."
        ),
        planb="Paseo llano Candanchú · vista exterior hacia frontera.",
    ),
    dict(
        day=4, date="2026-08-20",
        zona="Selva de Oza · Aguas Tuertas ⭐",
        parking_name="Área forestal Selva de Oza",
        parking_lat=42.822, parking_lon=-0.717,
        drive_from="Canal Roya / Astún → Oza (Valle de Hecho)", drive_km="~86 km", drive_h="~1h25",
        hike="Aguas Tuertas", hike_km="8 km", hike_dif="Fácil",
        hike_desn="~200 m", hike_h="2,5 h",
        concurrencia="Media",
        interes=["Aguas Tuertas","Río Aragón Subordán","Selva de Oza","Valle de Hecho","Siresa"],
        historia=(
            "<strong>Aguas Tuertas</strong> ('aguas torcidas') es una pradera alpina de origen "
            "glaciar a ~1640 m donde el río Aragón Subordán forma meandros imposibles en terreno "
            "llano, como si el río se hubiera olvidado de ir cuesta abajo. Es uno de los paisajes "
            "más singulares y fotogénicos del Pirineo, y sorprendentemente accesible. "
            "<strong>Selva de Oza</strong> es un hayedo-pinar de gran valor ecológico; el Valle de Hecho "
            "conserva el <strong>cheso</strong>, un dialecto aragonés con 1.500 hablantes, "
            "uno de los pocos vivos de Aragón. El pueblo de Hecho tiene un museo de escultura "
            "contemporánea al aire libre único en el Pirineo."
        ),
        observaciones=(
            "Jue 20 es el día más fresco de toda la semana aragonesa (21°C en Oza). "
            "Perros perfectos en Aguas Tuertas: terreno llano, agua en el río, poca gente. "
            "Aparcar en el área forestal de Oza (P4N varios spots, zona de acampada libre histórica "
            "ahora regulada). Tened los carteles en cuenta — zona ZEPA. "
            "Siresa (3 km de Oza): monasterio románico del s.IX, el más antiguo de Aragón, merece "
            "una parada de 20 min. Hecho pueblo (10 km) para avituallamiento."
        ),
        planb="Paseo borde río Aragón Subordán en Oza · fresco y sombreado.",
    ),
    dict(
        day=5, date="2026-08-21",
        zona="Ansó / Zuriza → Jaca → borde Navarra",
        parking_name="Embalse de Yesa (pernocta transición)",
        parking_lat=42.622, parking_lon=-1.072,
        drive_from="Oza → Jaca (~55 km) → Yesa (~45 km)", drive_km="~100 km", drive_h="~1h30",
        hike="Foz de Biniés (opcional AM temprano)", hike_km="4 km", hike_dif="Fácil",
        hike_desn="~80 m", hike_h="1,5 h",
        concurrencia="Alta Jaca agosto · tranquila Foz",
        interes=["Foz de Biniés","Ansó medieval","Jaca catedral románica","Ciudadela de Jaca","Embalse Yesa"],
        historia=(
            "<strong>Jaca</strong> (820 m) fue la primera capital del Reino de Aragón. Su "
            "<strong>catedral románica</strong> (1063) es la primera románica de España y modelo "
            "para las demás del Camino de Santiago. La <strong>Ciudadela</strong> (s.XVI) es una "
            "de las mejores fortalezas estrelladas de Europa, aún activa como cuartel. "
            "<strong>Ansó</strong> conserva el <strong>traje típico ansotano</strong>, uno de los "
            "trajes regionales más llamativos de España — las mujeres solteras llevaban la toca "
            "hacia adelante, las casadas hacia atrás. La aldea estuvo aislada durante siglos "
            "y desarrolló su propia cultura."
        ),
        observaciones=(
            "Día de lluvia (~16–21 mm) → ideal para conducción y cultura urbana. "
            "Foz de Biniés: si el tiempo lo permite a primera hora (gargantas kársticas, "
            "fácil, 1,5 h, perros OK). Jaca: visita catedral exterior + ciudadela desde fuera "
            "(perros no entran al museo pero sí paseo foso). "
            "Tarde: hacia embalse Yesa o ya Ochagavía si el tiempo mejora. "
            "Yesa tiene varios P4N en el borde del embalse — bonita pernocta de transición."
        ),
        planb="Jaca: catedral + ciudadela + mercado cubierto si llueve.",
    ),
    dict(
        day=6, date="2026-08-22",
        zona="Ochagavía · Valle de Salazar",
        parking_name="Borde Ochagavía (fuera casco)",
        parking_lat=42.908, parking_lon=-1.082,
        drive_from="Yesa → Ochagavía (~90 km)", drive_km="~90 km", drive_h="~1h15",
        hike="Acceso suave Selva de Irati · río Zatoia", hike_km="6 km", hike_dif="Fácil",
        hike_desn="~100 m", hike_h="2 h",
        concurrencia="Alta (sábado agosto)",
        interes=["Ochagavía casco medieval","Santuario de Muskilda","Río Zatoia","Puente medieval"],
        historia=(
            "<strong>Ochagavía</strong> es la capital del <strong>Valle de Salazar</strong>, "
            "uno de los valles pirenaicos navarros mejor conservados. Su casco medieval tiene "
            "el típico trazado de pueblo de montaña navarro: calles empedradas, casas de piedra "
            "con escudos, puente románico sobre el Zatoia. El <strong>Santuario de Muskilda</strong> "
            "(s.XIII, en el monte sobre el pueblo) es el más venerado del Pirineo navarro; "
            "cada 8 de septiembre los danzantes de Ochagavía bailan ante la Virgen con traje "
            "tradicional en una de las fiestas más antiguas de Navarra. "
            "La zona es la entrada al <strong>Queso Roncal DOP</strong>, el primer queso español "
            "con denominación de origen (1981)."
        ),
        observaciones=(
            "Llegar a primera hora para pillar parking fuera del casco (AC 7 m, callejuelas). "
            "P4N varios spots borde río y fuera del pueblo. "
            "Sábado agosto = alta concurrencia turística en el casco; los senderos están más tranquilos. "
            "Río Zatoia: agua limpia y fría, perfecto para perras. "
            "Avituallamiento: hay supermercado pequeño en Ochagavía. "
            "Gastronomía: cordero al chilindrón, queso Roncal, cuajada."
        ),
        planb="Casco medieval Ochagavía · tiendas de queso Roncal · paseo río.",
    ),
    dict(
        day=7, date="2026-08-23",
        zona="Selva de Irati · Embalse Irabia",
        parking_name="Área embalse Irabia / Casas de Irati",
        parking_lat=42.933, parking_lon=-1.032,
        drive_from="Ochagavía → Irabia (~15 km)", drive_km="~15 km", drive_h="~20 min",
        hike="Circular hayedo-abetal de Irati", hike_km="9 km", hike_dif="Fácil-Moderado",
        hike_desn="~250 m", hike_h="3 h",
        concurrencia="Alta (domingo) · se diluye en la selva",
        interes=["Selva de Irati","Embalse de Irabia","Hayedo-abetal","Casas de Irati","Abodi"],
        historia=(
            "La <strong>Selva de Irati</strong> es el segundo bosque caducifolio más grande de Europa, "
            "con 17.000 ha de hayedo-abetal compartidas entre Navarra y el País Vasco francés. "
            "Los hayas y abetos alcanzan los 35 m de altura; algunos ejemplares superan los 500 años. "
            "Históricamente fue zona de carboneo y extracción maderera para la Armada española "
            "(los barcos necesitaban los árboles rectos del Pirineo). "
            "El <strong>Embalse de Irabia</strong> (1942) es artificial pero perfectamente integrado "
            "en el paisaje. La selva alberga urogallos, corzos, jabalíes y, ocasionalmente, "
            "oso pardo (avistamientos raros pero documentados). "
            "En otoño el espectáculo cromático es de fama europea; en verano la sombra del hayedo "
            "es un refugio climático natural."
        ),
        observaciones=(
            "Mover camper a la zona Irabia — hay varios P4N remotos y el área de Casas de Irati "
            "tiene camping oficial. El acceso por pista forestal es ancho, sin problema para Sunlight. "
            "Domingo = turistas, pero entrad pronto (antes de 9h) y la selva se vacía. "
            "Perros con correa — zona sensible para aves (urogallo). "
            "Si llueve: el hayedo bajo lluvia es impresionante (niebla, setas en agosto-septiembre). "
            "Agua: río Irati nace aquí, cristalino y frío."
        ),
        planb="Parking Irabia + paseo borde embalse (sin hike, con lluvia igualmente bonito).",
    ),
    dict(
        day=8, date="2026-08-24",
        zona="Orbaitzeta · Río Irati interior",
        parking_name="Orbaitzeta / aguas arriba río",
        parking_lat=42.964, parking_lon=-1.217,
        drive_from="Irabia → Orbaitzeta (~20 km pista forestal)", drive_km="~20 km", drive_h="~30 min",
        hike="Senda Río Irati / Ruinas Orbaitzeta", hike_km="7 km", hike_dif="Fácil",
        hike_desn="~100 m", hike_h="2,5 h",
        concurrencia="Baja (lunes, zona remota)",
        interes=["Real Fábrica de Armas de Orbaitzeta","Río Irati","Bosque interior","Garralda"],
        historia=(
            "Las <strong>Ruinas de la Real Fábrica de Armas de Orbaitzeta</strong> son uno de los "
            "monumentos industriales más espectaculares y olvidados de España. "
            "Construida en 1784 por orden de Carlos III para fabricar cañones para la Armada, "
            "funcionó hasta 1874 cuando fue destruida durante las <strong>Guerras Carlistas</strong>. "
            "Las tres guerras civiles carlistas (1833–76) devastaron el Pirineo navarro: "
            "Navarra era el corazón del carlismo y estas montañas vieron combates brutales. "
            "Hoy las ruinas de sillería asoman entre el hayedo como una ciudad fantasma: "
            "edificios de 3 pisos cubiertos de hiedra, fraguas, canales hidráulicos. "
            "La visita es libre y gratuita; los perros pueden entrar."
        ),
        observaciones=(
            "⚠️ Día de mayor lluvia del viaje (~34 mm posibles). "
            "Plan A (seco): senda río Irati aguas arriba + ruinas Orbaitzeta. "
            "Plan B (lluvia): visita ruinas Orbaitzeta (bajo el hayedo, soporta bien lluvia) "
            "+ pueblo Garralda / Aribe para café. "
            "Zona muy remota y tranquila — baja concurrencia incluso en agosto. "
            "P4N: buscar spots borde río antes de Orbaitzeta. "
            "Mañana: mover a Isaba (~35 km)."
        ),
        planb="Ruinas Fábrica de Armas Orbaitzeta · bosque cubierto · pueblo Garralda.",
    ),
    dict(
        day=9, date="2026-08-25",
        zona="Isaba · Valle del Roncal",
        parking_name="Borde río Esca / Isaba",
        parking_lat=42.856, parking_lon=-0.921,
        drive_from="Orbaitzeta → Isaba (~35 km)", drive_km="~35 km", drive_h="~45 min",
        hike="Senda río Esca o acceso Belagua", hike_km="8 km", hike_dif="Fácil",
        hike_desn="~150 m", hike_h="2,5 h",
        concurrencia="Baja (martes)",
        interes=["Isaba","Circo de Belagua","Río Esca","Queso Roncal DOP","Tributo de las Tres Vacas"],
        historia=(
            "<strong>Isaba</strong> es el pueblo más importante del <strong>Valle del Roncal</strong>, "
            "famoso por su queso DOP y por una curiosidad histórica única en Europa: "
            "el <strong>Tributo de las Tres Vacas</strong>. Desde 1375 (¡cada año sin excepción!), "
            "el 13 de julio, Francia entrega tres vacas de raza pirenaica al Valle del Roncal "
            "como compensación por el uso de pastos del Pirineo. Es el único tributo que "
            "Francia paga a España. La ceremonia se celebra en el límite fronterizo de Pierre "
            "Saint-Martin. El <strong>Circo de Belagua</strong> es un anfiteatro glaciar imponente; "
            "el acceso desde Isaba sube a 1.400 m con vistas al Pico de Anie (2463 m, Francia)."
        ),
        observaciones=(
            "Último día en Navarra antes de la vuelta. Tranquilo martes. "
            "Senda del río Esca desde Isaba: plana, sombreada, perfecta para perras. "
            "Circo de Belagua: si el tiempo mejora, vale el desvío (14 km A/R, moderado). "
            "Isaba tiene queso Roncal en varias tiendas — ideal para llevar a casa. "
            "Pernocta: borde río Esca o P4N en los alrededores. "
            "Mañana D10: salida temprana a Teià (~435 km, ~5,5 h)."
        ),
        planb="Paseo pueblo Isaba · compras queso Roncal · río Esca.",
    ),
    dict(
        day=10, date="2026-08-26",
        zona="Vuelta a Teià",
        parking_name="Teià — casa",
        parking_lat=41.498, parking_lon=2.319,
        drive_from="Isaba → Teià (~435 km)", drive_km="~435 km", drive_h="5–6 h",
        hike="—", hike_km="—", hike_dif="—", hike_desn="—", hike_h="—",
        concurrencia="—",
        interes=["Parada sombra cada 2 h","AC para perras","Evitar parar sin sombra"],
        historia="",
        observaciones=(
            "Salir antes de las 8:00 para evitar el calor de costa. "
            "Costa mediterránea en agosto: sensación ~30°C+ — interior camper 35°C+ al sol. "
            "Paradas solo en áreas de servicio con sombra o gasolineras con zona arbolada. "
            "AC encendido para las perras. "
            "Ruta recomendada: Pamplona → Zaragoza → Lleida → Barcelona."
        ),
        planb="—",
    ),
]

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = r"""
:root{--bg:#f2eee4;--ink:#1a221c;--muted:#4d5c52;--card:#fffdf8;--pine:#1b4a3b;--clay:#9a5528;--line:#d7cdbc;--shadow:0 14px 32px rgba(26,34,28,.09);--sec:#e8efe9;--red:#a33;--gold:#7a5a00}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"Source Sans 3",system-ui,sans-serif;color:var(--ink);background:radial-gradient(900px 420px at 0% 0%,#dfe8df,transparent 55%),var(--bg);line-height:1.6}
.wrap{max-width:1000px;margin:0 auto;padding:0 1rem 4rem}
.top{position:sticky;top:0;z-index:50;background:rgba(242,238,228,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.5rem;padding:.5rem 0}
.brand{font-family:"Fraunces",serif;font-weight:700;color:var(--pine);font-size:1rem}
.brand small{display:block;font-family:"Source Sans 3",sans-serif;font-size:.68rem;font-weight:400;color:var(--muted)}
.btn{display:inline-block;padding:.4rem .7rem;border-radius:8px;font-size:.8rem;font-weight:600;text-decoration:none;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.btn-p{background:var(--pine);color:#fff;border-color:var(--pine)}.btn-g{background:#eef4ee}.btn-o{background:#fff3e6}.btn-w{background:#f5f0ff}
.btns{display:flex;flex-wrap:wrap;gap:.35rem;margin:.3rem 0}
.hero{padding:1.2rem 0 .8rem}.hero h1{font-family:"Fraunces",serif;font-size:clamp(1.5rem,4vw,2rem);margin:.3rem 0}
.lead{color:var(--muted);max-width:44rem}.chips{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.5rem}
.chip{font-size:.7rem;font-weight:700;background:var(--sec);color:var(--pine);padding:.2rem .5rem;border-radius:999px}
.section{margin:2rem 0}.section>h2{font-family:"Fraunces",serif;color:var(--pine);border-bottom:2px solid var(--clay);padding-bottom:.3rem;font-size:1.25rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.9rem 1rem;margin:.8rem 0;box-shadow:var(--shadow)}
.warn{background:#fff4e6;border-left:4px solid var(--clay);padding:.65rem .9rem;border-radius:8px;margin:.6rem 0}
.callout{background:var(--sec);padding:.65rem .9rem;border-radius:8px;margin:.6rem 0}
.day-nav{position:sticky;top:48px;z-index:40;display:grid;grid-template-columns:repeat(5,1fr);gap:.2rem;background:rgba(242,238,228,.97);padding:.4rem 0;margin:0 -1rem;padding-left:1rem;padding-right:1rem;backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
@media(min-width:600px){.day-nav{grid-template-columns:repeat(10,1fr)}}
.day-nav a{font-size:.65rem;text-align:center;padding:.3rem .15rem;border-radius:6px;text-decoration:none;color:var(--pine);font-weight:700;background:var(--card);border:1px solid var(--line)}
.day-nav a:hover{background:var(--sec)}
/* Summary table */
.summary-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0;border:1px solid var(--line);border-radius:14px;background:var(--card);box-shadow:var(--shadow)}
.summary-table{width:100%;border-collapse:collapse;font-size:.79rem;min-width:780px}
.summary-table thead th{background:var(--pine);color:#fff;padding:.5rem .6rem;text-align:left;font-size:.7rem;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.summary-table tbody td{padding:.5rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
.summary-table tbody tr:last-child td{border-bottom:0}
.summary-table tbody tr:hover td{background:#f4f9f5}
.summary-table a{color:var(--pine);font-weight:600;text-decoration:none}
.summary-table a:hover{text-decoration:underline}
.badge{display:inline-block;padding:.1rem .45rem;border-radius:999px;font-size:.68rem;font-weight:700;white-space:nowrap}
.dif-f{background:#d4edda;color:#155724}.dif-m{background:#fff3cd;color:#856404}.dif-a{background:#fde;color:var(--red)}
.crowd-b{color:#155724;font-weight:700}.crowd-m{color:#856404;font-weight:700}.crowd-a{color:var(--red);font-weight:700}
.wx-ok{color:var(--pine);font-weight:700}.wx-warn{color:var(--red);font-weight:700}
.star{color:var(--gold);font-weight:700}
/* Day cards */
.day-card{background:var(--card);border:1px solid var(--line);border-radius:18px;margin:2rem 0;overflow:hidden;box-shadow:var(--shadow)}
.day-card-head{background:linear-gradient(135deg,var(--pine),#2a6b55);color:#fff;padding:1rem 1.2rem}
.day-card-head h3{margin:0;font-family:"Fraunces",serif;font-size:1.1rem}
.day-card-head .sub{opacity:.9;font-size:.82rem;margin-top:.2rem}
.day-sec{padding:.8rem 1.1rem;border-top:1px solid var(--line)}
.day-sec h4{margin:0 0 .5rem;font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--clay)}
.day-sec.ruta{background:#f8faf8}.day-sec.parking{background:#f5f8f5}.day-sec.hike{background:#f0f8f0}
.day-sec.historia{background:#fffbf3}.day-sec.obs{background:#fafafa}.day-sec.meteo{background:#f0f6fa}.day-sec.planb{background:#fff8f0}
.spot{margin:.4rem 0;padding:.5rem .7rem;background:var(--sec);border-radius:8px;font-size:.88rem}
.spot strong{display:block;color:var(--pine);margin-bottom:.15rem}
.wx-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.4rem;font-size:.85rem}
@media(min-width:500px){.wx-grid{grid-template-columns:repeat(4,1fr)}}
.wx-grid>div{background:#e8f4fb;padding:.4rem .5rem;border-radius:6px}
.wx-grid em{display:block;font-size:.7rem;color:var(--muted);font-style:normal}
.wx-grid strong{display:block;font-size:.9rem}
.foot{padding:1.5rem 0;color:var(--muted);font-size:.82rem;border-top:1px solid var(--line)}
.fab{position:fixed;bottom:1rem;right:1rem;display:flex;gap:.35rem;z-index:60}
details.archive{margin:1.5rem 0}details.archive summary{cursor:pointer;font-weight:700;color:var(--muted)}
"""

# ── Helpers ──────────────────────────────────────────────────────────────────
def weather_block(day_num:int)->str:
    w = next((d for d in WEATHER["days"] if d["day"]==day_num), None)
    if not w: return "<p>—</p>"
    tips = "".join(f"<li>{esc(t)}</li>" for t in w.get("tips",[]))
    cls = "wx-ok" if w["app_max"]<=25 else "wx-warn"
    return f"""<div class="wx-grid">
<div><em>Zona</em><strong style="font-size:.78rem">{esc(w.get('place_label') or w['place'])}</strong></div>
<div><em>Temp día</em><strong>{w['t_min']:.0f}–{w['t_max']:.0f}°C</strong></div>
<div><em>Sensación máx</em><strong class="{cls}">{w['app_max']:.0f}°C</strong></div>
<div><em>Lluvia</em><strong>{w['precip_mm']:.1f} mm · {w['precip_prob']:.0f}%</strong></div>
</div><ul style="margin:.4rem 0;padding-left:1.2rem;font-size:.83rem">{tips}</ul>
<p style="font-size:.72rem;color:var(--muted);margin:.3rem 0 0">Open-Meteo · {esc(WEATHER['fetched_at'][:10])} · confirmar a las 7:00</p>"""

def dif_badge(dif:str)->str:
    m = {"Fácil":"dif-f","Moderado":"dif-m","Fácil-Moderado":"dif-f","Difícil":"dif-a"}
    cls = m.get(dif,"dif-m")
    return f'<span class="badge {cls}">{esc(dif)}</span>'

def crowd_span(c:str)->str:
    m = {"Baja":"crowd-b","Media":"crowd-m","Media-alta":"crowd-a","Alta":"crowd-a","Muy alta":"crowd-a"}
    cls = m.get(c.split()[0],"crowd-m")
    return f'<span class="{cls}">{esc(c)}</span>'

# ── Summary table ─────────────────────────────────────────────────────────────
def summary_table()->str:
    wx = {d["day"]:d for d in WEATHER["days"]}
    # D0 conducción row
    rows = [
        f"""<tr style="background:#f5f8f5">
<td><strong>D0</strong></td>
<td>domingo 16 ago<br><span style="color:var(--muted);font-size:.72rem">conducción nocturna</span></td>
<td>Teià → Canal Roya</td>
<td>~375 km · 4,5 h</td>
<td>Canal Roya (spot primera noche) {btn("Maps",gmaps_pin(42.80934,-0.51183),"g")}</td>
<td>—</td>
<td>—</td>
<td style="color:var(--muted)">5 mm · 89%</td>
<td>{btn("Ruta D0",gmaps_dir(*TEIA,*SPOT1),"g")}</td>
</tr>"""
    ]
    for d in DAYS:
        n = d["day"]
        w = wx.get(n)
        wx_html = "—"
        if w:
            cls = "wx-ok" if w["app_max"]<=25 else "wx-warn"
            wx_html = (f'<span class="{cls}">{w["app_max"]:.0f}°C</span>'
                       f'<br><span style="color:#2a5f8a">{w["precip_mm"]:.0f} mm · {w["precip_prob"]:.0f}%</span>')

        fecha_html = fmt_date(d["date"])
        star = " ⭐" if n==4 else ""
        hike_html = "—"
        if d["hike"] != "—":
            hike_html = (f'{esc(d["hike"])}<br>'
                         f'{dif_badge(d["hike_dif"])} {esc(d["hike_km"])} · {esc(d["hike_h"])}')
        # drive link
        if n==1:  dr_url = gmaps_dir(*TEIA,*CAN)
        elif n==3: dr_url = gmaps_pin(42.795,-0.458)
        elif n==4: dr_url = gmaps_dir(*CAN,*OZA)
        elif n==5: dr_url = gmaps_dir(*OZA,*YESA)
        elif n==6: dr_url = gmaps_dir(*YESA,*OCH)
        elif n==8: dr_url = gmaps_pin(42.964,-1.217)
        elif n==9: dr_url = gmaps_dir(-1.217,42.964,*ISA)
        elif n==10: dr_url = gmaps_dir(*OCH,*TEIA)
        else: dr_url = gmaps_pin(d["parking_lat"],d["parking_lon"])

        p4n_url = p4n(d["parking_lat"],d["parking_lon"])
        rows.append(
            f"""<tr>
<td><a href="#d{n}"><strong>D{n}{star}</strong></a></td>
<td>{fecha_html}</td>
<td><strong>{esc(d['zona'])}</strong></td>
<td>{esc(d['drive_km'])} · {esc(d['drive_h'])}</td>
<td>{esc(d['parking_name'])}<br>
{btn("GMaps",gmaps_pin(d['parking_lat'],d['parking_lon']),"g")}
{btn("P4N",p4n_url,"o")}</td>
<td>{hike_html}</td>
<td>{crowd_span(d['concurrencia'])}</td>
<td>{wx_html}</td>
<td>{btn("Ruta",dr_url,"g")}</td>
</tr>"""
        )
    return f"""<div class="summary-wrap">
<table class="summary-table">
<thead><tr>
<th>Día</th><th>Fecha</th><th>Zona</th><th>Conducción</th>
<th>Parking · pernocta</th><th>Excursión · dificultad</th>
<th>Concurrencia</th><th>Clima</th><th>Ruta</th>
</tr></thead>
<tbody>{"".join(rows)}</tbody>
</table></div>
<p style="font-size:.75rem;color:var(--muted);margin:.3rem 0">
Clima = sensación máx (altitude-adjusted) + precipitación previsión Open-Meteo {esc(WEATHER['fetched_at'][:10])}.
⭐ D4 = día estrella. Actualizar meteo cada mañana a las 7:00.
</p>
<p>{btns([("🗺️ Loop completo Google Maps", GMAPS_LOOP, "g"),
          ("D0 dom 16 · Teià → Canfranc", gmaps_dir(*TEIA,*CAN), "g")])}</p>"""

# ── Day cards ─────────────────────────────────────────────────────────────────
def day_card(d:dict)->str:
    n   = d["day"]
    tit = f"D{n} · {fmt_date(d['date'])} · {d['zona']}"
    sub = f"{d['drive_from']} · {d['drive_km']}" if d["drive_km"]!="—" else d["drive_from"]

    # ruta section
    if n==1:
        ruta_html = (f"<p>Llegaréis la noche del <strong>domingo 16</strong> desde Teià (~375 km, 4,5 h). "
                     f"Primer hike completo: <strong>lunes 17 por la mañana</strong>.</p>"
                     f"{btns([('Dom 16 · Teià → Canal Roya (spot)', gmaps_dir(*TEIA,*SPOT1), 'g')])}")
    elif n==4:
        ruta_html = (f"<p>Bajad a Canfranc Estación (~11 km) y continuad hasta Oza (Valle de Hecho, ~86 km · ~1h25). "
                     f"Jue 20 es el día más fresco de toda la semana aragonesa — <strong>día estrella</strong>.</p>"
                     f"{btns([('Canal Roya → Oza', gmaps_dir(*SPOT1,*OZA), 'g')])}")
    elif n==5:
        ruta_html = (f"<p>Día de transición: Oza → Jaca (~55 km · 45 min) → Yesa (~45 km · 45 min).</p>"
                     f"{btns([('Oza → Jaca', gmaps_dir(*OZA,*JACA), 'g'), ('Jaca → Yesa', gmaps_dir(*JACA,*YESA), 'g')])}")
    elif n==6:
        ruta_html = (f"<p>Yesa → Ochagavía (~90 km, ~1h15). Entrada al Pirineo navarro.</p>"
                     f"{btns([('Yesa → Ochagavía', gmaps_dir(*YESA,*OCH), 'g')])}")
    elif n==7:
        ruta_html = f"<p>Mover camper Ochagavía → zona Irabia (~15 km pista forestal ancha).</p>{btns([('Ochagavía → Irabia', gmaps_dir(*OCH,-1.032,42.933), 'g')])}"
    elif n==8:
        ruta_html = f"<p>Irabia → Orbaitzeta (~20 km pista forestal).</p>"
    elif n==9:
        ruta_html = (f"<p>Orbaitzeta → Isaba (~35 km, ~45 min). Último cambio de base.</p>"
                     f"{btns([('Orbaitzeta → Isaba', gmaps_dir(-1.217,42.964,*ISA), 'g')])}")
    elif n==10:
        ruta_html = (f"<p><strong>Vuelta a casa.</strong> ~435 km, 5–6 h. Salir antes de las 8:00.</p>"
                     f"{btns([('Ochagavía/Isaba → Teià', gmaps_dir(*ISA,*TEIA), 'g')])}")
    else:
        ruta_html = "<p>Sin traslado.</p>"

    # parking section
    parking_html = f"""<div class="spot"><strong>{esc(d['parking_name'])}</strong>
{btn("Abrir en Google Maps", gmaps_pin(d['parking_lat'],d['parking_lon']), "g")}
{btn("P4N zona", p4n(d['parking_lat'],d['parking_lon']), "o")}</div>"""

    # hike section
    if d["hike"]=="—":
        hike_html = "<p>Sin senderismo — solo conducción.</p>"
    else:
        hike_html = f"""<p><strong>{esc(d['hike'])}</strong> · {dif_badge(d['hike_dif'])} · 
{esc(d['hike_km'])} · {esc(d['hike_desn'])} desnivel · {esc(d['hike_h'])}</p>
{btns([('🗺️ Ver zona hike', gmaps_pin(d['parking_lat'],d['parking_lon']), 'g')])}"""

    # POIs
    poi_html = ", ".join(f"<strong>{esc(p)}</strong>" for p in d["interes"]) if d["interes"] else "—"

    # historia
    hist_html = f"<p>{d['historia']}</p>" if d["historia"] else ""

    # concurrencia
    obs_html = f"<p>{esc(d['observaciones'])}</p>" if d["observaciones"] else ""
    crowd_html = f"<p>Concurrencia esperada: {crowd_span(d['concurrencia'])}</p>"

    # plan B
    planb_html = f"<p><strong>Plan B lluvia:</strong> {esc(d['planb'])}</p>" if d["planb"] and d["planb"]!="—" else ""

    return f"""<article class="day-card" id="d{n}">
<div class="day-card-head"><h3>{esc(tit)}</h3><div class="sub">{esc(sub)}</div></div>
<section class="day-sec ruta"><h4>🚐 Ruta del día</h4>{ruta_html}</section>
<section class="day-sec parking"><h4>🅿️ Parking · pernocta</h4>{parking_html}</section>
<section class="day-sec hike"><h4>🥾 Excursión del día</h4>{hike_html}<p style="font-size:.82rem;color:var(--muted)">Interés: {poi_html}</p></section>
{f'<section class="day-sec historia"><h4>🏛️ Historia y contexto</h4>{hist_html}</section>' if hist_html else ""}
<section class="day-sec obs"><h4>👥 Observaciones · concurrencia</h4>{obs_html}{crowd_html}</section>
<section class="day-sec meteo"><h4>🌡️ Meteo del día</h4>{weather_block(n)}</section>
{f'<section class="day-sec planb"><h4>🌧️ Plan B lluvia</h4>{planb_html}</section>' if planb_html else ""}
</article>"""

# ── Nav ───────────────────────────────────────────────────────────────────────
def day_nav()->str:
    links = "".join(f'<a href="#d{i}">D{i}</a>' for i in range(1,11))
    return f'<nav class="day-nav wrap">{links}</nav>'

# ── Render ────────────────────────────────────────────────────────────────────
def render_spain_guide()->str:
    days_html = "".join(day_card(d) for d in DAYS)
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Guía camper · Pirineo Aragonés + Navarra · 16–26 ago 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap top-in">
<div class="brand">Guía Camper · Pirineo ≤25°C<small>16–26 ago · Canfranc · Oza · Navarra · Sunlight 600 + 2 perras</small></div>
<div class="btns">
<a class="btn btn-p" href="#resumen">Resumen</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#como-dormir">Dormir</a>
</div></div></header>
{day_nav()}
<main class="wrap">
<section class="hero">
<div class="chips">
<span class="chip">Dom 16 conducción</span>
<span class="chip">D1–3 Canfranc</span>
<span class="chip">D4 Oza ⭐</span>
<span class="chip">D5 Jaca+Nav</span>
<span class="chip">D6–9 Navarra</span>
<span class="chip">D10 vuelta</span>
</div>
<h1>Canfranc · Oza · Irati · Roncal</h1>
<p class="lead">Dom 16 noche → Canfranc · 3 días Pirineo aragonés · día estrella Oza/Aguas Tuertas ·
Selva de Irati · Valle del Roncal. Vuelta miércoles 26. Hike moderado, perras siempre.</p>
{btns([("🗺️ Loop completo",GMAPS_LOOP,"g"),("Dom 16 · Teià → Canfranc",gmaps_dir(*TEIA,*CAN),"g")])}
</section>

<section class="section" id="resumen">
<h2>Cuadro resumen completo</h2>
{summary_table()}
</section>

<section class="section" id="como-dormir">
<h2>Cómo buscar pernocta (sin P4N obligatorio)</h2>
<div class="card">
<ol style="padding-left:1.3rem;font-size:.9rem">
<li>Google Maps <strong>satélite</strong> → zoom borde río / bosque / camino forestal.</li>
<li>Buscar acceso ancho (&gt;2,10 m), sin cartel de prohibición, sin fondo de saco.</li>
<li>Street View para comprobar estado del suelo.</li>
<li>Llegar con luz — si hay cartel "prohibido pernocta" → siguiente candidato.</li>
<li><strong>Estacionar ≠ acampar</strong>: sin toldo, sin mesa fuera, sin fuego.</li>
</ol>
<div class="warn">P4N en agosto = masificado. Preferid spots no listados. Los botones P4N abren la zona en el mapa de la app.</div>
</div>
</section>

<section class="section" id="reglas">
<h2>Reglas del viaje</h2>
<div class="card">
<div class="warn"><strong>Perras:</strong> solo actividades donde entren con vosotros. Sin excepción.</div>
<div class="warn"><strong>Calor:</strong> hike cancelado si sensación máx &gt;25°C en la zona del trail.</div>
<ul style="font-size:.9rem;padding-left:1.3rem">
<li>Sunlight 600 · 2 perras · hike moderado máximo</li>
<li>Tramos ≤2 h entre bases (D0 y D10 largos)</li>
<li>Patous: correa obligatoria cerca de rebaños (toda la zona aragonesa y navarra)</li>
<li>Hike 7:00–12:00 — tardes de calor: sombra + agua para perras</li>
</ul>
</div>
</section>

<section class="section" id="dias"><h2>Día a día detallado</h2>
{days_html}
</section>

<details class="archive wrap"><summary>Versiones anteriores del itinerario (archivo)</summary>
<p class="card" style="font-size:.85rem">Albarracín–Morella–Irati, versiones Pirineo 15–24 y 16–25 con Baztán → archivadas en git.</p>
</details>

<footer class="foot wrap">
<p><strong>Guía Camper Pirineo ≤25°C</strong> · 16–26 agosto 2026 · Open-Meteo · Google Maps</p>
<p>Abrir en móvil: raw.githack → rama cursor/ruta-camper-refugio-4641 → guia-movil.html</p>
</footer>
</main>
<div class="fab">
<a class="btn btn-p" href="#resumen">Resumen</a>
<a class="btn" href="#d1">D1</a>
</div>
</body></html>"""


def main()->None:
    html_out = render_spain_guide()
    for name in ("guia-movil.html","guia-lonely-planet.html"):
        (ROOT/name).write_text(html_out, encoding="utf-8")
    print("written",len(html_out),"bytes")
    print("loop:",GMAPS_LOOP)


if __name__=="__main__":
    main()
