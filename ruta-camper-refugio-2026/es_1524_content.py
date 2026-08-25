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
VILLANUA= (-0.566,   42.784)   # P4N #135785 · Villanúa · 7 Calle Piscinas (borde río)
CANDANCHU = (-0.5360, 42.7867)  # P4N #532128 · Candanchú estación (1.520 m)
ARTIEDA = (-0.9834, 42.6031)   # P4N #82683 · Artieda borde Río Aragón
ANGLASE = (-0.505,  42.770)    # Parking Anglasé · Canal Roya trailhead
BORDA   = (-0.738,  42.754)    # Camping Borda Bisaltico · Valle de Hecho
GARCIPOLLERA = (-0.5472, 42.6274)  # Calle Valle Garcipollera · Castiello (acceso pozas Puente Viejo)
SAN_MIGUEL   = (-0.5622, 42.5743)  # Puente San Miguel · badinas río Aragón (Jaca)

# Additional route stops
ANSO   = (-0.821,   42.759)  # Ansó pueblo (pueblo más bonito de España)
BINIES = (-0.909,   42.694)  # Foz de Biniés / Biniés pueblo

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

GMAPS_LOOP = gmaps_route([TEIA, SPOT1, CANDANCHU, ARREBOL, BORDA, ARTIEDA, OCH, IRABIA, ORBA_NIGHT, ISA, TEIA])

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
        hike_from_overnight="3,5 km · 5 min en camper (P4N #285213 → base Astún)",
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
        zona="Búnkeres Línea P (AM) · Candanchú (noche)",
        # Pernocta: P4N #532128 Candanchú (estación de esquí, 1.520 m, gratuito, fresco)
        parking_name="P4N #532128 · Candanchú · Parking estación de esquí (1.520 m)",
        parking_lat=42.7867, parking_lon=-0.5360,
        p4n_id=532128,
        drive_from="Canfranc Estación → Candanchú (tras el hike)", drive_km="~9 km", drive_h="~10 min",
        # Trailhead: Canfranc Estación pueblo
        hike="Ruta de los Búnkeres – Línea P Canfranc", hike_lat=42.750, hike_lon=-0.525,
        hike_km="9,6 km", hike_dif="Fácil",
        hike_desn="~320 m", hike_h="2,5–3 h",
        hike_parking="Canfranc Estación pueblo (junto a la estación internacional de tren)",
        wikiloc_url="https://es.wikiloc.com/rutas-senderismo/ruta-de-los-bunkeres-estacion-de-canfranc-149355386",
        hike_from_overnight="~9 km · 10 min del P4N #532128 Candanchú a Canfranc Estación",
        concurrencia="Baja (ruta poco conocida)",
        interes=["Búnkeres Línea P (1944–57)","Bosque Picauvé","Mirador Estación Canfranc","Río Aragón","Candanchú a 1.520 m"],
        historia=(
            "La <strong>Línea P</strong> ('P' de Pirineos) fue el mayor proyecto de ingeniería militar "
            "de la España franquista: entre 1944 y 1957 se construyeron cientos de búnkeres de hormigón "
            "en los valles fronterizos para frenar una hipotética invasión aliada que nunca llegó. "
            "En Canfranc, el <strong>Núcleo de Resistencia nº 111 «Los Arañones»</strong> defendía "
            "el túnel ferroviario y la estación. El asentamiento C-1 apuntaba directamente a la boca "
            "del túnel desde el bosque. Algunos búnkeres se construyeron adosados a la propia obra "
            "ferroviaria, imitando el despiece de los sillares para camuflarlos."
        ),
        observaciones=(
            "D1 exigente (ibones + Malacara, 580 m). D2 = ruta fácil e histórica. "
            "🥾 Mañana: Búnkeres desde Canfranc Estación (~9 km del overnight, 10 min en camper). "
            "Bosque Picauvé + 12+ búnkeres Núcleo 111 + mirador estación. Fácil, perros OK. "
            "Tras el hike: subir ~9 km a Candanchú · P4N #532128 (gratuito, 18 plazas, 1.520 m, fresco). "
            "Sin servicios — vaciar en Canfranc Estación antes de subir. "
            "Normas: sin toldos ni mesas fuera. Puerta no hay, abierto todo el año. "
            "D3 mañana: Canal Roya desde Parking Anglasé (~6 km al sur del overnight)."
        ),
        planb="Paseo en Candanchú · vista hacia frontera · bar de la estación.",
    ),
    dict(
        day=3, date="2026-08-19",
        zona="Canal Roya (AM) · Pozas Garcipollera (PM) · El Arrebol",
        # Pernocta: Camping El Arrebol (reserva #109671 modificada a 19→20 ago)
        parking_name="Camping El Arrebol · N-330 km 643 · Jaca",
        parking_lat=42.5645, parking_lon=-0.5098,
        camping_url="https://www.campingelarrebol.com",
        camping_booking="https://booking.campingelarrebol.com/bookingForm?idProduct=3&checkin=2026-08-19&checkout=2026-08-20&guestAges=18,18#additional_concepts",
        drive_from="Parking Anglasé (hike) → El Arrebol", drive_km="~27 km", drive_h="~27 min",
        # Trailhead: Parking de Anglasé (N-330 entre Canfranc-Estación y Candanchú, antes de Rioseta)
        hike="Canal Roya – La Rinconada (GR-11)", hike_lat=42.770, hike_lon=-0.505,
        hike_km="14 km", hike_dif="Moderado",
        hike_desn="~520 m", hike_h="4–4,5 h",
        hike_parking="Parking Anglasé (N-330, entre Canfranc-Estación y Rioseta, ~6 km al sur del overnight Candanchú)",
        wikiloc_url="https://senderosturisticos.turismodearagon.com/ruta/ficha/148",
        hike_from_overnight="~6 km · 8 min al sur del P4N #532128 Candanchú (N-330 hacia Canfranc)",
        concurrencia="Media (GR-11 conocido pero no masificado)",
        interes=["Canal Roya (valle glaciar GR-11)","Refugio de Lacuars","La Rinconada (circo glaciar, 1.870 m)","Anayet de telón de fondo","Antigua Fondería Anglasé s.XIX","Villanúa (de paso)","Pozas de la Garcipollera (Puente Viejo)","Puente San Miguel · badinas río Aragón","Ciudadela de Jaca (plan C)"],
        historia=(
            "La <strong>Canal Roya</strong> es un valle de origen glaciar por el que discurre la etapa 12 del "
            "<strong>GR-11</strong>, el sendero transpirenaico de Hondarribia a Cadaqués. "
            "El camino pasa junto a la <strong>Fondería de Anglasé</strong>, restos de una fundería de cobre "
            "y hierro activa en los siglos XVIII–XIX para abastecer a las poblaciones del valle. "
            "Al fondo del valle, el <strong>Plano de la Rinconada</strong> (1.870 m) es un circo glaciar "
            "cerrado por las paredes del imponente <strong>Pico de Anayet</strong> (2.545 m), volcán extinto "
            "cuya chimenea forma una de las siluetas más características de todo el Pirineo. "
            "Por la tarde, las <strong>Pozas de la Garcipollera</strong> (Badinas del Puente Viejo, Castiello de Jaca) "
            "se forman en el río Ijuez bajo el acueducto de piedra del Canal de Jaca: triple poza de agua helada "
            "y sombra de ribera, a ~9 km del camping. El <strong>Puente San Miguel</strong> (s.XV, BIC) cruza el "
            "Aragón al oeste de Jaca; hay badinas a su pie. La <strong>Ciudadela de Jaca</strong> (s.XVI) queda "
            "como plan C si nublado — 5€, ~2 h; perros en el foso exterior, no en el museo."
        ),
        observaciones=(
            "⚠️ Dos climas el mismo día: hike Canal Roya sensación ~29°C; valle de Jaca / El Arrebol "
            "<strong>~36°C</strong> (sensación ~33°C). No quedarse en la parcela al sol por la tarde. "
            "Salir del P4N Candanchú a las 7:00, ~6 km al sur hasta Parking Anglasé; acabar el hike antes de las 12:00. "
            "Seguir las marcas del GR-11. Cruces de río con pasos entre piedras — las perras se refrescan en ruta. "
            "🏘️ De camino a El Arrebol (~27 km · ~27 min) pasáis por <strong>Villanúa</strong> — "
            "parada opcional 15-20 min (Cueva de las Güixas). "
            "🍽️ ~13-14h: check-in El Arrebol, comer rápido y salir. "
            "💧 <strong>Plan A tarde (16-19h): Pozas de la Garcipollera</strong> — triple poza bajo acueducto, "
            "río Ijuez, agua helada, sombra de árboles. ~9 km · ~9 min desde El Arrebol "
            "(Calle del Valle de la Garcipollera, Castiello). Parking en el desvío / apartadero de asfalto "
            "(no bajar la camper por la pista de piedras: se quedan furgos atascadas). "
            "15-20 min a pie hasta las pozas. Calzado de río, toallas; llegar pronto para coger sombra. "
            "Perros OK con correa. "
            "🔄 <strong>Plan B (más cerca): Puente San Miguel</strong> — ~5 km · ~8 min, badinas del Aragón "
            "con sombra. Menos espectacular, muy práctico si hay prisa o cansancio. "
            "🏰 <strong>Plan C (solo nublado): Ciudadela de Jaca</strong> (5€, ~2h) — a ~5 km. "
            "Perros no entran al museo; sí al foso exterior. "
            "🐾 Noche: piscina para perros El Arrebol mejor ~20-21h, cuando baje el calor. "
            "📋 Reserva El Arrebol #109671 · Parcela Estándar · 19/08→20/08 (salida 12:00h). "
            "💶 Total: 47€ (35€ parcela + 6€ adulto + 6€ dos perras). Depósito: 14,10€. Pendiente: 32,90€. "
            "☎️ 974 57 95 57 · info@campingelarrebol.com."
        ),
        planb="Canal Roya se puede acortar volviendo desde el Refugio de Lacuars (~10 km, ~300 m). "
              "Si tormenta: saltar las pozas y quedarse en El Arrebol (sombra/AC + piscina perros al atardecer). "
              "Si solo nubes: Ciudadela de Jaca (5€, ~2h).",
    ),
    dict(
        day=4, date="2026-08-20",
        zona="Selva de Oza · Aguas Tuertas ⭐",
        # Pernocta: Camping Borda Bisaltico (Valle de Hecho, 9 km de Hecho hacia Oza)
        # Plan B: P4N #227980 (42.7705,-0.7424) — gratuito, zona discutida legalmente, forestal dijo que está
        #         fuera del parque pero la pernocta sigue prohibida en Aragón según reglamento.
        parking_name="Camping Borda Bisaltico · Ctra. Gabardito km 2 · Valle de Hecho",
        parking_lat=42.754, parking_lon=-0.738,
        camping_url="https://bordabisaltico.com/camping-valle-hecho-junto-selva-oza-pirineos/",
        camping_booking="https://bordabisaltico.com/situacion-y-contacto/",
        p4n_backup=227980,  # Plan B: gratuito, legalmente discutido pero tolerable
        drive_from="El Arrebol → Hecho → Borda Bisaltico", drive_km="~52 km", drive_h="~1 h",
        # Trailhead: parking terminal del Valle de Oza (fin del asfalto), ~13 km al norte del camping
        hike="Aguas Tuertas", hike_lat=42.862, hike_lon=-0.742,
        hike_km="8 km", hike_dif="Fácil",
        hike_desn="~200 m", hike_h="2,5 h",
        hike_parking="Parking terminal Valle de Oza / Borda Betés (fin del asfalto, ~13 km al norte del camping)",
        hike_from_overnight="~13 km · ~30 min al norte del camping (carretera del valle; tramo lento)",
        concurrencia="Media",
        interes=["Meandros imposibles de Aguas Tuertas","Río Aragón Subordán","Hayedo-pinar Oza","Siresa s.IX","Boca del Infierno","Hecho (arquitectura pirenaica)"],
        historia=(
            "<strong>Aguas Tuertas</strong> ('aguas torcidas') es una pradera alpina glaciar a 1640 m "
            "donde el río Aragón Subordán forma meandros imposibles en terreno llano. "
            "<strong>Selva de Oza</strong> es un hayedo-pinar de gran valor ecológico; el Valle de Hecho "
            "conserva el <strong>cheso</strong>, dialecto aragonés con ~1.500 hablantes. "
            "El monasterio de <strong>Siresa</strong> (3 km) es el más antiguo de Aragón (s.IX). "
            "El pueblo de <strong>Hecho</strong> conserva el trazado y la arquitectura pirenaica tradicional: "
            "casas de piedra con tejados de losa, chimeneas troncocónicas y balcones de madera. "
            "Tiene un singular museo de escultura contemporánea al aire libre repartido por sus calles."
        ),
        observaciones=(
            "⏰ Salida El Arrebol 12:00h (checkout) → Borda Bisaltico ~52 km, ~1 h. "
            "🏘️ De camino, paráis en <strong>Hecho pueblo</strong> (justo antes de Borda Bisaltico) — "
            "callejeo 20-30 min por su casco de arquitectura pirenaica y el museo de escultura al aire libre. "
            "Check-in camping desde las 12h (coincide bien con la salida de El Arrebol). "
            "Jue 20: día fresco (~22°C sensación en Oza) con chubascos posibles. "
            "Dejar la camper en Borda Bisaltico y conducir ~13 km / ~30 min al norte hasta el trailhead. "
            "Hike Aguas Tuertas tarde (14h–17h) — terreno llano, agua en el río, perras sueltas. "
            "Siresa (3 km de Oza): monasterio s.IX, 20 min, vale la parada. "
            "⚠️ Sin reservas para parcelas — llamad 3 días antes para consultar ocupación: "
            "☎️ 974 34 89 40 / 696 981 816. Puerta cerrada 00:00–08:30h. "
            "🆘 Plan B si lleno: P4N #227980 (42.7705,-0.7424) — zona discutida, forestal confirmó fuera "
            "del parque pero pernocta reglamentariamente prohibida en Aragón (discretion advised)."
        ),
        planb="Paseo borde río Aragón Subordán en Oza · sombra garantizada · Siresa monasterio.",
    ),
    dict(
        day=5, date="2026-08-21",
        zona="Ansó (pueblo más bonito) → Foz de Biniés → Artieda / Yesa",
        # Pernocta opción 1: P4N #82683 (Artieda, borde río Aragón) — más natural pero acceso justo para 7m
        # Pernocta opción 2: P4N #26522 (Yesa, Monasterio de Leyre) — fácil acceso, cultural, recomendado AC grande
        # Pernocta opción 3: P4N #552933 (Yesa, borde río) — solo 2 plazas, mosquitos+++
        parking_name="P4N #82683 · Artieda · Borde Río Aragón",
        parking_lat=42.6031, parking_lon=-0.9834,
        p4n_id=82683,
        p4n_alts=[
            (26522,  "P4N #26522 · Monasterio Leyre (Yesa)", 42.6367, -1.1727),
            (552933, "P4N #552933 · Yesa · Borde Río (2 plazas)", 42.6109, -1.2179),
        ],
        drive_from="Borda Bisaltico → Ansó → Foz Biniés → Artieda/Yesa", drive_km="~68 km", drive_h="~2h35",
        # Trailhead: Foz de Biniés (parada en ruta)
        hike="Foz de Biniés (opcional AM, parada en ruta)", hike_lat=42.694, hike_lon=-0.909,
        hike_km="4 km", hike_dif="Fácil",
        hike_desn="~80 m", hike_h="1,5 h",
        hike_parking="Parking junto a Biniés pueblo (A-1603)",
        hike_from_overnight="Foz de Biniés está en ruta (~40 km · ~1h35 desde Borda vía Ansó)",
        concurrencia="Alta Ansó agosto · Baja Foz",
        interes=["Ansó (pueblo más bonito de España)","Traje típico ansotano","Foz de Biniés (gargantas kársticas)","Monasterio de Leyre"],
        historia=(
            "<strong>Ansó</strong> está reconocido como uno de los <strong>pueblos más bonitos de España</strong>: "
            "callejuelas empedradas, casas de piedra con escudos nobiliarios y el <strong>traje típico ansotano</strong>, "
            "uno de los más llamativos de la Península — las mujeres solteras llevaban la toca hacia adelante, "
            "las casadas hacia atrás. El pueblo estuvo aislado durante siglos y desarrolló una cultura propia, "
            "con museo etnológico en la iglesia de San Pedro. "
            "La <strong>Foz de Biniés</strong> es un cañón kárstico excavado por el río Veral, accesible por "
            "pasarela de madera sin desnivel. "
            "(Ciudadela de Jaca es plan C en D3 si nublado; no hace falta volver a Jaca antes de Yesa.)"
        ),
        observaciones=(
            "Día de transición fresco (~23°C sensación). "
            "🏘️ Mañana: parada en <strong>Ansó</strong> (~18 km · ~30 min desde Borda Bisaltico) — paseo por el casco "
            "medieval, museo etnológico, tiendas de artesanía. 1-1,5 h. "
            "Foz de Biniés después (~23 km · ~1h05 desde Ansó; pasarela fácil, 1,5 h, perros OK). "
            "Luego directo a Artieda/Yesa (~25 km · ~40 min) — sin desvío a Jaca (ahorra ~80 km). "
            "📍 Pernocta preferida: P4N #82683 Artieda (borde río, plano, 10 plazas) "
            "⚠️ ACCESO JUSTO para 7m: camino pedregoso estrecho — ver el camino andando primero. "
            "Legalidad Artieda: reviews contradictorios (GC multó a uno, otros sin problema). "
            "📍 Alternativa A: P4N #26522 Monasterio Leyre (acceso fácil, inclinado, no shade). "
            "📍 Alternativa B: P4N #552933 Yesa río (solo 2 plazas, mosquitos+++, ramas bajas)."
        ),
        planb="Ansó bajo cubierto: museo etnológico · café pueblo · Foz corta si llueve.",
    ),
    dict(
        day=6, date="2026-08-22",
        zona="Ochagavía · Valle de Salazar",
        # Pernocta: fuera del casco medieval (la camper no cabe dentro)
        parking_name="Borde río Zatoia / salida norte Ochagavía (fuera casco)",
        parking_lat=42.908, parking_lon=-1.082,
        drive_from="Artieda/Yesa → Ochagavía", drive_km="~60 km", drive_h="~1h05",
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
            "⚠️ Tormenta posible (~19 mm) — acortar Zatoia si truena; casco + queso bajo cubierta. "
            "Avituallamiento: supermercado en Ochagavía. Queso Roncal: comprar aquí."
        ),
        planb="Casco medieval Ochagavía · tiendas de queso Roncal · paseo río bajo la lluvia.",
    ),
    dict(
        day=7, date="2026-08-23",
        zona="Selva de Irati · Embalse Irabia",
        # Pernocta: Casas de Irati / área de aparcamiento Irabia
        parking_name="Casas de Irati · Área Irabia (fin de pista forestal asfaltada)",
        parking_lat=42.929, parking_lon=-1.015,
        drive_from="Ochagavía → Irabia (pista forestal ancha)", drive_km="~8 km", drive_h="~17 min",
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
            "La pista forestal Ochagavía → Irabia es amplia (~8 km · ~17 min; OK para Sunlight 600). "
            "El hike circular empieza y termina en el mismo parking donde dormís. "
            "⚠️ Tormenta fuerte posible (~43 mm) — el hayedo aguanta bien la lluvia; evitar crestas/Abodi. "
            "Entrar pronto (antes de 9h). Perros con correa — ZEPA sensible para urogallo. "
            "Agua: río Irati cristalino y frío."
        ),
        planb="Paseo borde embalse Irabia bajo lluvia (el hayedo con niebla es impresionante).",
    ),
    dict(
        day=8, date="2026-08-24",
        zona="Orbaitzeta · Río Irati interior",
        # Pernocta: norte de Orbaitzeta, borde río Irati (aguas arriba de las ruinas)
        parking_name="Norte Orbaitzeta · borde río Irati (aguas arriba ruinas)",
        parking_lat=42.979, parking_lon=-1.231,
        drive_from="Irabia → Orbaitzeta (pista / carreteras locales)", drive_km="~40 km", drive_h="~50 min",
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
            "⚠️ Día cálido (~29°C sensación) — hike AM temprano o bajo hayedo. "
            "Traslado Irabia → Orbaitzeta ~40 km · ~50 min. "
            "Plan A: senda río Irati aguas arriba + ruinas Orbaitzeta. "
            "Plan B (calor/lluvia): las ruinas están bajo hayedo denso — visita perfecta con sombra. "
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
        drive_from="Orbaitzeta → Isaba", drive_km="~57 km", drive_h="~1h05",
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
            "Último día en Navarra · traslado ~57 km · ~1h05. "
            "⚠️ Tormenta/granizo posible (~23 mm) — Senda del Esca corta si empeora. "
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
        drive_from="Isaba → Teià", drive_km="~412 km", drive_h="~5h20",
        hike="—", hike_lat=None, hike_lon=None,
        hike_km="—", hike_dif="—", hike_desn="—", hike_h="—",
        hike_parking="",
        concurrencia="—",
        interes=["Parada sombra cada 2 h","AC para perras","Evitar parar sin sombra"],
        historia="",
        observaciones=(
            "Salir antes de las 8:00 para evitar el calor de costa. "
            "Costa mediterránea en agosto: sensación ~30°C — interior camper 35°C+ al sol. "
            "Paradas solo en áreas de servicio con sombra o gasolineras con zona arbolada. "
            "AC encendido para las perras. Ruta: Pamplona → Zaragoza → Lleida → Barcelona. "
            "Total ~412 km · ~5h20 (OSRM; sumad paradas)."
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
    if n==2: return gmaps_dir(*SPOT1,*CANDANCHU)  # Astún overnight → Candanchú (tras Búnkeres)
    if n==3: return gmaps_dir(*ANGLASE,*ARREBOL)  # post-hike Anglasé → El Arrebol
    if n==4: return gmaps_dir(*ARREBOL,*BORDA)  # El Arrebol → Borda Bisaltico
    if n==5: return gmaps_route([BORDA, ANSO, BINIES, ARTIEDA])  # sin desvío a Jaca
    if n==6: return gmaps_dir(*ARTIEDA,*OCH)
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
        th_row = ""
        if d.get("hike_from_overnight") and d["hike"] != "—":
            th_row = f'<div class="row"><b>Al trail</b><span style="font-size:.78rem">{esc(d["hike_from_overnight"])}</span></div>\n'
        star = " ⭐" if n == 4 else ""
        night_link = d["camping_url"] if d.get("camping_url") else p4n_url_for(d)
        night_label = "Web Camping" if d.get("camping_url") else ("Ficha P4N" if d.get("p4n_id") else "P4N zona")
        cards.append(f"""<article class="sum-card">
<div class="k"><a href="#d{n}">D{n}{star}</a></div>
<h3>{fmt_date(d["date"])} · {esc(d["zona"])}</h3>
<div class="row"><b>Km</b><span>{esc(d["drive_km"])} · {esc(d["drive_h"])}</span></div>
<div class="row"><b>Pernocta</b><span>{esc(d["parking_name"])}</span></div>
<div class="row"><b>Hike</b><span>{hike_html}</span></div>
{th_row}<div class="row"><b>Gente</b><span>{crowd_span(d["concurrencia"])}</span></div>
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
        ruta_html = (f"<p>🥾 Búnkeres desde Canfranc Estación (~9 km · 10 min del overnight Candanchú). "
                     f"Tras el hike: subir a P4N #532128 Candanchú (1.520 m).</p>"
                     f"{btns([('Canfranc Estación → Candanchú (conducir)', gmaps_dir(-0.525,42.750,*CANDANCHU), 'g')])}")
    elif n==3:
        d3_btns = btns([
            ("Candanchú → Anglasé", gmaps_dir(*CANDANCHU, *ANGLASE), "g"),
            ("Anglasé → El Arrebol", gmaps_dir(*ANGLASE, *ARREBOL), "g"),
            ("El Arrebol → Pozas Garcipollera", gmaps_dir(*ARREBOL, *GARCIPOLLERA), "g"),
            ("El Arrebol → Puente San Miguel", gmaps_dir(*ARREBOL, *SAN_MIGUEL), "g"),
        ])
        ruta_html = (
            "<p>🥾 AM: Canal Roya desde Parking Anglasé (~6 km · 8 min desde Candanchú). "
            "Tras el hike: Anglasé → El Arrebol (~27 km · ~27 min) — check-in y comida. "
            "💧 PM fresco: <strong>Pozas Garcipollera</strong> (~9 km · ~9 min, agua helada + sombra). "
            "Plan B: Puente San Miguel (~5 km · ~8 min). "
            "Noche: piscina perros El Arrebol (~20-21h).</p>"
            + d3_btns
        )
    elif n==4:
        ruta_html = (f"<p>El Arrebol → Camping Borda Bisaltico vía Hecho (~52 km, ~1 h). "
                     f"Jue 20 fresco (~22°C) — <strong>día estrella</strong> Aguas Tuertas.</p>"
                     f"{btns([('El Arrebol → Borda Bisaltico (conducir)', gmaps_dir(*ARREBOL,*BORDA), 'g')])}")
    elif n==5:
        d5_btns = btns([
            ('Borda Bisaltico → Ansó', gmaps_dir(*BORDA,*ANSO), 'g'),
            ('Ansó → Foz Biniés', gmaps_dir(*ANSO,*BINIES), 'g'),
            ('Foz Biniés → Artieda', gmaps_dir(*BINIES,*ARTIEDA), 'g'),
        ])
        ruta_html = (f"<p>Borda → Ansó (pueblo) → Foz de Biniés → Artieda/Yesa (~68 km · ~2h35; sin desvío a Jaca).</p>"
                     f"{d5_btns}")
    elif n==6:
        ruta_html = (f"<p>Artieda/Yesa → Ochagavía (~60 km, ~1h05). Entrada al Pirineo navarro.</p>"
                     f"{btns([('Artieda → Ochagavía (conducir)', gmaps_dir(*ARTIEDA,*OCH), 'g')])}")
    elif n==7:
        ruta_html = (f"<p>Mover camper Ochagavía → Casas de Irati/Irabia (~8 km · ~17 min, pista ancha OK Sunlight 600).</p>"
                     f"{btns([('Ochagavía → Casas de Irati (conducir)', gmaps_dir(*OCH,*IRABIA), 'g')])}")
    elif n==8:
        ruta_html = (f"<p>Irabia → Orbaitzeta (~40 km · ~50 min).</p>"
                     f"{btns([('Irabia → Orbaitzeta (conducir)', gmaps_dir(*IRABIA,*ORBA_NIGHT), 'g')])}")
    elif n==9:
        ruta_html = (f"<p>Orbaitzeta → Isaba (~57 km · ~1h05). Último cambio de base.</p>"
                     f"{btns([('Orbaitzeta → Isaba (conducir)', gmaps_dir(*ORBA_NIGHT,*ISA), 'g')])}")
    elif n==10:
        ruta_html = (f"<p><strong>Vuelta a casa.</strong> ~412 km · ~5h20. Salir antes de las 8:00.</p>"
                     f"{btns([('Isaba → Teià (conducir)', gmaps_dir(*ISA,*TEIA), 'g')])}")
    else:
        ruta_html = "<p>Sin traslado — misma base.</p>"

    # parking section
    if d.get("camping_url"):
        n_day = d["day"]
        if n_day == 3:
            # El Arrebol: piscina perros, reserva confirmada
            camping_btns = btns([
                ("Conducir aquí (Google)", gmaps_pin(d["parking_lat"], d["parking_lon"]), "g"),
                ("Web El Arrebol", d["camping_url"], "o"),
                ("Reserva confirmada", d["camping_booking"], "p"),
            ])
            camp_desc = "Perros sin suplemento · 2 perras gratis · piscina perros · restaurante pet-friendly"
            camp_badge = '<span style="background:#d4edda;color:#155724;font-size:.72rem;font-weight:700;padding:.2rem .5rem;border-radius:999px">🐾 El Arrebol · piscina perros · reserva #109671</span>'
        else:
            # Borda Bisaltico: sin reservas, llamar antes
            p4n_backup_btn = (f'\n{btn("🆘 Plan B: P4N #227980", p4n_place(d["p4n_backup"]), "o")}' if d.get("p4n_backup") else "")
            camping_btns = btns([
                ("Conducir aquí (Google)", gmaps_pin(d["parking_lat"], d["parking_lon"]), "g"),
                ("Web Borda Bisaltico", d["camping_url"], "o"),
                ("Contacto / ¿Queda plaza?", d["camping_booking"], "p"),
            ]) + p4n_backup_btn
            camp_desc = "Sin reservas · llamar 3 días antes: 974 34 89 40 / 696 981 816 · check-in desde 12h · perros OK"
            camp_badge = '<span style="background:#d4edda;color:#155724;font-size:.72rem;font-weight:700;padding:.2rem .5rem;border-radius:999px">🏕️ Borda Bisaltico · sin reserva · perros OK</span>'
        parking_html = f"""<div class="spot"><strong>{esc(d['parking_name'])}</strong>
{camp_badge}
<p style="margin:.25rem 0;font-size:.82rem;color:var(--muted)">{camp_desc}</p>
{camping_btns}</div>"""
    else:
        alts_html = ""
        if d.get("p4n_alts"):
            alt_btns = "".join(
                f'<div style="margin-top:.3rem">{btn(f"🔁 {label}", p4n_place(pid), "o")}'
                f'{btn("🗺️ Nav", gmaps_pin(lat,lon), "g")}</div>'
                for pid, label, lat, lon in d["p4n_alts"]
            )
            alts_html = f'<div style="margin-top:.5rem;font-size:.78rem;color:var(--muted)">Alternativas si no hay sitio:</div>{alt_btns}'
        parking_html = f"""<div class="spot"><strong>{esc(d['parking_name'])}</strong>
<p style="margin:.25rem 0;font-size:.82rem;color:var(--muted)">Navegación en coche al parking (no pin suelto).</p>
{btn("Conducir aquí (Google)", gmaps_pin(d['parking_lat'],d['parking_lon']), "g")}
{btn("Ficha P4N" if d.get("p4n_id") else "P4N zona", p4n_url_for(d), "o")}{alts_html}</div>"""

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
        wl_btn = (f'\n{btn("📍 Ruta oficial · GR-11 Canal Roya" if "senderistos" in d["wikiloc_url"] or "senderosturisticos" in d["wikiloc_url"] else "📍 Wikiloc · ruta completa", d["wikiloc_url"], "o")}' if d.get("wikiloc_url") else "")
        hike_html = f"""<p><strong>{esc(d['hike'])}</strong> · {dif_badge(d['hike_dif'])} · \
{esc(d['hike_km'])} · {esc(d['hike_desn'])} desnivel · {esc(d['hike_h'])}</p>
{th_note}
{btns([('🗺️ Navegar al trailhead (Google)', gmaps_pin(hlat, hlon), 'g')])}{wl_btn}
<p style="font-size:.75rem;color:var(--muted)">Confirmar ruta en Wikiloc/AllTrails antes del hike.</p>"""

    # POIs
    poi_html = ", ".join(f"<strong>{esc(p)}</strong>" for p in d["interes"]) if d["interes"] else "—"

    # historia
    hist_html = f"<p>{d['historia']}</p>" if d["historia"] else ""

    # concurrencia
    obs_html = f"<p>{d['observaciones']}</p>" if d["observaciones"] else ""
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
<a class="btn" href="#opcionales">+ Excursiones</a>
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

<section class="section" id="opcionales">
<h2>🗺️ Excursiones opcionales (fuera del eje principal)</h2>
<div class="warn">
Estos sitios están a 60–100 km del eje Jaca–Hecho–Ansó–Navarra y no encajan en los tramos ≤2h
sin sacrificar un día ya reservado (El Arrebol, Borda Bisaltico, Aguas Tuertas). Se documentan
aquí por si os sobra un día o preferís sustituir alguno de los días fijos.
</div>

<div class="card">
<h3 style="margin-top:0;color:var(--pine)">Valle de Tena (Panticosa · Sallent · Lanuza)</h3>
<p style="font-size:.85rem;color:var(--muted)">Desde Jaca: ~59 km · ~55 min por Biescas</p>
<div class="spot"><strong>Balneario y Pasarelas de Panticosa</strong>
<p style="margin:.25rem 0;font-size:.85rem">Pasarelas de madera sobre el río Caldarés, cascadas encajonadas. Entrada ~4€/persona. Fácil, corto, perros OK.</p></div>
<div class="spot"><strong>Ibón de Piedrafita</strong>
<p style="margin:.25rem 0;font-size:.85rem">Lago accesible junto a la carretera, con el Bosque del Betato alrededor. Paseo fácil, ideal para parada corta con perras.</p></div>
<div class="spot"><strong>Sallent de Gállego y Lanuza</strong>
<p style="margin:.25rem 0;font-size:.85rem">Sallent: casco medieval con puente sobre el Gállego. Lanuza: pueblo reconstruido junto al embalse, muy fotogénico pero pequeño — 20-30 min de visita basta.</p></div>
{btns([("Cómo llegar desde Jaca", gmaps_dir(*JACA, -0.317, 42.831), "g")])}
<p style="font-size:.78rem;color:var(--muted)">Para incorporarlo: sustituiría el día de Canal Roya (D3) o requeriría un día extra de viaje.</p>
</div>

<div class="card">
<h3 style="color:var(--pine)">Sobrarbe (Aínsa · Boltaña · Broto · Cañón de Añisclo)</h3>
<p style="font-size:.85rem;color:var(--muted)">Desde Jaca: ~80 km / ~1h20 hasta Aínsa (Boltaña y Broto muy cerca)</p>
<div class="spot"><strong>Aínsa</strong>
<p style="margin:.25rem 0;font-size:.85rem">Casco medieval amurallado, plaza porticada de piedra, una de las villas mejor conservadas del Pirineo. Mirador sobre la confluencia Cinca-Ara.</p></div>
<div class="spot"><strong>Broto</strong>
<p style="margin:.25rem 0;font-size:.85rem">Pueblo de piedra a la entrada de Ordesa, buena opción para comer — varios restaurantes con terraza junto al río Ara.</p></div>
<div class="spot"><strong>Ruta circular de San Úrbez (Cañón de Añisclo)</strong>
<p style="margin:.25rem 0;font-size:.85rem">~2 km · ~30 m desnivel · Fácil · 45 min–1h. Ermita rupestre s.VIII, puente románico, Cascada del Aso. "Cañones espectaculares" — dentro del Parque Nacional de Ordesa, perros con correa obligatoria. Parking pequeño en temporada alta.</p></div>
<div class="spot"><strong>Boltaña</strong>
<p style="margin:.25rem 0;font-size:.85rem">Cocapital del Sobrarbe junto a Aínsa, casco antiguo sobre el río Ara.</p></div>
{btns([("Cómo llegar desde Jaca", gmaps_dir(*JACA, 0.135, 42.416), "g")])}
<p style="font-size:.78rem;color:var(--muted)">Para incorporarlo: día completo dedicado (ida+vuelta desde Jaca ~160 km) o pernocta en la zona, sustituyendo un día del tramo navarro.</p>
</div>
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
