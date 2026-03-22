"""
utils.py — Route generation with real geocoding and OSRM road routing.
"""

import random
import math
import urllib.request
import urllib.parse
import json
from datetime import datetime

CITY_BOUNDS = {
    "lat_min": 18.89, "lat_max": 19.25,
    "lng_min": 72.77, "lng_max": 72.99,
}

TRANSPORT_MODES = {
    "metro": {"speed_kmh": 40, "crowding_base": 55, "reliability": 0.88},
    "bus":   {"speed_kmh": 18, "crowding_base": 65, "reliability": 0.72},
    "walk":  {"speed_kmh":  5, "crowding_base":  5, "reliability": 0.99},
    "bike":  {"speed_kmh": 15, "crowding_base":  8, "reliability": 0.93},
    "auto":  {"speed_kmh": 22, "crowding_base": 20, "reliability": 0.80},
}

MUMBAI_LOCATIONS = {
    "csmt": (18.9398, 72.8355),
    "cst": (18.9398, 72.8355),
    "chhatrapati shivaji terminus": (18.9398, 72.8355),
    "victoria terminus": (18.9398, 72.8355),
    "masjid": (18.9518, 72.8381),
    "sandhurst road": (18.9629, 72.8365),
    "byculla": (18.9762, 72.8331),
    "chinchpokli": (18.9864, 72.8328),
    "currey road": (18.9947, 72.8332),
    "parel": (19.0027, 72.8420),
    "dadar": (19.0178, 72.8478),
    "matunga": (19.0266, 72.8569),
    "sion": (19.0396, 72.8619),
    "kurla": (19.0726, 72.8793),
    "vidyavihar": (19.0803, 72.8890),
    "ghatkopar": (19.0868, 72.9088),
    "vikhroli": (19.1059, 72.9258),
    "kanjurmarg": (19.1290, 72.9285),
    "bhandup": (19.1444, 72.9375),
    "nahur": (19.1570, 72.9415),
    "mulund": (19.1726, 73.0326),
    "thane": (19.2183, 72.9781),
    "kalwa": (19.2334, 72.9957),
    "mumbra": (19.1870, 73.0237),
    "kopar": (19.1864, 73.0452),
    "dombivli": (19.2180, 73.0860),
    "thakurli": (19.2260, 73.1022),
    "kalyan": (19.2403, 73.1305),
    "churchgate": (18.9322, 72.8264),
    "marine lines": (18.9442, 72.8238),
    "charni road": (18.9518, 72.8189),
    "grant road": (18.9646, 72.8143),
    "mumbai central": (18.9697, 72.8194),
    "mahalaxmi": (18.9820, 72.8246),
    "lower parel": (18.9976, 72.8328),
    "elphinstone road": (19.0070, 72.8355),
    "prabhadevi": (19.0166, 72.8295),
    "dadar west": (19.0178, 72.8420),
    "matunga road": (19.0250, 72.8432),
    "mahim": (19.0354, 72.8416),
    "bandra": (19.0596, 72.8295),
    "bandra west": (19.0596, 72.8255),
    "bandra east": (19.0596, 72.8395),
    "khar": (19.0728, 72.8361),
    "santacruz": (19.0822, 72.8393),
    "vile parle": (19.0990, 72.8492),
    "andheri": (19.1136, 72.8697),
    "andheri west": (19.1136, 72.8557),
    "andheri east": (19.1136, 72.8797),
    "jogeshwari": (19.1369, 72.8490),
    "goregaon": (19.1663, 72.8526),
    "malad": (19.1872, 72.8484),
    "kandivali": (19.2043, 72.8527),
    "borivali": (19.2307, 72.8567),
    "dahisar": (19.2500, 72.8590),
    "mira road": (19.2800, 72.8735),
    "bhayandar": (19.3010, 72.8518),
    "naigaon": (19.3510, 72.8460),
    "vasai road": (19.3840, 72.8328),
    "virar": (19.4550, 72.8110),
    "dockyard road": (18.9660, 72.8445),
    "reay road": (18.9778, 72.8465),
    "cotton green": (18.9875, 72.8445),
    "sewri": (19.0008, 72.8546),
    "wadala road": (19.0169, 72.8631),
    "guru tegh bahadur nagar": (19.0328, 72.8679),
    "chunabhatti": (19.0516, 72.8810),
    "tilak nagar": (19.0660, 72.8975),
    "chembur": (19.0626, 72.9005),
    "govandi": (19.0555, 72.9150),
    "mankhurd": (19.0485, 72.9315),
    "vashi": (19.0760, 72.9986),
    "sanpada": (19.0655, 73.0048),
    "juinagar": (19.0550, 73.0175),
    "nerul": (19.0330, 73.0195),
    "seawoods darave": (19.0196, 73.0175),
    "belapur": (19.0176, 73.0405),
    "kharghar": (19.0473, 73.0705),
    "mansarovar": (19.0380, 73.0850),
    "khandeshwar": (19.0225, 73.1010),
    "panvel": (18.9894, 73.1175),
    "airoli": (19.1550, 72.9990),
    "rabale": (19.1375, 73.0005),
    "ghansoli": (19.1160, 73.0000),
    "koparkhairane": (19.1035, 73.0015),
    "turbhe": (19.0785, 73.0200),
    "powai": (19.1176, 72.9060),
    "colaba": (18.9067, 72.8147),
    "versova": (19.1295, 72.8155),
    "bkc": (19.0658, 72.8652),
    "bandra kurla complex": (19.0658, 72.8652),
    "juhu": (19.1075, 72.8263),
    "lokhandwala": (19.1357, 72.8274),
    "navi mumbai": (19.0330, 73.0297),
    "fort": (18.9340, 72.8356),
    "nariman point": (18.9256, 72.8242),
    "worli": (19.0048, 72.8175),
    "wadala": (18.9986, 72.8579),
    "dharavi": (19.0376, 72.8562),
    "film city": (19.1573, 72.8776),
}

