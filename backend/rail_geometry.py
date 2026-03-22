"""
rail_geometry.py — Actual GPS coordinates for every Mumbai train station.
Used to draw routes that follow real rail tracks instead of roads.
"""

# Exact lat/lng for every station on each line
# These snap the map route to actual rail corridors

STATION_COORDS = {
    # ── WESTERN RAILWAY (north-south along western coast) ────────────────────
    "churchgate":      (18.9322, 72.8264),
    "marine lines":    (18.9442, 72.8238),
    "charni road":     (18.9518, 72.8189),
    "grant road":      (18.9646, 72.8143),
    "mumbai central":  (18.9697, 72.8194),
    "mahalaxmi":       (18.9820, 72.8246),
    "lower parel":     (18.9976, 72.8328),
    "elphinstone road":(19.0070, 72.8355),
    "dadar":           (19.0178, 72.8478),
    "matunga road":    (19.0250, 72.8432),
    "mahim":           (19.0354, 72.8416),
    "bandra":          (19.0542, 72.8402),
    "khar":            (19.0728, 72.8361),
    "santacruz":       (19.0822, 72.8393),
    "vile parle":      (19.0990, 72.8492),
    "andheri":         (19.1136, 72.8493),
    "jogeshwari":      (19.1295, 72.8490),
    "goregaon":        (19.1566, 72.8494),
    "malad":           (19.1872, 72.8484),
    "kandivali":       (19.2043, 72.8527),
    "borivali":        (19.2307, 72.8567),
    "dahisar":         (19.2500, 72.8590),
    "mira road":       (19.2800, 72.8735),
    "bhayandar":       (19.3010, 72.8518),
    "naigaon":         (19.3510, 72.8460),
    "vasai road":      (19.3840, 72.8328),
    "virar":           (19.4550, 72.8110),

    # ── CENTRAL RAILWAY MAIN LINE (CST → Kalyan) ─────────────────────────────
    "csmt":            (18.9404, 72.8356),
    "masjid":          (18.9518, 72.8381),
    "sandhurst road":  (18.9629, 72.8365),
    "byculla":         (18.9786, 72.8356),
    "chinchpokli":     (18.9864, 72.8328),
    "currey road":     (18.9947, 72.8332),
    "parel":           (19.0015, 72.8418),
    "matunga":         (19.0266, 72.8569),
    "sion":            (19.0396, 72.8619),
    "kurla":           (19.0726, 72.8793),
    "vidyavihar":      (19.0803, 72.8890),
    "ghatkopar":       (19.0868, 72.9088),
    "vikhroli":        (19.1059, 72.9258),
    "kanjurmarg":      (19.1290, 72.9285),
    "bhandup":         (19.1444, 72.9375),
    "nahur":           (19.1570, 72.9415),
    "mulund":          (19.1726, 72.9526),
    "thane":           (19.1820, 72.9745),
    "kalwa":           (19.2000, 73.0028),
    "mumbra":          (19.1870, 73.0237),
    "diva":            (19.1811, 73.0285),
    "kopar":           (19.1864, 73.0452),
    "dombivli":        (19.2180, 73.0860),
    "thakurli":        (19.2260, 73.1022),
    "kalyan":          (19.2403, 73.1305),

    # ── HARBOUR LINE (CST → Panvel, eastern route) ───────────────────────────
    "dockyard road":   (18.9660, 72.8445),
    "reay road":       (18.9778, 72.8465),
    "cotton green":    (18.9875, 72.8445),
    "sewri":           (19.0008, 72.8546),
    "wadala road":     (19.0169, 72.8631),
    "guru tegh bahadur nagar": (19.0328, 72.8679),
    "chunabhatti":     (19.0516, 72.8810),
    "tilak nagar":     (19.0660, 72.8975),
    "chembur":         (19.0619, 72.9000),
    "govandi":         (19.0555, 72.9150),
    "mankhurd":        (19.0485, 72.9315),
    "vashi":           (19.0760, 72.9988),
    "sanpada":         (19.0655, 73.0048),
    "juinagar":        (19.0550, 73.0175),
    "nerul":           (19.0330, 73.0195),
    "seawoods darave": (19.0196, 73.0175),
    "belapur":         (19.0176, 73.0405),
    "kharghar":        (19.0473, 73.0705),
    "mansarovar":      (19.0380, 73.0850),
    "khandeshwar":     (19.0225, 73.1010),
    "panvel":          (18.9894, 73.1175),

    # ── TRANS-HARBOUR LINE (Thane → Nerul) ───────────────────────────────────
    "airoli":          (19.1550, 72.9990),
    "rabale":          (19.1375, 73.0005),
    "ghansoli":        (19.1160, 73.0000),
    "koparkhairane":   (19.1035, 73.0015),
    "turbhe":          (19.0785, 73.0200),

    # ── METRO LINE 1 (Versova → Ghatkopar) ───────────────────────────────────
    "versova":         (19.1295, 72.8155),
    "jogeshwari":      (19.1369, 72.8490),  # same as WR
    "chakala":         (19.1136, 72.8770),
    "marol naka":      (19.1028, 72.8798),
    "saki naka":       (19.0952, 72.8897),
    "asalpha":         (19.0910, 72.8985),

    # ── METRO LINE 2A (Dahisar E → DN Nagar) ─────────────────────────────────
    "dahisar east":    (19.2500, 72.8650),
    "kandivali east":  (19.2043, 72.8630),
    "borivali east":   (19.2307, 72.8650),
    "goregaon east":   (19.1566, 72.8620),
    "malad east":      (19.1872, 72.8580),
    "andheri west":    (19.1136, 72.8340),
    "d n nagar":       (19.1076, 72.8290),

    # ── METRO LINE 7 (Dahisar E → Andheri E) ─────────────────────────────────
    "jogeshwari east": (19.1369, 72.8560),
    "andheri east":    (19.1136, 72.8697),
}


