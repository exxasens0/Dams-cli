"""Guía camper 16–26 ago 2026 · Dom16 noche→Canfranc · D1-3 Canfranc · D4 Oza · D5 Jaca+Nav · D6-9 Navarra · D10 Teià."""
from __future__ import annotations
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEATHER = json.loads((ROOT / "_weather_es1524.json").read_text())

# ── Coordenadas clave ────────────────────────────────────────────────────────
# Formato (lon, lat) para gmaps_dir/gmaps_route; (lat, lon) para gmaps_pin/p4n
TEIA   = (2.319,    41.498)
SPOT1  = (-0.5121,  42.8091)  # P4N #285213 · Parking Carretera Astún (22889)

# Overnight spots (lon, lat) para gmaps_route
OZA_NIGHT  = (-0.738,  42.840)  # Área forestal Selva de Oza (borde pinar)
YESA       = (-1.061,  42.609)  # Embalse Yesa, margen sur
OCH        = (-1.082,  42.908)  # Ochagavía, borde río (fuera casco)
IRABIA     = (-1.015,  42.929)  # Casas de Irati / Irabia
ORBA_NIGHT = (-1.231,  42.979)  # Norte Orbaitzeta, borde río Irati
ISA        = (-0.919,  42.855)  # Isaba, borde río Esca

JACA   = (-0.549,   42.568)
ARREBOL= (-0.5098,  42.5645)  # Camping El Arrebol · N-330 km 643 · Jaca

# Anayet area (Valle de Tena, distinto valle que Astún)
PORTALET_TH = (-0.370,  42.791)  # Parking El Portalet trailhead (Anayet hike)
FORMIGAL_NIGHT = (-0.347, 42.776) # Near Sallent de Gállego / Formigal (overnight D3)

# Trailheads (lat, lon) para gmaps_pin (uso interno)
TH_ESTANES  = (42.796, -0.459)  # Astún ski base → Ibón de Estanes
TH_CANALROYA= (42.772, -0.480)  # Candanchú/Rioseta → Canal Roya
TH_ANAYET   = (42.796, -0.459)  # Astún ski base → Lagunas de Anayet
TH_AGUAS    = (42.862, -0.742)  # Parking terminal Valle Oza → Aguas Tuertas
TH_BINIES   = (42.694, -0.909)  # Acceso Foz de Biniés (junto a Biniés pueblo)
TH_ZATOIA   = (42.906, -1.067)  # Puente medieval Ochagavía → Río Zatoia
TH_IRATI    = (42.929, -1.012)  # Casas de Irati (mismo que pernocta D7)
TH_ORBA     = (42.985, -1.240)  # Parking Ruinas Fábrica de Armas Orbaitzeta
TH_ESCA     = (42.848, -0.919)  # Sur Isaba → Senda Río Esca

P4N_NIGHT1 = 285213

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
def gmaps_pin(lat, lon) -> str:
    """Navegación en coche al punto (no search: el pin cae en pistas sin acceso)."""
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&destination={lat},{lon}&travelmode=driving"
    )


def p4n(lat, lon, zoom: int = 14) -> str:
    return f"https://park4night.com/es/search?lat={lat}&lng={lon}&zoom={zoom}"


def p4n_place(place_id: int) -> str:
    return f"https://park4night.com/es/place/{place_id}"


def p4n_url_for(d: dict) -> str:
    if d.get("p4n_id"):
        return p4n_place(d["p4n_id"])
    return p4n(d["parking_lat"], d["parking_lon"])

GMAPS_LOOP = gmaps_route([TEIA, SPOT1, OZA_NIGHT, OCH, ISA, TEIA])

def btn(label,url,kind="g")->str:
    cls={"g":"btn btn-g","o":"btn btn-o","w":"btn btn-w","p":"btn btn-p"}.get(kind,"btn")
    extra = "" if str(url).startswith("#") else ' target="_blank" rel="noopener"'
    return f'<a class="{cls}" href="{esc(url)}"{extra}>{esc(label)}</a>'
def btns(items)->str:
    return '<div class="btns">'+"".join(btn(l,u,k) for l,u,k in items)+"</div>"