# All Mumbai congestion hotspots — used by heatmap
ALL_HOTSPOTS = [
    (18.9398, 72.8355, 0.95),  # CST
    (18.9322, 72.8264, 0.90),  # Churchgate
    (19.0178, 72.8478, 0.92),  # Dadar
    (19.0726, 72.8793, 0.88),  # Kurla
    (19.2183, 72.9781, 0.85),  # Thane
    (19.2403, 73.1305, 0.82),  # Kalyan
    (19.0596, 72.8295, 0.82),  # Bandra
    (19.0822, 72.8393, 0.75),  # Santacruz
    (19.0990, 72.8492, 0.75),  # Vile Parle
    (19.1136, 72.8697, 0.85),  # Andheri
    (19.1369, 72.8490, 0.72),  # Jogeshwari
    (19.1663, 72.8526, 0.70),  # Goregaon
    (19.1872, 72.8484, 0.68),  # Malad
    (19.2043, 72.8527, 0.65),  # Kandivali
    (19.2307, 72.8567, 0.70),  # Borivali
    (19.0868, 72.9088, 0.78),  # Ghatkopar
    (19.1059, 72.9258, 0.68),  # Vikhroli
    (19.1290, 72.9285, 0.66),  # Kanjurmarg
    (19.1444, 72.9375, 0.65),  # Bhandup
    (19.1726, 73.0326, 0.68),  # Mulund
    (18.9976, 72.8328, 0.78),  # Lower Parel
    (19.0027, 72.8420, 0.75),  # Parel
    (19.0070, 72.8355, 0.72),  # Elphinstone
    (19.0396, 72.8619, 0.70),  # Sion
    (19.0626, 72.9005, 0.70),  # Chembur
    (19.0555, 72.9150, 0.65),  # Govandi
    (19.0485, 72.9315, 0.68),  # Mankhurd
    (19.0760, 72.9988, 0.78),  # Vashi
    (19.0655, 73.0048, 0.70),  # Sanpada
    (19.0330, 73.0195, 0.72),  # Nerul
    (19.0176, 73.0405, 0.70),  # Belapur
    (19.0473, 73.0705, 0.65),  # Kharghar
    (18.9894, 73.1175, 0.68),  # Panvel
    (19.1550, 72.9990, 0.65),  # Airoli
    (19.0785, 73.0200, 0.70),  # Turbhe
    (19.0658, 72.8652, 0.80),  # BKC
    (19.1176, 72.9060, 0.75),  # Powai
    (18.9067, 72.8147, 0.72),  # Colaba
]

_geocode_cache = {}