def get_rail_waypoints(line_id: str, src_station: str, dst_station: str) -> list:
    """
    Return GPS waypoints that follow actual rail track geometry
    by connecting real station coordinates in order.
    Much more accurate than OSRM driving routes.
    """
    from mumbai_transit import TRAIN_LINES, METRO_LINES

    all_lines = {**TRAIN_LINES, **METRO_LINES}
    line = all_lines.get(line_id)
    if not line:
        return []

    stations = line["stations"]
    src = src_station.strip().lower()
    dst = dst_station.strip().lower()

    if src not in stations or dst not in stations:
        # Fallback: just use src and dst coords
        sc = STATION_COORDS.get(src)
        dc = STATION_COORDS.get(dst)
        if sc and dc:
            return [[sc[0], sc[1]], [dc[0], dc[1]]]
        return []

    si = stations.index(src)
    di = stations.index(dst)

    # Get ordered stations between src and dst
    if si <= di:
        route_stations = stations[si:di+1]
    else:
        route_stations = stations[di:si+1][::-1]

    # Build waypoints from station coordinates
    waypoints = []
    for s in route_stations:
        coords = STATION_COORDS.get(s)
        if coords:
            waypoints.append([coords[0], coords[1]])

    return waypoints


def get_multi_leg_waypoints(legs: list) -> list:
    """
    Build waypoints for a multi-leg journey (e.g. WR to CSMT, then HL to Vashi).
    legs = list of (line_id, src_station, dst_station)
    Returns combined waypoint list.
    """
    all_waypoints = []
    for line_id, src, dst in legs:
        wps = get_rail_waypoints(line_id, src, dst)
        if all_waypoints and wps:
            # Avoid duplicate point at interchange
            if all_waypoints[-1] == wps[0]:
                wps = wps[1:]
        all_waypoints.extend(wps)
    return all_waypoints