# ── Datos completos por día ──────────────────────────────────────────────────
# parking_lat/lon = PERNOCTA (camper duerme aquí, P4N link)
# hike_lat/lon    = TRAILHEAD (donde aparcas para iniciar el hike)
# Si hike_lat no se indica se asume igual a parking
DAYS = [
    dict(
        day=1, date="2026-08-17",
        zona="Carretera Astún · Canfranc (22889)",
        # Pernocta: P4N #285213, camino al ski Astún
        parking_name="P4N #285213 · Parking Carretera Astún",
        parking_lat=42.8091, parking_lon=-0.5121,
        p4n_id=285213,
        drive_from="Dom 16 noche, Teià → Parking Carretera Astún", drive_km="~375 km", drive_h="4,5 h",
        # Trailhead: base estación Astún (3,5 km del overnight)
        hike="Ibones de Astún + Punta Malacara (circular)", hike_lat=42.796, hike_lon=-0.459,
        hike_km="9,2 km", hike_dif="Moderado",
        hike_desn="~580 m", hike_h="4–4,5 h",
        hike_parking="Parking base estación Astún (Valle de Astún 22889, 3,5 km del overnight)",
        wikiloc_url="https://es.wikiloc.com/rutas-alpinismo/estacio-desqui-dastun-punta-malacara-ibon-de-las-truchas-ibon-de-astun-ibon-de-escalar-ibon-de-las-54386380",
        alt_hike=dict(
            nombre="Ruta de los Búnkeres – Línea P Canfranc",
            km="~9,6 km",
            desnivel="~320 m",
            dif="Fácil",
            tiempo="2,5–3 h",
            parking_lat=42.750, parking_lon=-0.525,
            parking_desc="Canfranc Estación pueblo (junto a la estación de tren)",
            wikiloc="https://es.wikiloc.com/rutas-senderismo/ruta-de-los-bunkeres-estacion-de-canfranc-149355386",
            nota=(
                "Ruta histórica por el bosque de Picauvé visitando los búnkeres de la <strong>Línea P</strong> "
                "(1944–1957), construidos por Franco para frenar una hipotética invasión aliada que nunca llegó. "
                "Más de 12 posiciones de hormigón armado defendiendo el túnel ferroviario y la estación. "
                "Perros OK · sin secciones técnicas · compatible con visita exterior estación Canfranc."
            ),
        ),
        concurrencia="Media-alta",
        interes=["Ibón de Escalar (2075 m)","Ibón de Truchas (2120 m)","Punta Malacara (2268 m)","Frontera Francia","Telesilla a los Lagos (opcional)"],
        historia=(
            "La <strong>Estación Internacional de Canfranc</strong> (1928) fue la más grande de España "
            "y segunda de Europa. Su apertura conectó España y Francia por el Pirineo central. "
            "Durante la II Guerra Mundial fue paso clandestino de judíos y se cree que por aquí "
            "salió arte expoliado por los nazis. En 1970 un accidente en el puente francés cortó el "
            "servicio; lleva décadas en rehabilitación como hotel de lujo."
        ),
        observaciones=(
            "Mañana del dom 16: llegada nocturna al P4N sin hike. "
            "🥾 Lunes 17: circular ibones desde base de Astún (3,5 km en camper). "
            "Ibón de Escalar → Ibón de Truchas → Punta Malacara (2268 m) → vuelta. "
            "Altitud máx 2268 m — dificultad moderada, sin sección técnica. "
            "🚡 Telesilla Los Lagos (opcional): sube hasta 2100 m en 10 min, directo al Ibón de Truchas. "
            "Mascotas permitidas en el telesilla. Ahorra ~350 m de desnivel; precio: ~15–20€/persona. "
            "Pozas y agua en ruta para las perras. Patous en pastizales — correa obligatoria. "
            "Parking base Astún gratuito (asfaltado). Canfranc pueblo a ~11 km para pan/gastro."
        ),
        planb="Visita exterior estación Canfranc · paseo río Aragón · Canfranc Pueblo.",
    ),
    dict(
        day=2, date="2026-08-18",
        zona="Canal Roya (AM) → Camping El Arrebol (tarde)",
        # Pernocta: Camping El Arrebol, Jaca (piscina perros, restaurante pet-friendly)
        parking_name="Camping El Arrebol · N-330 km 643 · Jaca",
        parking_lat=42.5645, parking_lon=-0.5098,
        camping_url="https://www.campingelarrebol.com",
        camping_booking="https://booking.campingelarrebol.com/bookingForm?idProduct=3&checkin=2026-08-18&checkout=2026-08-19&guestAges=18,18#additional_concepts",
        drive_from="Candanchú → El Arrebol tras el hike (AM)", drive_km="~33 km", drive_h="~30 min",
        # Trailhead: Candanchú / Rioseta (parking al pie del Canal Roya)
        hike="Canal Roya – Laguna de Tortiellas", hike_lat=42.772, hike_lon=-0.480,
        hike_km="10 km", hike_dif="Fácil-Moderado",
        hike_desn="~300 m", hike_h="3 h",
        hike_parking="Parking Candanchú / Rioseta (al pie del Canal Roya, A-136 km 45)",
        concurrencia="Media (hike) · Media (camping agosto)",
        interes=["Canal Roya glaciar","Laguna Tortiellas","GR-11","Piscina para perros El Arrebol","Zona de suelta"],
        historia=(
            "El <strong>Canal Roya</strong> es un valle glaciar que serpentea hacia la frontera "
            "francesa. Forma parte del <strong>GR-11</strong>, el sendero que cruza los Pirineos "
            "de Cabo Higuer a Cap de Creus. El nombre 'Canal' viene de los barrancos rectilíneos "
            "tallados por glaciares cuaternarios. En días claros se ven los picos fronterizos."
        ),
        observaciones=(
            "Mejor día del tramo aragonés: 0 mm, ~24°C en Canfranc (~26°C en Jaca/El Arrebol). "
            "🥾 Mañana: Canal Roya desde Candanchú (salir temprano, 7–8h). "
            "🍽️ Mediodía (~13h): conducir a Camping El Arrebol (~33 km, 30 min). "
            "Comer en el restaurante pet-friendly del camping (perros dentro). "
            "🐾 Tarde: piscina para perros + zona de suelta libre + riachuelo a pie del camping. "
            "El camping también tiene acceso a la ribera del río para que se refresquen. "
            "Máximo 2 perros; gratuito en parcelas y bungalows (+3€/noche en parcelas). "
            "📋 Reserva #109671 — Parcela, 1 noche. Estado: entrega a cuenta realizada. "
            "Contacto camping: 974 57 95 57 · info@campingelarrebol.com. "
            "⚠️ Cancelación gratis hasta 7 días antes (hasta el martes 11 ago). "
            "D3 (mié 19): salir de El Arrebol hacia Astún (~38 km, ~35 min) para Anayet."
        ),
        planb="Tarde en El Arrebol: piscina, zona de suelta, restaurante — plan B perfecto si llueve.",
    ),
    dict(
        day=3, date="2026-08-19",
        zona="Ibones de Anayet · Valle de Tena (Formigal)",
        # Pernocta: borde Sallent de Gállego / Formigal (P4N zona)
        # ⚠️ ANAYET NO ESTÁ EN ASTÚN — está en Valle de Tena, 60 km al este de Jaca
        parking_name="Borde Sallent de Gállego / Formigal (P4N zona)",
        parking_lat=42.776, parking_lon=-0.347,
        drive_from="El Arrebol → Portalet Anayet (~62 km, ~55 min)", drive_km="~62 km", drive_h="~55 min",
        # Trailhead: Parking El Portalet (ruta desde Portalet: 550 m desnivel vs 750 m desde Corral Mulas)
        hike="Ibones de Anayet desde El Portalet", hike_lat=42.791, hike_lon=-0.370,
        hike_km="10 km", hike_dif="Moderado",
        hike_desn="~550 m", hike_h="3,5–4 h",
        hike_parking="Parking El Portalet (A-136 km s/n · estación de esquí Formigal, lado norte)",
        wikiloc_url="https://es.wikiloc.com/rutas-senderismo/ibones-de-anayet-desde-el-portalet-formigal-27294107",
        concurrencia="Media-alta (agosto, destino muy conocido)",
        interes=["Ibones de Anayet (2233 m)","Pico Anayet (2574 m, solo vistas)","Midi d'Ossau","Valle de Tena","GR-11"],
        historia=(
            "Los <strong>Ibones de Anayet</strong> son unos lagos glaciares a 2.233 m situados a los pies "
            "del espectacular <strong>Pico Anayet</strong> (2.574 m), una antigua chimenea volcánica que "
            "es uno de los montes más fotogénicos del Pirineo por su silueta característica. "
            "Con el <strong>Midi d'Ossau</strong> (2.884 m, Francia) como telón de fondo, el paisaje "
            "es de fama europea. El Valle de Tena fue una de las primeras zonas con estaciones de esquí "
            "en España; Formigal (1966) es hoy una de las más grandes del país."
        ),
        observaciones=(
            "⚠️ Anayet NO está en Astún — es el Valle de Tena (Formigal), 60 km este de Jaca. "
            "Ruta desde El Portalet: 10 km, 550 m desnivel — más fresquita que la de Corral de Mulas (750 m). "
            "Ruta muy expuesta al sol sin sombra — salir antes de las 8:00. "
            "🐾 Perras: correa obligatoria (vacas y caballos en toda la ruta). "
            "🚫 PROHIBIDO BAÑARSE en los ibones (22 jun – 21 sep 2026) — multa hasta 1.000€. "
            "🦟 Sanguijuelas en el agua del ibón — no meter a las perras en el lago; sí en riachuelos del camino. "
            "💧 Sin fuentes de agua potable en ruta — llevar mínimo 2L por persona + agua extra para las perras. "
            "🏔️ No subir al pico (cadena, pasos expuestos) — quedarse en los ibones. "
            "Pernocta: P4N zona Sallent de Gállego / Formigal (42.776, -0.347)."
        ),
        planb="Sallent de Gállego pueblo (casco medieval, gastro) · borde río Gállego.",
    ),
    dict(
        day=4, date="2026-08-20",
        zona="Selva de Oza · Aguas Tuertas ⭐",
        # Pernocta: área forestal Selva de Oza
        parking_name="Área forestal Selva de Oza (borde pinar, Valle de Hecho)",
        parking_lat=42.840, parking_lon=-0.738,
        # p4n_id: sin ID confirmado → usa search centrado en el spot
        drive_from="Formigal/Portalet → Oza (Valle de Hecho)", drive_km="~90 km", drive_h="~1h30",
        # Trailhead: parking terminal del Valle de Oza (fin del asfalto), 2,5 km más al norte
        hike="Aguas Tuertas", hike_lat=42.862, hike_lon=-0.742,
        hike_km="8 km", hike_dif="Fácil",
        hike_desn="~200 m", hike_h="2,5 h",
        hike_parking="Parking terminal Valle de Oza / Borda Betés (fin del asfalto, ~2,5 km al norte de la pernocta)",
        concurrencia="Media",
        interes=["Meandros imposibles de Aguas Tuertas","Río Aragón Subordán","Hayedo-pinar Oza","Siresa s.IX"],
        historia=(
            "<strong>Aguas Tuertas</strong> ('aguas torcidas') es una pradera alpina glaciar a 1640 m "
            "donde el río Aragón Subordán forma meandros imposibles en terreno llano. "
            "<strong>Selva de Oza</strong> es un hayedo-pinar de gran valor ecológico; el Valle de Hecho "
            "conserva el <strong>cheso</strong>, dialecto aragonés con ~1.500 hablantes. "
            "El monasterio de <strong>Siresa</strong> (3 km) es el más antiguo de Aragón (s.IX)."
        ),
        observaciones=(
            "Jue 20: único día fresco de toda la semana aragonesa (~21°C sensación en Oza). "
            "Pernocta en el área forestal Oza: 42.840, -0.738 — buscar en P4N zona. "
            "Hike desde el parking terminal del asfalto (42.862, -0.742): de ahí 4 km a los meandros. "
            "Aguas Tuertas: terreno llano, agua en el río, las perras van sueltas. "
            "Siresa (3 km desde Oza): 20 min, vale la parada. Hecho pueblo (10 km) para avituallamiento."
        ),
        planb="Paseo borde río Aragón Subordán en Oza · sombra garantizada.",
    ),
    dict(
        day=5, date="2026-08-21",
        zona="Foz de Biniés → Jaca → Embalse Yesa",
        # Pernocta: borde Embalse Yesa, margen sur
        parking_name="Borde Embalse Yesa (margen sur, cerca N-240)",
        parking_lat=42.609, parking_lon=-1.061,
        drive_from="Oza → Jaca (~55 km) → Yesa (~45 km)", drive_km="~100 km", drive_h="~1h30",
        # Trailhead: Foz de Biniés (parada en ruta, 2 km antes de llegar a Biniés pueblo)
        hike="Foz de Biniés (opcional AM, parada en ruta)", hike_lat=42.694, hike_lon=-0.909,
        hike_km="4 km", hike_dif="Fácil",
        hike_desn="~80 m", hike_h="1,5 h",
        hike_parking="Parking junto a Biniés pueblo (A-1603, km 2 · se llega antes de Jaca)",
        concurrencia="Alta Jaca agosto · Baja Foz",
        interes=["Foz de Biniés (gargantas kársticas)","Ansó medieval","Jaca catedral románica","Ciudadela Jaca","Embalse Yesa"],
        historia=(
            "<strong>Jaca</strong> (820 m) fue la primera capital del Reino de Aragón. Su "
            "<strong>catedral románica</strong> (1063) es la primera románica de España. "
            "<strong>Ansó</strong> conserva el traje típico ansotano, uno de los más llamativos "
            "de España. La <strong>Foz de Biniés</strong> es un cañón kárstico excavado por el río "
            "Veral, accesible por pasarela de madera sin desnivel."
        ),
        observaciones=(
            "Día de lluvia (~16–21 mm) → ideal para conducción y cultura urbana. "
            "Foz de Biniés: si el tiempo lo permite a primera hora (pasarela fácil, 1,5 h, perros OK, "
            "desvío -10 km desde la ruta principal). Jaca: catedral exterior + ciudadela exterior. "
            "Pernocta Yesa: P4N zona 42.609, -1.061 — varios spots borde embalse y río Aragón."
        ),
        planb="Jaca: catedral + ciudadela + mercado cubierto · café bajo porches.",
    ),
    dict(
        day=6, date="2026-08-22",
        zona="Ochagavía · Valle de Salazar",
        # Pernocta: fuera del casco medieval (la camper no cabe dentro)
        parking_name="Borde río Zatoia / salida norte Ochagavía (fuera casco)",
        parking_lat=42.908, parking_lon=-1.082,
        drive_from="Yesa → Ochagavía (~90 km)", drive_km="~90 km", drive_h="~1h15",
        # Trailhead: puente medieval (entrada al sendero Zatoia, 500 m del overnight)
        hike="Sendero Río Zatoia", hike_lat=42.906, hike_lon=-1.067,
        hike_km="6 km", hike_dif="Fácil",
        hike_desn="~100 m", hike_h="2 h",
        hike_parking="Puente medieval Ochagavía (centro pueblo, ~500 m del parking nocturno)",
        concurrencia="Alta (sábado agosto)",
        interes=["Ochagavía casco medieval","Santuario de Muskilda (s.XIII)","Río Zatoia","Puente románico","Queso Roncal DOP"],
        historia=(
            "<strong>Ochagavía</strong> es la capital del Valle de Salazar. Su casco medieval tiene "
            "calles empedradas, casas de piedra con escudos y puente románico sobre el Zatoia. "
            "El <strong>Santuario de Muskilda</strong> (s.XIII) es el más venerado del Pirineo "
            "navarro — cada 8 de septiembre los danzantes bailan ante la Virgen con traje tradicional. "
            "La zona es la entrada al <strong>Queso Roncal DOP</strong> (primer queso español con DO, 1981)."
        ),
        observaciones=(
            "La camper (7 m) NO entra al casco medieval — aparcar fuera en borde del río. "
            "Coordenadas pernocta sugeridas: 42.908, -1.082 (norte del pueblo, borde prado). "
            "El sendero del Zatoia arranca desde el puente medieval (500 m andando desde la camper). "
            "Río Zatoia: agua limpia y fría, perfecto para las perras. "
            "Avituallamiento: hay supermercado en Ochagavía. Queso Roncal: comprar aquí."
        ),
        planb="Casco medieval Ochagavía · tiendas de queso Roncal · paseo río bajo la lluvia.",
    ),
    dict(
        day=7, date="2026-08-23",
        zona="Selva de Irati · Embalse Irabia",
        # Pernocta: Casas de Irati / área de aparcamiento Irabia
        parking_name="Casas de Irati · Área Irabia (fin de pista forestal asfaltada)",
        parking_lat=42.929, parking_lon=-1.015,
        drive_from="Ochagavía → Irabia (~15 km pista forestal ancha)", drive_km="~15 km", drive_h="~20 min",
        # Trailhead: mismo parking (el hike circular empieza aquí)
        hike="Circular hayedo-abetal de Irati", hike_lat=42.929, hike_lon=-1.012,
        hike_km="9 km", hike_dif="Fácil-Moderado",
        hike_desn="~250 m", hike_h="3 h",
        hike_parking="Parking Casas de Irati (= pernocta, inicio del circular)",
        concurrencia="Alta (domingo) · se diluye en la selva",
        interes=["Selva de Irati (2º bosque caducifolio Europa)","Embalse de Irabia","Hayas 500 años","Urogallo","Abodi"],
        historia=(
            "La <strong>Selva de Irati</strong> es el segundo bosque caducifolio más grande de Europa, "
            "17.000 ha de hayedo-abetal compartidas entre Navarra y el País Vasco francés. "
            "Las hayas y abetos alcanzan los 35 m; algunos ejemplares superan los 500 años. "
            "Históricamente zona de carboneo y extracción maderera para la Armada española. "
            "La selva alberga urogallos, corzos, jabalíes y, ocasionalmente, oso pardo."
        ),
        observaciones=(
            "La pista forestal Ochagavía → Irabia es amplia (ancho OK para Sunlight 600). "
            "El hike circular empieza y termina en el mismo parking donde dormís. "
            "Entrar pronto (antes de 9h): la selva se vacía aunque el parking esté lleno. "
            "Perros con correa — zona ZEPA sensible para urogallo. "
            "Agua: río Irati nace aquí, cristalino y frío."
        ),
        planb="Paseo borde embalse Irabia bajo lluvia (el hayedo con niebla es impresionante).",
    ),
    dict(
        day=8, date="2026-08-24",
        zona="Orbaitzeta · Río Irati interior",
        # Pernocta: norte de Orbaitzeta, borde río Irati (aguas arriba de las ruinas)
        parking_name="Norte Orbaitzeta · borde río Irati (aguas arriba ruinas)",
        parking_lat=42.979, parking_lon=-1.231,
        drive_from="Irabia → Orbaitzeta (~20 km pista forestal)", drive_km="~20 km", drive_h="~30 min",
        # Trailhead: parking habilitado junto a las ruinas (1 km al norte de la pernocta)
        hike="Senda Río Irati / Ruinas Orbaitzeta", hike_lat=42.985, hike_lon=-1.240,
        hike_km="7 km", hike_dif="Fácil",
        hike_desn="~100 m", hike_h="2,5 h",
        hike_parking="Parking habilitado Ruinas Fábrica de Armas (señalizado desde Orbaitzeta, ~1 km al norte)",
        concurrencia="Baja (lunes, zona remota)",
        interes=["Real Fábrica de Armas Orbaitzeta (1784)","Río Irati","Hayedo interior","Pueblo Garralda"],
        historia=(
            "Las <strong>Ruinas de la Real Fábrica de Armas de Orbaitzeta</strong> son uno de los "
            "monumentos industriales más espectaculares y olvidados de España. "
            "Construida en 1784 por orden de Carlos III para fabricar cañones para la Armada, "
            "fue destruida en 1874 durante las <strong>Guerras Carlistas</strong>. "
            "Hoy las ruinas de sillería asoman entre el hayedo como una ciudad fantasma: "
            "edificios de 3 pisos cubiertos de hiedra, fraguas, canales hidráulicos. Visita libre."
        ),
        observaciones=(
            "⚠️ Día de mayor lluvia del viaje (~34 mm posibles). "
            "Plan A (seco): senda río Irati aguas arriba + ruinas Orbaitzeta. "
            "Plan B (lluvia): las ruinas están bajo hayedo denso — visita perfecta con lluvia. "
            "Zona muy remota y tranquila. Pernocta: buscar en P4N zona 42.979, -1.231."
        ),
        planb="Ruinas Fábrica de Armas Orbaitzeta · bosque cubierto · café pueblo Garralda (12 km).",
    ),
    dict(
        day=9, date="2026-08-25",
        zona="Isaba · Valle del Roncal",
        # Pernocta: sur de Isaba, borde río Esca (junto al camping municipal o aguas abajo)
        parking_name="Sur Isaba · borde río Esca (junto a Camping El Ferial o aguas abajo)",
        parking_lat=42.853, parking_lon=-0.919,
        drive_from="Orbaitzeta → Isaba (~35 km)", drive_km="~35 km", drive_h="~45 min",
        # Trailhead: pasarela al sur del pueblo (senda Esca), ~500 m al sur del overnight
        hike="Senda Río Esca (Isaba sur)", hike_lat=42.848, hike_lon=-0.919,
        hike_km="8 km", hike_dif="Fácil",
        hike_desn="~150 m", hike_h="2,5 h",
        hike_parking="Pasarela sur de Isaba (senda del Esca, ~500 m al sur de la pernocta)",
        concurrencia="Baja (martes)",
        interes=["Isaba","Circo de Belagua","Río Esca","Queso Roncal DOP","Tributo de las Tres Vacas (1375)"],
        historia=(
            "<strong>Isaba</strong> es el pueblo más importante del <strong>Valle del Roncal</strong>. "
            "El <strong>Tributo de las Tres Vacas</strong>: desde 1375 (¡cada año sin excepción!), "
            "cada 13 de julio Francia entrega tres vacas de raza pirenaica al Valle del Roncal "
            "como compensación por uso de pastos del Pirineo. Es el único tributo que Francia paga "
            "a España. El <strong>Circo de Belagua</strong> es un anfiteatro glaciar con vistas al "
            "Pico de Anie (2463 m)."
        ),
        observaciones=(
            "Último día en Navarra. Senda del Esca: plana, sombreada, perfecta para perras. "
            "La pasarela de inicio está a ~500 m al sur de la pernocta — no necesitáis mover la camper. "
            "Isaba tiene queso Roncal en varias tiendas — comprar para llevar a casa. "
            "Circo de Belagua (si tiempo mejora): 14 km A/R, moderado, arranca 8 km al norte de Isaba."
        ),
        planb="Paseo pueblo Isaba · compras queso Roncal · río Esca pasarela.",
    ),
    dict(
        day=10, date="2026-08-26",
        zona="Vuelta a Teià",
        parking_name="Teià — casa",
        parking_lat=41.498, parking_lon=2.319,
        drive_from="Isaba → Teià (~435 km)", drive_km="~435 km", drive_h="5–6 h",
        hike="—", hike_lat=None, hike_lon=None,
        hike_km="—", hike_dif="—", hike_desn="—", hike_h="—",
        hike_parking="",
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
:root{--bg:#f2eee4;--ink:#1a221c;--muted:#4d5c52;--card:#fffdf8;--pine:#1b4a3b;--clay:#9a5528;--line:#d7cdbc;--shadow:0 10px 24px rgba(26,34,28,.08);--sec:#e8efe9;--red:#a33;--gold:#7a5a00}
*{box-sizing:border-box}html{scroll-behavior:smooth;overflow-x:hidden;-webkit-text-size-adjust:100%}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.55;overflow-wrap:anywhere;word-break:break-word}
.wrap{max-width:720px;margin:0 auto;padding:0 .85rem 5.5rem}
.chrome{position:sticky;top:0;z-index:50;background:rgba(242,238,228,.98);border-bottom:1px solid var(--line)}
.top-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.35rem;padding:.45rem 0 .15rem}
.brand{font-weight:800;color:var(--pine);font-size:.92rem}
.brand small{display:none;font-size:.68rem;font-weight:400;color:var(--muted)}
@media(min-width:520px){.brand small{display:block}}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:.45rem .75rem;border-radius:8px;font-size:.8rem;font-weight:600;text-decoration:none;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.btn-p{background:var(--pine);color:#fff;border-color:var(--pine)}.btn-g{background:#eef4ee}.btn-o{background:#fff3e6}
.btns{display:flex;flex-wrap:wrap;gap:.35rem;margin:.35rem 0}
.hero{padding:1rem 0 .5rem}.hero h1{font-size:1.35rem;margin:.25rem 0;color:var(--pine)}
.lead{color:var(--muted);font-size:.92rem}
.chips{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.45rem}
.chip{font-size:.68rem;font-weight:700;background:var(--sec);color:var(--pine);padding:.2rem .5rem;border-radius:999px}
.section{margin:1.4rem 0}.section>h2{color:var(--pine);border-bottom:2px solid var(--clay);padding-bottom:.3rem;font-size:1.15rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.85rem .95rem;margin:.7rem 0}
.warn{background:#fff4e6;border-left:4px solid var(--clay);padding:.6rem .8rem;border-radius:8px;margin:.55rem 0}
.callout{background:var(--sec);padding:.6rem .8rem;border-radius:8px;margin:.55rem 0}
.day-nav{display:grid;grid-template-columns:repeat(5,1fr);gap:.25rem;padding:.35rem 0 .5rem}
@media(min-width:640px){.day-nav{grid-template-columns:repeat(11,1fr)}}
.day-nav a{font-size:.72rem;text-align:center;min-height:38px;display:flex;align-items:center;justify-content:center;padding:.35rem .1rem;border-radius:6px;text-decoration:none;color:var(--pine);font-weight:700;background:var(--card);border:1px solid var(--line)}
.badge{display:inline-block;padding:.12rem .45rem;border-radius:999px;font-size:.68rem;font-weight:700}
.dif-f{background:#d4edda;color:#155724}.dif-m{background:#fff3cd;color:#856404}
.crowd-b{color:#155724;font-weight:700}.crowd-m{color:#856404;font-weight:700}.crowd-a{color:var(--red);font-weight:700}
.wx-ok{color:var(--pine);font-weight:700}.wx-warn{color:var(--red);font-weight:700}
.sum-card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.75rem .85rem;margin:.65rem 0}
.sum-card .k{font-size:.68rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
.sum-card h3{margin:.15rem 0 .4rem;font-size:1.02rem;color:var(--pine)}
.sum-card .row{display:grid;grid-template-columns:4.6rem 1fr;gap:.15rem .4rem;font-size:.86rem;margin:.12rem 0}
.sum-card .row b{color:var(--muted);font-weight:600;font-size:.75rem}
.day-card{background:var(--card);border:1px solid var(--line);border-radius:16px;margin:1.3rem 0;overflow:hidden}
.day-card-head{background:var(--pine);color:#fff;padding:.9rem 1rem}
.day-card-head h3{margin:0;font-size:1.05rem}
.day-card-head .sub{opacity:.9;font-size:.8rem;margin-top:.2rem}
.day-sec{padding:.75rem .9rem;border-top:1px solid var(--line)}
.day-sec h4{margin:0 0 .4rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--clay)}
.day-sec.ruta{background:#f8faf8}.day-sec.parking{background:#f5f8f5}.day-sec.hike{background:#f0f8f0}
.day-sec.historia{background:#fffbf3}.day-sec.obs{background:#fafafa}.day-sec.meteo{background:#f0f6fa}.day-sec.planb{background:#fff8f0}
.spot{margin:.35rem 0;padding:.5rem .65rem;background:var(--sec);border-radius:8px;font-size:.88rem}
.spot strong{display:block;color:var(--pine);margin-bottom:.15rem}
.wx-grid{display:grid;grid-template-columns:1fr 1fr;gap:.35rem;font-size:.84rem}
.wx-grid>div{background:#e8f4fb;padding:.4rem .5rem;border-radius:6px}
.wx-grid em{display:block;font-size:.68rem;color:var(--muted);font-style:normal}
.wx-grid strong{display:block}
.foot{padding:1.3rem 0;color:var(--muted);font-size:.8rem;border-top:1px solid var(--line)}
.fab{position:fixed;bottom:.8rem;right:.8rem;display:flex;gap:.3rem;z-index:60}
details.archive{margin:1.2rem 0}details.archive summary{cursor:pointer;font-weight:700;color:var(--muted)}
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

def _drive_url(d: dict) -> str:
    n = d["day"]
    if n==1: return gmaps_dir(*TEIA,*SPOT1)
    if n==2: return gmaps_dir(*SPOT1,*ARREBOL)
    if n==3: return gmaps_dir(*ARREBOL,*PORTALET_TH)
    if n==4: return gmaps_dir(*FORMIGAL_NIGHT,*OZA_NIGHT)
    if n==5: return gmaps_dir(*OZA_NIGHT,*YESA)
    if n==6: return gmaps_dir(*YESA,*OCH)
    if n==7: return gmaps_dir(*OCH,*IRABIA)
    if n==8: return gmaps_dir(*IRABIA,*ORBA_NIGHT)
    if n==9: return gmaps_dir(*ORBA_NIGHT,*ISA)
    if n==10: return gmaps_dir(*ISA,*TEIA)
    return gmaps_pin(d["parking_lat"], d["parking_lon"])


def summary_table() -> str:
    wx = {d["day"]: d for d in WEATHER["days"]}
    cards = []

    cards.append(f"""<article class="sum-card" id="d0">
<div class="k">D0 · conducción</div>
<h3>domingo 16 ago · Teià → Parking Astún</h3>
<div class="row"><b>Km</b><span>~375 km · 4,5 h</span></div>
<div class="row"><b>Parking</b><span>P4N #285213 Carretera Astún (22889)</span></div>
<div class="row"><b>Hike</b><span>Sin hike · llegada noche</span></div>
<div class="row"><b>Clima</b><span>lluvia posible en llegada</span></div>
{btns([("Conducir al parking", gmaps_dir(*TEIA,*SPOT1), "g"), ("Ficha P4N", p4n_place(P4N_NIGHT1), "o")])}
</article>""")

    for d in DAYS:
        n = d["day"]
        w = wx.get(n)
        wx_html = "—"
        if w:
            cls = "wx-ok" if w["app_max"] <= 25 else "wx-warn"
            wx_html = f'<span class="{cls}">{w["app_max"]:.0f}°C</span> · {w["precip_mm"]:.0f} mm ({w["precip_prob"]:.0f}%)'
        hike_html = "—"
        if d["hike"] != "—":
            hike_html = f'{esc(d["hike"])} · {dif_badge(d["hike_dif"])} · {esc(d["hike_km"])} · {esc(d["hike_h"])}'
        star = " ⭐" if n == 4 else ""
        night_link = d["camping_url"] if d.get("camping_url") else p4n_url_for(d)
        night_label = "Web Camping" if d.get("camping_url") else ("Ficha P4N" if d.get("p4n_id") else "P4N zona")
        cards.append(f"""<article class="sum-card">
<div class="k"><a href="#d{n}">D{n}{star}</a></div>
<h3>{fmt_date(d["date"])} · {esc(d["zona"])}</h3>
<div class="row"><b>Km</b><span>{esc(d["drive_km"])} · {esc(d["drive_h"])}</span></div>
<div class="row"><b>Pernocta</b><span>{esc(d["parking_name"])}</span></div>
<div class="row"><b>Hike</b><span>{hike_html}</span></div>
<div class="row"><b>Gente</b><span>{crowd_span(d["concurrencia"])}</span></div>
<div class="row"><b>Clima</b><span>{wx_html}</span></div>
{btns([
    ("Conducir", _drive_url(d), "g"),
    (night_label, night_link, "o"),
    ("Detalle", f"#d{n}", "p"),
])}
</article>""")

    return f"""
<p>{btns([("🗺️ Loop completo", GMAPS_LOOP, "g"), ("D0 Teià → P4N #285213", gmaps_dir(*TEIA,*SPOT1), "g")])}</p>
{"".join(cards)}
<p style="font-size:.75rem;color:var(--muted)">Clima Open-Meteo {esc(WEATHER['fetched_at'][:10])} · revisar 7:00. ⭐ D4 día estrella.</p>
"""

# ── Day cards ─────────────────────────────────────────────────────────────────
def day_card(d:dict)->str:
    n   = d["day"]
    tit = f"D{n} · {fmt_date(d['date'])} · {d['zona']}"
    sub = f"{d['drive_from']} · {d['drive_km']}" if d["drive_km"]!="—" else d["drive_from"]

    # ruta section
    if n==1:
        ruta_html = (f"<p>Llegaréis la noche del <strong>domingo 16</strong> desde Teià (~375 km, 4,5 h). "
                     f"Primer hike completo: <strong>lunes 17 por la mañana</strong>.</p>"
                     f"{btns([('Dom 16 · Teià → P4N #285213 (conducir)', gmaps_dir(*TEIA,*SPOT1), 'g')])}")
    elif n==2:
        ruta_html = (f"<p>🥾 Mañana Canal Roya (7–12h) · 🍽️ 13h conducir a Camping El Arrebol (~33 km, 30 min). "
                     f"Tarde-noche en el camping: piscina para perros, zona de suelta, restaurante.</p>"
                     f"{btns([('Candanchú → El Arrebol (conducir)', gmaps_dir(*SPOT1,*ARREBOL), 'g')])}")
    elif n==3:
        ruta_html = (f"<p>El Arrebol → Parking El Portalet (Formigal) ~62 km, ~55 min via Sabiñánigo/Biescas. "
                     f"⚠️ Anayet NO está en Astún — es el Valle de Tena, otro valle diferente.</p>"
                     f"{btns([('El Arrebol → Portalet Anayet (conducir)', gmaps_dir(*ARREBOL,*PORTALET_TH), 'g')])}")
    elif n==4:
        ruta_html = (f"<p>Formigal/Portalet → Oza (Valle de Hecho, ~90 km · ~1h30 via Sabiñánigo). "
                     f"Jue 20 es el día más fresco de toda la semana aragonesa — <strong>día estrella</strong>.</p>"
                     f"{btns([('Formigal → Oza (conducir)', gmaps_dir(*FORMIGAL_NIGHT,*OZA_NIGHT), 'g')])}")
    elif n==5:
        ruta_html = (f"<p>Día de transición: Oza → Jaca (~55 km · 45 min) → Yesa (~45 km · 45 min).</p>"
                     f"{btns([('Oza → Jaca', gmaps_dir(*OZA_NIGHT,*JACA), 'g'), ('Jaca → Yesa', gmaps_dir(*JACA,*YESA), 'g')])}")
    elif n==6:
        ruta_html = (f"<p>Yesa → Ochagavía (~90 km, ~1h15). Entrada al Pirineo navarro.</p>"
                     f"{btns([('Yesa → Ochagavía (conducir)', gmaps_dir(*YESA,*OCH), 'g')])}")
    elif n==7:
        ruta_html = (f"<p>Mover camper Ochagavía → Casas de Irati/Irabia (~15 km pista forestal ancha, OK para Sunlight 600).</p>"
                     f"{btns([('Ochagavía → Casas de Irati (conducir)', gmaps_dir(*OCH,*IRABIA), 'g')])}")
    elif n==8:
        ruta_html = (f"<p>Irabia → Orbaitzeta (~20 km, continua la pista forestal).</p>"
                     f"{btns([('Irabia → Orbaitzeta (conducir)', gmaps_dir(*IRABIA,*ORBA_NIGHT), 'g')])}")
    elif n==9:
        ruta_html = (f"<p>Orbaitzeta → Isaba (~35 km, ~45 min). Último cambio de base.</p>"
                     f"{btns([('Orbaitzeta → Isaba (conducir)', gmaps_dir(*ORBA_NIGHT,*ISA), 'g')])}")
    elif n==10:
        ruta_html = (f"<p><strong>Vuelta a casa.</strong> ~435 km, 5–6 h. Salir antes de las 8:00.</p>"
                     f"{btns([('Isaba → Teià (conducir)', gmaps_dir(*ISA,*TEIA), 'g')])}")
    else:
        ruta_html = "<p>Sin traslado — misma base.</p>"

    # parking section
    if d.get("camping_url"):
        camping_btns = btns([
            ("Conducir aquí (Google)", gmaps_pin(d["parking_lat"], d["parking_lon"]), "g"),
            ("Web El Arrebol", d["camping_url"], "o"),
            ("Reservar parcela", d["camping_booking"], "p"),
        ])
        camping_badge = '<span style="background:#d4edda;color:#155724;font-size:.72rem;font-weight:700;padding:.2rem .5rem;border-radius:999px">🐾 Camping pet-friendly · piscina perros</span>'
        parking_html = f"""<div class="spot"><strong>{esc(d['parking_name'])}</strong>
{camping_badge}
<p style="margin:.25rem 0;font-size:.82rem;color:var(--muted)">Perros gratis en bungalows · +3€/noche en parcelas · máx 2 perros · perros en el restaurante</p>
{camping_btns}</div>"""
    else:
        parking_html = f"""<div class="spot"><strong>{esc(d['parking_name'])}</strong>
<p style="margin:.25rem 0;font-size:.82rem;color:var(--muted)">Navegación en coche al parking (no pin suelto).</p>
{btn("Conducir aquí (Google)", gmaps_pin(d['parking_lat'],d['parking_lon']), "g")}
{btn("Ficha P4N" if d.get("p4n_id") else "P4N zona", p4n_url_for(d), "o")}</div>"""

    # hike section
    if d["hike"]=="—":
        hike_html = "<p>Sin senderismo — solo conducción.</p>"
    else:
        hlat = d.get("hike_lat") or d["parking_lat"]
        hlon = d.get("hike_lon") or d["parking_lon"]
        hp   = d.get("hike_parking","")
        same_as_night = (abs(hlat - d["parking_lat"]) < 0.001 and abs(hlon - d["parking_lon"]) < 0.001)
        th_note = ("<em style='font-size:.8rem;color:var(--muted)'>Trailhead = pernocta, no hay que mover la camper.</em>"
                   if same_as_night else
                   f"<em style='font-size:.8rem;color:var(--muted)'>{esc(hp)}</em>")
        wl_btn = (f'\n{btn("📍 Wikiloc · ruta completa", d["wikiloc_url"], "o")}' if d.get("wikiloc_url") else "")
        hike_html = f"""<p><strong>{esc(d['hike'])}</strong> · {dif_badge(d['hike_dif'])} · \
{esc(d['hike_km'])} · {esc(d['hike_desn'])} desnivel · {esc(d['hike_h'])}</p>
{th_note}
{btns([('🗺️ Navegar al trailhead (Google)', gmaps_pin(hlat, hlon), 'g')])}{wl_btn}
<p style="font-size:.75rem;color:var(--muted)">Confirmar ruta en Wikiloc/AllTrails antes del hike.</p>"""

        # Alternative hike (e.g. Plan B or bonus route)
        if d.get("alt_hike"):
            ah = d["alt_hike"]
            hike_html += f"""
<details style="margin-top:.75rem;border:1px solid var(--line);border-radius:10px;overflow:hidden">
<summary style="padding:.6rem .85rem;background:var(--sec);cursor:pointer;font-size:.82rem;font-weight:700;color:var(--pine)">
🏛️ Alternativa histórica: {esc(ah['nombre'])} ({esc(ah['dif'])} · {esc(ah['km'])})
</summary>
<div style="padding:.75rem .85rem;font-size:.85rem">
<p>{ah['nota']}</p>
<p style="font-size:.8rem;color:var(--muted)">{esc(ah['km'])} · {esc(ah['desnivel'])} desnivel · {esc(ah['tiempo'])}</p>
<p style="font-size:.78rem;color:var(--muted)">Inicio: {esc(ah['parking_desc'])}</p>
{btns([('🗺️ Navegar al inicio (Google)', gmaps_pin(ah['parking_lat'], ah['parking_lon']), 'g'),
       ('📍 Wikiloc · ruta búnkeres', ah['wikiloc'], 'o')])}
</div>
</details>"""

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
    links = '<a href="#d0">D0</a>' + "".join(f'<a href="#d{i}">D{i}</a>' for i in range(1,11))
    return f'<nav class="day-nav">{links}</nav>'

# ── Render ────────────────────────────────────────────────────────────────────
def render_spain_guide()->str:
    days_html = "".join(day_card(d) for d in DAYS)
    return f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Guía camper · Pirineo · 16–26 ago 2026</title>
<style>{CSS}</style>
</head><body>
<div class="chrome"><div class="wrap">
<header class="top-in">
<div class="brand">Guía Camper · Pirineo ≤25°C<small>16–26 ago · Canfranc · Oza · Navarra · Sunlight 600 + 2 perras</small></div>
<div class="btns">
<a class="btn btn-p" href="#resumen">Resumen</a>
<a class="btn btn-g" href="#d1">Días</a>
<a class="btn btn-o" href="#como-dormir">Dormir</a>
</div>
</header>
{day_nav()}
</div></div>
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
{btns([("🗺️ Loop completo",GMAPS_LOOP,"g"),("Dom 16 · Teià → P4N #285213",gmaps_dir(*TEIA,*SPOT1),"g")])}
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
<p>Si GitHub enseña código: descargad <code>guia-movil.html</code> y abridlo en el navegador. No uses raw.githubusercontent.com.</p>
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