def geocode(location: str) -> tuple:
    """Geocode a location — Mumbai table first, then Nominatim India-only."""
    key = location.strip().lower()

    if key in _geocode_cache:
        print(f"[Geocode] '{location}' → cache hit")
        return _geocode_cache[key]

    if key in MUMBAI_LOCATIONS:
        result = MUMBAI_LOCATIONS[key]
        _geocode_cache[key] = result
        print(f"[Geocode] '{location}' → {result} (lookup table)")
        return result

    try:
        params = urllib.parse.urlencode({
            "q": location,
            "format": "json",
            "limit": "1",
            "countrycodes": "in",
        })
        url = f"https://nominatim.openstreetmap.org/search?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "CommuteIQ/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
            if data:
                result = (float(data[0]["lat"]), float(data[0]["lon"]))
                _geocode_cache[key] = result
                print(f"[Geocode] '{location}' → {result} (nominatim)")
                return result
    except Exception as e:
        print(f"[Geocode] Nominatim failed for '{location}': {e}")

    result = (19.0760, 72.8777)
    _geocode_cache[key] = result
    print(f"[Geocode] '{location}' → Mumbai center fallback")
    return result


def get_real_route(src_lat, src_lng, dst_lat, dst_lng, profile="driving") -> dict:
    """Fetch real road route from OSRM public API."""
    url = (
        f"https://router.project-osrm.org/route/v1/{profile}/"
        f"{src_lng},{src_lat};{dst_lng},{dst_lat}"
        f"?overview=full&geometries=geojson&steps=false"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CommuteIQ/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                coords = route["geometry"]["coordinates"]
                waypoints = [[c[1], c[0]] for c in coords]
                distance_km = round(route["distance"] / 1000, 2)
                duration_min = round(route["duration"] / 60, 1)
                print(f"[OSRM] {profile}: {distance_km}km, {duration_min}min, {len(waypoints)} points")
                if distance_km > 200:
                    print(f"[OSRM] Rejected — {distance_km}km too large")
                    return None
                return {
                    "waypoints": waypoints,
                    "distance_km": distance_km,
                    "duration_min": duration_min,
                }
    except Exception as e:
        print(f"[OSRM] Failed ({profile}): {e}")
    return None


def haversine_distance(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _is_peak_hour(hour: int) -> bool:
    return (8 <= hour <= 10) or (17 <= hour <= 19)


def generate_routes(source: str, destination: str, time_str: str, preference: str) -> list:
    from ml_engine import predict_route

    # Geocode once each
    src_lat, src_lng = geocode(source)
    dst_lat, dst_lng = geocode(destination)

    # Sanity check — must be within Mumbai region
    MUMBAI_LAT_RANGE = (18.85, 19.50)
    MUMBAI_LNG_RANGE = (72.75, 73.25)
    if not (MUMBAI_LAT_RANGE[0] <= src_lat <= MUMBAI_LAT_RANGE[1] and
            MUMBAI_LNG_RANGE[0] <= src_lng <= MUMBAI_LNG_RANGE[1]):
        print(f"[WARNING] Source '{source}' outside Mumbai — using center")
        src_lat, src_lng = 19.0760, 72.8777
    if not (MUMBAI_LAT_RANGE[0] <= dst_lat <= MUMBAI_LAT_RANGE[1] and
            MUMBAI_LNG_RANGE[0] <= dst_lng <= MUMBAI_LNG_RANGE[1]):
        print(f"[WARNING] Destination '{destination}' outside Mumbai — using center")
        dst_lat, dst_lng = 19.0760, 72.8777

    straight_km = haversine_distance(src_lat, src_lng, dst_lat, dst_lng)
    print(f"[Routes] {source}({src_lat:.4f},{src_lng:.4f}) → {destination}({dst_lat:.4f},{dst_lng:.4f}) | {straight_km:.2f}km straight")

    try:
        hour = int(time_str.split(":")[0]) if time_str else datetime.now().hour
    except Exception:
        hour = datetime.now().hour

    is_peak = _is_peak_hour(hour)
    day_of_week = datetime.now().weekday()

    route_configs = [
        {"id": "route_1", "name": "Express Metro",  "modes": ["Metro", "Walk"],  "transport_mode": 1, "color": "#6366f1", "profile": "driving"},
        {"id": "route_2", "name": "Bus Route",      "modes": ["Bus",   "Walk"],  "transport_mode": 0, "color": "#10b981", "profile": "driving"},
        {"id": "route_3", "name": "Mixed Transit",  "modes": ["Auto",  "Metro"], "transport_mode": 4, "color": "#f59e0b", "profile": "cycling"},
    ]

    routes = []
    for i, cfg in enumerate(route_configs):
        osrm = get_real_route(src_lat, src_lng, dst_lat, dst_lng, cfg["profile"])

        if osrm:
            distance_km   = osrm["distance_km"]
            osrm_duration = osrm["duration_min"]
            waypoints     = osrm["waypoints"]
        else:
            distance_km   = straight_km * [1.0, 1.15, 1.08][i]
            osrm_duration = None
            n = 8
            waypoints = [
                [src_lat + (dst_lat - src_lat)*j/n,
                 src_lng + (dst_lng - src_lng)*j/n]
                for j in range(n+1)
            ]

        mode_key  = ["bus", "metro", "walk", "bike", "auto"][cfg["transport_mode"]]
        mode_info = TRANSPORT_MODES[mode_key]

        features = {
            "hour":           hour,
            "is_peak":        int(is_peak),
            "distance_km":    distance_km,
            "num_stops":      max(2, int(distance_km * 0.8)),
            "transport_mode": cfg["transport_mode"],
            "weather_score":  random.uniform(0.5, 1.0),
            "day_of_week":    day_of_week,
        }
        prediction  = predict_route(features)
        crowding    = prediction["crowding_pct"]
        delay       = prediction["delay_minutes"]

        if osrm_duration:
            travel_time = int(osrm_duration + delay)
        else:
            travel_time = int((distance_km / mode_info["speed_kmh"]) * 60 + delay)

        confidence = mode_info["reliability"] - (0.05 if is_peak else 0) + random.uniform(-0.05, 0.05)
        confidence = round(max(0.4, min(0.99, confidence)), 2)

        if preference == "least_crowded":
            crowding    *= 0.75
            travel_time  = int(travel_time * 1.1)
        elif preference == "fastest":
            travel_time  = int(travel_time * 0.9)
            crowding    *= 1.1

        routes.append({
            "route_id":         cfg["id"],
            "name":             cfg["name"],
            "modes":            cfg["modes"],
            "travel_time":      max(5, travel_time),
            "distance_km":      round(distance_km, 2),
            "crowding_pct":     round(min(100, max(5, crowding)), 1),
            "delay_minutes":    round(max(0, delay), 1),
            "confidence_score": confidence,
            "color":            cfg["color"],
            "waypoints":        waypoints,
            "source":      {"lat": src_lat, "lng": src_lng, "name": source},
            "destination": {"lat": dst_lat, "lng": dst_lng, "name": destination},
            "disrupted":   False,
            "num_stops":   features["num_stops"],
        })

    if preference == "fastest":
        routes.sort(key=lambda r: r["travel_time"])
    elif preference == "least_crowded":
        routes.sort(key=lambda r: r["crowding_pct"])
    else:
        routes.sort(key=lambda r: r["travel_time"]*0.5 + r["crowding_pct"]*0.3 - r["confidence_score"]*20)

    return routes


def generate_heatmap_data(src_lat=19.076, src_lng=72.877, dst_lat=19.076, dst_lng=72.877) -> list:
    """Generate congestion heatmap — only hotspots within the route bounding box."""
    points = []

    # Bounding box of route + small buffer
    lat_min = min(src_lat, dst_lat) - 0.03
    lat_max = max(src_lat, dst_lat) + 0.03
    lng_min = min(src_lng, dst_lng) - 0.03
    lng_max = max(src_lng, dst_lng) + 0.03

    for lat, lng, intensity in ALL_HOTSPOTS:
        if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
            # Tight cluster of 5 points per hotspot
            for _ in range(5):
                points.append({
                    "lat":       lat + random.uniform(-0.003, 0.003),
                    "lng":       lng + random.uniform(-0.003, 0.003),
                    "intensity": max(0.3, min(1.0, intensity + random.uniform(-0.1, 0.1))),
                })

    # Fallback — if no hotspots in range, show nearest 3
    if len(points) == 0:
        nearest = sorted(ALL_HOTSPOTS,
            key=lambda h: haversine_distance(h[0], h[1], (src_lat+dst_lat)/2, (src_lng+dst_lng)/2))[:3]
        for lat, lng, intensity in nearest:
            for _ in range(5):
                points.append({
                    "lat":       lat + random.uniform(-0.003, 0.003),
                    "lng":       lng + random.uniform(-0.003, 0.003),
                    "intensity": max(0.3, min(1.0, intensity + random.uniform(-0.1, 0.1))),
                })

    # Light congestion along the route corridor
    for i in range(15):
        t = i / 15
        points.append({
            "lat":       src_lat + (dst_lat - src_lat) * t + random.uniform(-0.002, 0.002),
            "lng":       src_lng + (dst_lng - src_lng) * t + random.uniform(-0.002, 0.002),
            "intensity": random.uniform(0.15, 0.30),
        })

    return points


def format_response(data: dict, status: str = "success") -> dict:
    return {
        "status":    status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data":      data,
    }


def generate_routes_with_transit(source: str, destination: str, time_str: str, preference: str) -> list:
    """
    Generate routes using real Mumbai transit database + OSRM road geometry.
    Falls back to generic routes if no transit match found.
    """
    from ml_engine import predict_route
    from mumbai_transit import get_real_transit_routes

    src_lat, src_lng = geocode(source)
    dst_lat, dst_lng = geocode(destination)

    MUMBAI_LAT_RANGE = (18.85, 19.50)
    MUMBAI_LNG_RANGE = (72.75, 73.25)
    if not (MUMBAI_LAT_RANGE[0] <= src_lat <= MUMBAI_LAT_RANGE[1]):
        src_lat, src_lng = 19.0760, 72.8777
    if not (MUMBAI_LAT_RANGE[0] <= dst_lat <= MUMBAI_LAT_RANGE[1]):
        dst_lat, dst_lng = 19.0760, 72.8777

    try:
        hour = int(time_str.split(":")[0]) if time_str else datetime.now().hour
    except Exception:
        hour = datetime.now().hour

    is_peak = _is_peak_hour(hour)
    day_of_week = datetime.now().weekday()
    straight_km = haversine_distance(src_lat, src_lng, dst_lat, dst_lng)

    # Lowercase versions for transit lookup
    src = source.strip().lower()
    dst = destination.strip().lower()

    print(f"[Transit] {source}({src_lat:.4f},{src_lng:.4f}) → {destination}({dst_lat:.4f},{dst_lng:.4f})")

    # Get real transit options
    transit_options = get_real_transit_routes(source, destination, is_peak)

    # OSRM road geometry
    osrm_driving = get_real_route(src_lat, src_lng, dst_lat, dst_lng, "driving")
    osrm_cycling = get_real_route(src_lat, src_lng, dst_lat, dst_lng, "cycling")

    COLORS = ["#6366f1", "#10b981", "#f59e0b", "#ec4899"]
    
    routes = []
    for i, transit in enumerate(transit_options):
        waypoints = []
        distance_km = straight_km * 1.3
        osrm_duration = None

        # Train/Metro: use real rail track geometry
        if transit["type"] in ("direct_train", "interchange", "hybrid"):
            try:
                from rail_geometry import get_rail_waypoints, get_multi_leg_waypoints
                from mumbai_transit import find_station_on_line, TRAIN_LINES, METRO_LINES
                steps = [s for s in transit.get("steps", []) if s["mode"] in ("Local Train", "Metro")]
                all_lines = {**TRAIN_LINES, **METRO_LINES}

                if transit["type"] == "direct_train" and steps:
                    s_from = src
                    s_to = dst
                    src_line_list = find_station_on_line(s_from)
                    dst_line_list = find_station_on_line(s_to)
                    for _, sl_id, _ in src_line_list:
                        for _, dl_id, _ in dst_line_list:
                            if sl_id == dl_id:
                                waypoints = get_rail_waypoints(sl_id, s_from, s_to)
                                break
                        if waypoints:
                            break
                else:
                    legs = []
                    for step in steps:
                        s_from = step["from"].strip().lower()
                        s_to = step["to"].strip().lower()
                        if s_from == s_to:
                            continue
                        from_lines = find_station_on_line(s_from)
                        to_lines = find_station_on_line(s_to)
                        matched = False
                        for _, fl, _ in from_lines:
                            for _, tl, _ in to_lines:
                                if fl == tl:
                                    legs.append((fl, s_from, s_to))
                                    matched = True
                                    break
                            if matched:
                                break
                        if not matched and from_lines:
                            legs.append((from_lines[0][1], s_from, s_to))
                    if legs:
                        waypoints = get_multi_leg_waypoints(legs)
            except Exception as e:
                print(f"[Rail] Geometry error: {e}")

            # Compute track distance from waypoints
            if len(waypoints) >= 2:
                track_dist = sum(
                    haversine_distance(waypoints[j][0], waypoints[j][1],
                                       waypoints[j+1][0], waypoints[j+1][1])
                    for j in range(len(waypoints)-1)
                )
                distance_km = round(track_dist, 2)

        # Bus/Cab: use OSRM road geometry
        if not waypoints and osrm_driving:
            waypoints = osrm_driving["waypoints"]
            distance_km = osrm_driving["distance_km"]
            osrm_duration = osrm_driving["duration_min"]
        elif not waypoints:
            n = 8
            waypoints = [
                [src_lat + (dst_lat - src_lat)*j/n,
                 src_lng + (dst_lng - src_lng)*j/n]
                for j in range(n+1)
            ]

        features = {
            "hour": hour,
            "is_peak": int(is_peak),
            "distance_km": distance_km,
            "num_stops": transit["num_stops"],
            "transport_mode": {"Local Train": 1, "Metro": 1, "Bus": 0, "Auto/Cab": 4}.get(transit["modes"][0], 1),
            "weather_score": random.uniform(0.5, 1.0),
            "day_of_week": day_of_week,
        }

        prediction = predict_route(features)
        crowding = prediction["crowding_pct"]
        delay = prediction["delay_minutes"]

        # Travel time: use OSRM duration adjusted by mode
        if osrm_duration:
            if transit["type"] == "cab_auto":
                travel_time = int(osrm_duration * 1.1 + delay)  # Traffic
            elif transit["type"] == "bus":
                travel_time = int(osrm_duration * 1.4 + delay + transit["frequency_min"] * 0.5)
            else:
                # Train: faster than driving on long routes
                travel_time = int(osrm_duration * 0.85 + delay + transit["frequency_min"] * 0.3)
        else:
            travel_time = int((distance_km / 25) * 60 + delay)

        reliability = {"direct_train": 0.88, "interchange": 0.82, "bus": 0.72, "cab_auto": 0.90}
        confidence = reliability.get(transit["type"], 0.80) + random.uniform(-0.05, 0.05)
        confidence = round(max(0.5, min(0.99, confidence)), 2)

        if preference == "least_crowded":
            crowding *= 0.75
            travel_time = int(travel_time * 1.1)
        elif preference == "fastest":
            travel_time = int(travel_time * 0.9)

        # Build route name from modes
        route_name = " + ".join(transit["modes"])
        if transit["type"] == "interchange":
            route_name = f"{transit['modes'][0]} (via interchange)"

        routes.append({
            "route_id": f"route_{i+1}",
            "name": route_name,
            "modes": transit["modes"],
            "travel_time": max(5, travel_time),
            "distance_km": round(distance_km, 2),
            "crowding_pct": round(min(100, max(5, crowding)), 1),
            "delay_minutes": round(max(0, delay), 1),
            "confidence_score": confidence,
            "color": COLORS[i],
            "waypoints": waypoints,
            "source": {"lat": src_lat, "lng": src_lng, "name": source},
            "destination": {"lat": dst_lat, "lng": dst_lng, "name": destination},
            "disrupted": False,
            "num_stops": transit["num_stops"],
            "transfers": transit["transfers"],
            "steps": transit["steps"],
            "description": transit["description"],
            "frequency_min": transit["frequency_min"],
        })

    if not routes:
        return generate_routes(source, destination, time_str, preference)

    if preference == "fastest":
        routes.sort(key=lambda r: r["travel_time"])
    elif preference == "least_crowded":
        routes.sort(key=lambda r: r["crowding_pct"])
    else:
        routes.sort(key=lambda r: r["travel_time"]*0.5 + r["crowding_pct"]*0.3 - r["confidence_score"]*20)

    return routes

    #cd routes