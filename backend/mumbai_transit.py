"""
mumbai_transit.py — Complete Mumbai transit system.
Covers: Local Trains (WR/CR/HL/THL), Metro (M1/M2A/M7),
BEST/NMMT Buses, and Hybrid routes (Bus+Train, Train+Metro, etc.)
"""

# ── LOCAL TRAIN LINES ─────────────────────────────────────────────────────────

TRAIN_LINES = {
    "western": {
        "name": "Western Railway",
        "short": "WR",
        "color": "#3b82f6",
        "termini": {"south": "churchgate", "north": "virar"},
        "platforms": {
            "churchgate": {"slow": "1/2", "fast": "3/4"},
            "marine lines": {"slow": "1", "fast": "2"},
            "charni road": {"slow": "1", "fast": "2"},
            "grant road": {"slow": "1", "fast": "2"},
            "mumbai central": {"slow": "1/2", "fast": "3/4"},
            "mahalaxmi": {"slow": "1", "fast": "2"},
            "lower parel": {"slow": "1", "fast": "2"},
            "elphinstone road": {"slow": "1", "fast": "2"},
            "dadar": {"slow": "1/2", "fast": "3/4"},
            "matunga road": {"slow": "1", "fast": "2"},
            "mahim": {"slow": "1", "fast": "2"},
            "bandra": {"slow": "1/2", "fast": "3/4"},
            "khar": {"slow": "1", "fast": "2"},
            "santacruz": {"slow": "1", "fast": "2"},
            "vile parle": {"slow": "1", "fast": "2"},
            "andheri": {"slow": "1/2", "fast": "3/4"},
            "jogeshwari": {"slow": "1", "fast": "2"},
            "goregaon": {"slow": "1/2", "fast": "3/4"},
            "malad": {"slow": "1", "fast": "2"},
            "kandivali": {"slow": "1", "fast": "2"},
            "borivali": {"slow": "1/2", "fast": "3/4"},
            "dahisar": {"slow": "1", "fast": "2"},
            "mira road": {"slow": "1", "fast": "2"},
            "bhayandar": {"slow": "1", "fast": "2"},
            "naigaon": {"slow": "1", "fast": "2"},
            "vasai road": {"slow": "1/2", "fast": "3/4"},
            "virar": {"slow": "1/2", "fast": "3/4"},
        },
        "train_types": {"slow": "Slow Local", "fast": "Fast Local"},
        "stations": [
            "churchgate", "marine lines", "charni road", "grant road",
            "mumbai central", "mahalaxmi", "lower parel", "elphinstone road",
            "dadar", "matunga road", "mahim", "bandra", "khar", "santacruz",
            "vile parle", "andheri", "jogeshwari", "goregaon", "malad",
            "kandivali", "borivali", "dahisar", "mira road", "bhayandar",
            "naigaon", "vasai road", "virar"
        ],
        "fast_stations": [
            "churchgate", "mumbai central", "dadar", "bandra",
            "andheri", "goregaon", "borivali", "vasai road", "virar"
        ],
        "freq_peak_min": 3,
        "freq_offpeak_min": 8,
    },
    "central": {
        "name": "Central Railway (Main Line)",
        "short": "CR",
        "color": "#ef4444",
        "termini": {"south": "csmt", "north": "kalyan"},
        "platforms": {
            "csmt": {"slow": "1/2/3", "fast": "4/5/6"},
            "masjid": {"slow": "1", "fast": "2"},
            "byculla": {"slow": "1", "fast": "2"},
            "parel": {"slow": "1", "fast": "2"},
            "dadar": {"slow": "1/2", "fast": "3/4"},
            "matunga": {"slow": "1", "fast": "2"},
            "sion": {"slow": "1", "fast": "2"},
            "kurla": {"slow": "1/2", "fast": "3/4"},
            "ghatkopar": {"slow": "1", "fast": "2"},
            "vikhroli": {"slow": "1", "fast": "2"},
            "bhandup": {"slow": "1", "fast": "2"},
            "mulund": {"slow": "1", "fast": "2"},
            "thane": {"slow": "1/2", "fast": "3/4"},
            "dombivli": {"slow": "1/2", "fast": "3/4"},
            "kalyan": {"slow": "1/2", "fast": "3/4/5"},
        },
        "train_types": {"slow": "Slow Local", "fast": "Fast Local"},
        "stations": [
            "csmt", "masjid", "sandhurst road", "byculla", "chinchpokli",
            "currey road", "parel", "dadar", "matunga", "sion", "kurla",
            "vidyavihar", "ghatkopar", "vikhroli", "kanjurmarg", "bhandup",
            "nahur", "mulund", "thane", "kalwa", "mumbra", "diva",
            "kopar", "dombivli", "thakurli", "kalyan"
        ],
        "fast_stations": ["csmt", "dadar", "kurla", "thane", "dombivli", "kalyan"],
        "freq_peak_min": 3,
        "freq_offpeak_min": 7,
    },
    "harbour": {
        "name": "Harbour Line",
        "short": "HL",
        "color": "#8b5cf6",
        "termini": {"south": "csmt", "north": "panvel"},
        "platforms": {
            "csmt": {"slow": "7/8"},
            "masjid": {"slow": "3/4"},
            "sandhurst road": {"slow": "3/4"},
            "dockyard road": {"slow": "1/2"},
            "reay road": {"slow": "1/2"},
            "cotton green": {"slow": "1/2"},
            "sewri": {"slow": "1/2"},
            "wadala road": {"slow": "1/2"},
            "guru tegh bahadur nagar": {"slow": "1/2"},
            "chunabhatti": {"slow": "1/2"},
            "kurla": {"slow": "5/6"},
            "tilak nagar": {"slow": "1/2"},
            "chembur": {"slow": "1/2"},
            "govandi": {"slow": "1/2"},
            "mankhurd": {"slow": "1/2"},
            "vashi": {"slow": "1/2/3"},
            "sanpada": {"slow": "1/2"},
            "juinagar": {"slow": "1/2"},
            "nerul": {"slow": "1/2/3"},
            "seawoods darave": {"slow": "1/2"},
            "belapur": {"slow": "1/2/3"},
            "kharghar": {"slow": "1/2"},
            "mansarovar": {"slow": "1/2"},
            "khandeshwar": {"slow": "1/2"},
            "panvel": {"slow": "1/2/3/4"},
        },
        "train_types": {"slow": "Harbour Local"},
        "stations": [
            "csmt", "masjid", "sandhurst road", "dockyard road", "reay road",
            "cotton green", "sewri", "wadala road", "guru tegh bahadur nagar",
            "chunabhatti", "kurla", "tilak nagar", "chembur", "govandi",
            "mankhurd", "vashi", "sanpada", "juinagar", "nerul",
            "seawoods darave", "belapur", "kharghar", "mansarovar",
            "khandeshwar", "panvel"
        ],
        "fast_stations": ["csmt", "wadala road", "kurla", "vashi", "nerul", "panvel"],
        "freq_peak_min": 5,
        "freq_offpeak_min": 8,
    },
    "trans_harbour": {
        "name": "Trans-Harbour Line",
        "short": "THL",
        "color": "#f59e0b",
        "termini": {"west": "thane", "east": "nerul"},
        "platforms": {
            "thane": {"slow": "5/6"},
            "airoli": {"slow": "1/2"},
            "rabale": {"slow": "1/2"},
            "ghansoli": {"slow": "1/2"},
            "koparkhairane": {"slow": "1/2"},
            "turbhe": {"slow": "1/2"},
            "juinagar": {"slow": "3/4"},
            "nerul": {"slow": "3/4"},
        },
        "train_types": {"slow": "Trans-Harbour Local"},
        "stations": [
            "thane", "airoli", "rabale", "ghansoli",
            "koparkhairane", "turbhe", "juinagar", "nerul"
        ],
        "fast_stations": ["thane", "airoli", "nerul"],
        "freq_peak_min": 10,
        "freq_offpeak_min": 15,
    },
}

# ── METRO LINES ───────────────────────────────────────────────────────────────

METRO_LINES = {
    "metro_1": {
        "name": "Metro Line 1",
        "short": "M1",
        "color": "#06b6d4",
        "termini": {"west": "versova", "east": "ghatkopar"},
        "platforms": {s: {"metro": "1/2"} for s in [
            "versova", "jogeshwari", "andheri", "chakala",
            "marol naka", "saki naka", "asalpha", "ghatkopar"
        ]},
        "train_types": {"metro": "Metro"},
        "stations": [
            "versova", "jogeshwari", "andheri", "chakala",
            "marol naka", "saki naka", "asalpha", "ghatkopar"
        ],
        "fast_stations": ["versova", "andheri", "ghatkopar"],
        "freq_peak_min": 4,
        "freq_offpeak_min": 8,
    },
    "metro_2a": {
        "name": "Metro Line 2A",
        "short": "M2A",
        "color": "#10b981",
        "termini": {"south": "d n nagar", "north": "dahisar east"},
        "platforms": {s: {"metro": "1/2"} for s in [
            "dahisar east", "kandivali east", "borivali east",
            "goregaon east", "malad east", "kandivali", "andheri west", "d n nagar"
        ]},
        "train_types": {"metro": "Metro"},
        "stations": [
            "dahisar east", "kandivali east", "borivali east",
            "goregaon east", "malad east", "kandivali", "andheri west", "d n nagar"
        ],
        "fast_stations": ["dahisar east", "andheri west", "d n nagar"],
        "freq_peak_min": 5,
        "freq_offpeak_min": 10,
    },
    "metro_7": {
        "name": "Metro Line 7",
        "short": "M7",
        "color": "#f97316",
        "termini": {"south": "andheri east", "north": "dahisar east"},
        "platforms": {s: {"metro": "1/2"} for s in [
            "dahisar east", "kandivali east", "goregaon east",
            "jogeshwari east", "andheri east"
        ]},
        "train_types": {"metro": "Metro"},
        "stations": [
            "dahisar east", "kandivali east", "goregaon east",
            "jogeshwari east", "andheri east"
        ],
        "fast_stations": ["dahisar east", "andheri east"],
        "freq_peak_min": 5,
        "freq_offpeak_min": 10,
    },
}

# ── CROSS-NETWORK INTERCHANGE MAP ─────────────────────────────────────────────
# For lines that share NO direct station, define the best interchange path
# (src_line, dst_line) → preferred interchange station + platform

CROSS_NETWORK = {
    ("western",      "harbour"):      {"ic": "csmt",       "pf_src": "3/4",  "pf_dst": "7/8"},
    ("western",      "trans_harbour"):{"ic": "csmt",       "pf_src": "3/4",  "pf_dst": "7/8"},
    ("harbour",      "western"):      {"ic": "csmt",       "pf_src": "7/8",  "pf_dst": "1/2"},
    ("harbour",      "trans_harbour"):{"ic": "nerul",      "pf_src": "1/2",  "pf_dst": "3/4"},
    ("trans_harbour","harbour"):      {"ic": "nerul",      "pf_src": "3/4",  "pf_dst": "1/2"},
    ("trans_harbour","western"):      {"ic": "csmt",       "pf_src": "1/2",  "pf_dst": "1/2"},
    ("metro_1",      "harbour"):      {"ic": "ghatkopar",  "pf_src": "1/2",  "pf_dst": "5/6"},
    ("metro_1",      "central"):      {"ic": "ghatkopar",  "pf_src": "1/2",  "pf_dst": "1/2"},
    ("central",      "metro_1"):      {"ic": "ghatkopar",  "pf_src": "1/2",  "pf_dst": "1/2"},
    ("western",      "metro_1"):      {"ic": "andheri",    "pf_src": "1/2",  "pf_dst": "1/2"},
    ("metro_1",      "western"):      {"ic": "andheri",    "pf_src": "1/2",  "pf_dst": "1/2"},
}

# ── HYBRID ROUTES (Bus+Train, Train+Bus, Train+Metro+Train) ───────────────────
# These are manually curated multi-modal journeys for common city pairs

HYBRID_ROUTES = [
    # Santacruz → Vashi: Bus 311 to Kurla + Harbour Line
    {
        "from_match": ["santacruz"],
        "to_match": ["vashi", "nerul", "panvel", "belapur", "kharghar"],
        "name": "Bus 311 + Harbour Line",
        "modes": ["Bus", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Bus",
                "line": "BEST Bus 311",
                "from": "Santacruz Station (W)",
                "to": "Kurla Station (W)",
                "via": ["Santacruz East", "Kalina", "Vakola"],
                "stops": 5,
                "freq_min": 10,
                "fare": 10,
                "journey_min": 25,
                "color": "#10b981",
                "platform": "—",
                "train_type": "", "direction": "Kurla",
                "is_fast": False,
                "boarding_tip": "Board BEST Bus 311 from Santacruz Station West, stand near signal",
                "alight_tip": "Alight at Kurla Station West. Walk to Kurla station for Harbour Line",
            },
            {
                "mode": "Transfer",
                "line": "Walk to Kurla station — Harbour Line",
                "from": "Kurla Station (W)", "to": "Kurla Station (HL)",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "5/6",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Go to Kurla station Harbour Line side — Platform 5/6",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Harbour Line",
                "from": "Kurla",
                "to": "Vashi / Nerul / Panvel (as needed)",
                "stops": 5,
                "freq_min": 10,
                "fare": 15,
                "color": "#8b5cf6",
                "platform": "5/6",
                "train_type": "Harbour Local",
                "direction": "Panvel",
                "is_fast": False,
                "boarding_tip": "Board Harbour Local towards Panvel from Platform 5/6 at Kurla",
                "alight_tip": "Alight at Vashi (or Nerul/Panvel as needed)",
            },
        ],
        "num_stops": 10,
        "frequency_min": 10,
        "description": "BEST Bus 311 to Kurla, then Harbour Line to Vashi/Panvel",
    },

    # Borivali → Vashi: WR to CSMT + Harbour Line
    {
        "from_match": ["borivali", "dahisar", "mira road", "virar", "vasai road", "naigaon", "bhayandar"],
        "to_match": ["vashi", "nerul", "panvel", "belapur", "kharghar", "sanpada"],
        "name": "WR to CSMT + Harbour Line",
        "modes": ["Local Train", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Western Railway",
                "from": "Borivali / North Mumbai",
                "to": "CSMT",
                "stops": 15,
                "freq_min": 3,
                "color": "#3b82f6",
                "platform": "3/4",
                "train_type": "Fast Local",
                "direction": "Churchgate",
                "is_fast": True,
                "boarding_tip": "Board Fast Local towards Churchgate from Platform 3/4. Ride to CSMT (last stop or alight at CSMT)",
                "alight_tip": "Alight at CSMT. Walk to Harbour Line — Platform 7/8",
            },
            {
                "mode": "Transfer",
                "line": "Change at CSMT — Harbour Line",
                "from": "CSMT", "to": "CSMT",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "7/8",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Cross over to Platform 7/8 for Harbour Line (Panvel direction)",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Harbour Line",
                "from": "CSMT",
                "to": "Vashi / Nerul / Panvel (as needed)",
                "stops": 15,
                "freq_min": 5,
                "color": "#8b5cf6",
                "platform": "7/8",
                "train_type": "Harbour Local",
                "direction": "Panvel",
                "is_fast": False,
                "boarding_tip": "Board Harbour Local towards Panvel from Platform 7/8",
                "alight_tip": "Alight at Vashi (16th stop from CSMT) or Nerul/Panvel as needed",
            },
        ],
        "num_stops": 30,
        "frequency_min": 10,
        "description": "WR Fast Local to CSMT, change to Harbour Line towards Panvel",
    },

    # Andheri/Goregaon/Malad → Thane/Kalyan: WR to Dadar + CR
    {
        "from_match": ["andheri", "goregaon", "malad", "kandivali", "borivali", "jogeshwari"],
        "to_match": ["thane", "kalyan", "dombivli", "mulund", "bhandup", "vikhroli", "ghatkopar"],
        "name": "WR to Dadar + Central Railway",
        "modes": ["Local Train", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Western Railway",
                "from": "Andheri / North Mumbai",
                "to": "Dadar",
                "stops": 5,
                "freq_min": 3,
                "color": "#3b82f6",
                "platform": "1/2",
                "train_type": "Slow Local",
                "direction": "Churchgate",
                "is_fast": False,
                "boarding_tip": "Board Slow Local towards Churchgate. Alight at Dadar (Platform 1/2 WR side)",
                "alight_tip": "Alight at Dadar WR. Walk across to Dadar CR — Platform 1/2",
            },
            {
                "mode": "Transfer",
                "line": "Change at Dadar — WR to CR",
                "from": "Dadar (WR)", "to": "Dadar (CR)",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "1/2",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Walk from Dadar WR side to Dadar CR side — Platform 1/2 for Kalyan direction",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Central Railway (Main Line)",
                "from": "Dadar",
                "to": "Thane / Kalyan (as needed)",
                "stops": 6,
                "freq_min": 3,
                "color": "#ef4444",
                "platform": "3/4",
                "train_type": "Fast Local",
                "direction": "Kalyan",
                "is_fast": True,
                "boarding_tip": "Board CR Fast Local towards Kalyan from Platform 3/4",
                "alight_tip": "Alight at Thane (5 stops) or Kalyan (9 stops) as needed",
            },
        ],
        "num_stops": 11,
        "frequency_min": 3,
        "description": "WR to Dadar, change to Central Railway towards Thane/Kalyan",
    },

    # South Mumbai → Andheri/Goregaon: CR to Dadar + WR
    {
        "from_match": ["csmt", "masjid", "byculla", "parel", "sion", "kurla", "ghatkopar", "dadar"],
        "to_match": ["andheri", "goregaon", "malad", "kandivali", "borivali", "vile parle", "jogeshwari"],
        "name": "CR/HL to Dadar + Western Railway",
        "modes": ["Local Train", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Central Railway",
                "from": "CSMT / South Mumbai",
                "to": "Dadar",
                "stops": 7,
                "freq_min": 3,
                "color": "#ef4444",
                "platform": "1/2",
                "train_type": "Slow Local",
                "direction": "Kalyan",
                "is_fast": False,
                "boarding_tip": "Board CR Slow Local towards Kalyan, alight at Dadar (Platform 1/2)",
                "alight_tip": "Alight at Dadar CR. Walk to Dadar WR — Platform 1/2 or 3/4",
            },
            {
                "mode": "Transfer",
                "line": "Change at Dadar — CR to WR",
                "from": "Dadar (CR)", "to": "Dadar (WR)",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "3/4",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Walk to Dadar WR side, Platform 3/4 for Fast Local towards Virar",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Western Railway",
                "from": "Dadar",
                "to": "Andheri / Borivali (as needed)",
                "stops": 7,
                "freq_min": 3,
                "color": "#3b82f6",
                "platform": "3/4",
                "train_type": "Fast Local",
                "direction": "Virar",
                "is_fast": True,
                "boarding_tip": "Board WR Fast Local towards Virar from Platform 3/4",
                "alight_tip": "Alight at Andheri (3 stops) or Borivali (7 stops) as needed",
            },
        ],
        "num_stops": 14,
        "frequency_min": 3,
        "description": "CR to Dadar, change to Western Railway towards Andheri/Borivali",
    },

    # Metro + Harbour: Andheri metro → Ghatkopar → Harbour Line (Navi Mumbai)
    {
        "from_match": ["versova", "d n nagar", "andheri west"],
        "to_match": ["vashi", "nerul", "panvel", "belapur", "chembur", "mankhurd"],
        "name": "Metro + Harbour Line",
        "modes": ["Metro", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Metro",
                "line": "Metro Line 1",
                "from": "Andheri / Versova",
                "to": "Ghatkopar",
                "stops": 7,
                "freq_min": 4,
                "fare": 40,
                "color": "#06b6d4",
                "platform": "1/2",
                "train_type": "Metro",
                "direction": "Ghatkopar",
                "is_fast": False,
                "boarding_tip": "Board Metro Line 1 towards Ghatkopar from Platform 1/2",
                "alight_tip": "Alight at Ghatkopar. Take exit towards CR/HL platforms",
            },
            {
                "mode": "Transfer",
                "line": "Change at Ghatkopar — Metro to Harbour Line",
                "from": "Ghatkopar (Metro)", "to": "Ghatkopar (HL)",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "5/6",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Exit Metro at Ghatkopar. Walk to Harbour Line — Platform 5/6",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Harbour Line",
                "from": "Ghatkopar",
                "to": "Vashi / Nerul / Panvel (as needed)",
                "stops": 6,
                "freq_min": 5,
                "color": "#8b5cf6",
                "platform": "5/6",
                "train_type": "Harbour Local",
                "direction": "Panvel",
                "is_fast": False,
                "boarding_tip": "Board Harbour Local towards Panvel from Platform 5/6 at Ghatkopar",
                "alight_tip": "Alight at Vashi, Nerul, or Panvel as needed",
            },
        ],
        "num_stops": 13,
        "frequency_min": 10,
        "description": "Metro Line 1 to Ghatkopar, then Harbour Line to Navi Mumbai",
    },

    # Thane → Navi Mumbai via Trans-Harbour
    {
        "from_match": ["thane", "kalwa", "mumbra"],
        "to_match": ["vashi", "nerul", "belapur", "panvel", "airoli", "ghansoli", "koparkhairane"],
        "name": "Trans-Harbour Line (Direct)",
        "modes": ["Local Train"],
        "transfers": 0,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Trans-Harbour Line",
                "from": "Thane",
                "to": "Vashi / Nerul (via Airoli)",
                "stops": 7,
                "freq_min": 15,
                "color": "#f59e0b",
                "platform": "5/6",
                "train_type": "Trans-Harbour Local",
                "direction": "Nerul",
                "is_fast": False,
                "boarding_tip": "Board Trans-Harbour Local towards Nerul from Platform 5/6 at Thane",
                "alight_tip": "Alight at Airoli (2nd stop), Ghansoli, Koparkhairane, Turbhe, or Nerul",
            },
        ],
        "num_stops": 7,
        "frequency_min": 15,
        "description": "Direct Trans-Harbour Local from Thane to Navi Mumbai via Airoli",
    },

    # CSMT / South Mumbai → Navi Mumbai via Harbour Line
    {
        "from_match": ["csmt", "churchgate", "marine lines", "grant road", "mumbai central",
                       "mahalaxmi", "lower parel", "parel", "byculla"],
        "to_match": ["vashi", "nerul", "panvel", "belapur", "kharghar", "sanpada",
                     "juinagar", "seawoods darave", "mansarovar", "khandeshwar"],
        "name": "Harbour Line (Direct — South Mumbai to Navi Mumbai)",
        "modes": ["Local Train"],
        "transfers": 0,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Harbour Line",
                "from": "CSMT / South Mumbai",
                "to": "Vashi / Nerul / Panvel (as needed)",
                "stops": 16,
                "freq_min": 5,
                "color": "#8b5cf6",
                "platform": "7/8",
                "train_type": "Harbour Local",
                "direction": "Panvel",
                "is_fast": False,
                "boarding_tip": "Board Harbour Local from CSMT Platform 7/8 towards Panvel",
                "alight_tip": "Alight at Vashi (16th stop), Nerul (19th), or Panvel (24th) as needed",
            },
        ],
        "num_stops": 16,
        "frequency_min": 10,
        "description": "Direct Harbour Local from CSMT to Navi Mumbai",
    },

    # Goregaon / Andheri → Panvel (the exact route the user asked about)
    {
        "from_match": ["goregaon", "santacruz", "vile parle", "andheri", "jogeshwari", "malad"],
        "to_match": ["panvel", "kharghar", "mansarovar", "khandeshwar", "belapur", "seawoods darave"],
        "name": "WR to CSMT + Harbour Line to Panvel",
        "modes": ["Local Train", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Western Railway",
                "from": "Goregaon / Andheri",
                "to": "CSMT",
                "stops": 12,
                "freq_min": 3,
                "color": "#3b82f6",
                "platform": "1/2",
                "train_type": "Slow Local",
                "direction": "Churchgate",
                "is_fast": False,
                "boarding_tip": "Board Slow Local towards Churchgate. Count stops — Goregaon to CSMT is about 12 stops via Dadar",
                "alight_tip": "Alight at CSMT. Walk to Harbour Line Platform 7/8",
            },
            {
                "mode": "Transfer",
                "line": "Change at CSMT — WR to Harbour Line",
                "from": "CSMT", "to": "CSMT",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "7/8",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Walk to Platform 7/8 at CSMT for Harbour Line towards Panvel",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Harbour Line",
                "from": "CSMT",
                "to": "Panvel",
                "stops": 24,
                "freq_min": 5,
                "color": "#8b5cf6",
                "platform": "7/8",
                "train_type": "Harbour Local",
                "direction": "Panvel",
                "is_fast": False,
                "boarding_tip": "Board Harbour Local towards Panvel from Platform 7/8",
                "alight_tip": "Alight at Panvel — last stop (24th from CSMT)",
            },
        ],
        "num_stops": 36,
        "frequency_min": 10,
        "description": "WR Slow Local to CSMT, then Harbour Local to Panvel",
    },

    # Churchgate / WR → Kurla/Ghatkopar (via Dadar interchange)
    {
        "from_match": ["churchgate", "marine lines", "charni road", "grant road", "mumbai central"],
        "to_match": ["kurla", "ghatkopar", "sion", "matunga", "vidyavihar"],
        "name": "WR to Dadar + Central Railway",
        "modes": ["Local Train", "Local Train"],
        "transfers": 1,
        "steps": [
            {
                "mode": "Local Train",
                "line": "Western Railway",
                "from": "Churchgate / South WR",
                "to": "Dadar",
                "stops": 8,
                "freq_min": 3,
                "color": "#3b82f6",
                "platform": "3/4",
                "train_type": "Fast Local",
                "direction": "Virar",
                "is_fast": True,
                "boarding_tip": "Board WR Fast Local towards Virar from Platform 3/4. Alight at Dadar",
                "alight_tip": "Alight at Dadar WR side. Walk to Dadar CR side",
            },
            {
                "mode": "Transfer",
                "line": "Change at Dadar — WR to CR",
                "from": "Dadar (WR)", "to": "Dadar (CR)",
                "stops": 0, "freq_min": 0,
                "color": "#94a3b8", "platform": "1/2",
                "train_type": "", "direction": "", "is_fast": False,
                "boarding_tip": "Walk to Dadar CR Platform 1/2 for Slow Local towards Kalyan",
                "alight_tip": "",
            },
            {
                "mode": "Local Train",
                "line": "Central Railway (Main Line)",
                "from": "Dadar",
                "to": "Kurla / Ghatkopar (as needed)",
                "stops": 3,
                "freq_min": 3,
                "color": "#ef4444",
                "platform": "1/2",
                "train_type": "Slow Local",
                "direction": "Kalyan",
                "is_fast": False,
                "boarding_tip": "Board CR Slow Local towards Kalyan from Platform 1/2",
                "alight_tip": "Alight at Kurla (2nd stop) or Ghatkopar (3rd stop)",
            },
        ],
        "num_stops": 11,
        "frequency_min": 3,
        "description": "WR Fast to Dadar, then CR Slow to Kurla/Ghatkopar",
    },
]

# ── BEST / NMMT BUS ROUTES ────────────────────────────────────────────────────

BEST_BUS_ROUTES = {
    "311":  {"from_stop": "Santacruz Station (W)", "to_stop": "Kurla Station (W)", "key_stops": ["Santacruz Station (W)", "Santacruz East Naka", "Kalina University", "Vakola Bridge", "Kurla Station (W)"], "boarding_note": "Board from Santacruz Station West, stand near signal", "alight_note": "Alight at Kurla Station West, near auto stand", "freq_min": 10, "fare": 10, "journey_min": 25, "from_match": ["santacruz"], "to_match": ["kurla"]},
    "313":  {"from_stop": "Santacruz Station (E)", "to_stop": "Kurla Station BKC", "key_stops": ["Santacruz Station (E)", "BKC Gate 1", "BKC Gate 5", "Kurla Station BKC"], "boarding_note": "Board from Santacruz Station East", "alight_note": "Alight at Kurla near BKC gate", "freq_min": 12, "fare": 10, "journey_min": 20, "from_match": ["santacruz"], "to_match": ["kurla"]},
    "507":  {"from_stop": "Santacruz Station (W)", "to_stop": "Nerul Bus Station", "key_stops": ["Santacruz Station (W)", "Bandra East", "Kurla Station", "Chembur Naka", "Mankhurd", "Vashi Bus Stop", "Nerul Bus Station"], "boarding_note": "Board from Santacruz Station West — Bus Bay 3", "alight_note": "Alight at Vashi Bus Stop or Nerul Bus Station as needed", "freq_min": 30, "fare": 40, "journey_min": 75, "from_match": ["santacruz"], "to_match": ["vashi", "nerul"]},
    "517":  {"from_stop": "Santacruz Station (W)", "to_stop": "Vashi APMC Market", "key_stops": ["Santacruz Station (W)", "Bandra", "Kurla", "Chembur", "Mankhurd", "Vashi APMC Market"], "boarding_note": "Board from Santacruz Station West — Bus Bay near McDonald's", "alight_note": "Alight at Vashi APMC Market stop", "freq_min": 25, "fare": 35, "journey_min": 70, "from_match": ["santacruz"], "to_match": ["vashi"]},
    "301":  {"from_stop": "Bandra Station (W)", "to_stop": "CSMT Bus Terminus", "key_stops": ["Bandra Station (W)", "Mahim Church", "Dadar TT", "Parel", "CSMT Bus Terminus"], "boarding_note": "Board from Bandra Station West, outside exit", "alight_note": "Alight at CSMT Bus Terminus near Platform 1", "freq_min": 8, "fare": 15, "journey_min": 40, "from_match": ["bandra"], "to_match": ["csmt", "cst"]},
    "302":  {"from_stop": "Bandra Station (W)", "to_stop": "Andheri Station (W)", "key_stops": ["Bandra Station (W)", "Khar Station", "Santacruz Station", "Vile Parle Station", "Andheri Station (W)"], "boarding_note": "Board from Bandra Station West — Bus Bay 1", "alight_note": "Alight at Andheri Station West", "freq_min": 8, "fare": 10, "journey_min": 25, "from_match": ["bandra"], "to_match": ["andheri"]},
    "201":  {"from_stop": "Andheri Station (W)", "to_stop": "Bandra Station (W)", "key_stops": ["Andheri Station (W)", "Vile Parle Station", "Santacruz Station", "Bandra Station (W)"], "boarding_note": "Board from Andheri Station West — Bus Bay 1", "alight_note": "Alight at Bandra Station West", "freq_min": 8, "fare": 10, "journey_min": 20, "from_match": ["andheri"], "to_match": ["bandra"]},
    "228":  {"from_stop": "Andheri Station (W)", "to_stop": "CSMT", "key_stops": ["Andheri Station (W)", "Vile Parle", "Santacruz", "Bandra", "Dadar TT", "CSMT"], "boarding_note": "Board from Andheri Station West — Bus Bay 2", "alight_note": "Alight at CSMT Bus Terminus", "freq_min": 15, "fare": 25, "journey_min": 55, "from_match": ["andheri"], "to_match": ["csmt", "cst", "churchgate"]},
    "232":  {"from_stop": "Andheri Station (E)", "to_stop": "Kurla Station", "key_stops": ["Andheri Station (E)", "MIDC", "Marol", "Kurla Station"], "boarding_note": "Board from Andheri Station East bus stop", "alight_note": "Alight at Kurla Station", "freq_min": 12, "fare": 12, "journey_min": 20, "from_match": ["andheri"], "to_match": ["kurla"]},
    "351":  {"from_stop": "Dadar Station (E)", "to_stop": "Kurla Station", "key_stops": ["Dadar Station (E)", "Sion Hospital", "Sion Station", "Kurla Station"], "boarding_note": "Board from Dadar Station East, near signal", "alight_note": "Alight at Kurla Station bus stop", "freq_min": 10, "fare": 10, "journey_min": 20, "from_match": ["dadar"], "to_match": ["kurla"]},
    "352":  {"from_stop": "Dadar Station (W)", "to_stop": "Bandra Station", "key_stops": ["Dadar Station (W)", "Shivaji Park", "Mahim", "Bandra Station"], "boarding_note": "Board from Dadar Station West, near petrol pump", "alight_note": "Alight at Bandra Station West", "freq_min": 10, "fare": 10, "journey_min": 20, "from_match": ["dadar"], "to_match": ["bandra"]},
    "451":  {"from_stop": "Borivali Station (W)", "to_stop": "Andheri Station (W)", "key_stops": ["Borivali Station (W)", "Kandivali Station", "Malad Station", "Goregaon Station", "Andheri Station (W)"], "boarding_note": "Board from Borivali Station West — Bus Bay near exit gate", "alight_note": "Alight at Andheri Station West", "freq_min": 10, "fare": 15, "journey_min": 35, "from_match": ["borivali"], "to_match": ["andheri"]},
    "T01":  {"from_stop": "Thane Station (E)", "to_stop": "Vashi Bus Stand", "key_stops": ["Thane Station (E)", "Airoli Naka", "Ghansoli", "Vashi Bus Stand"], "boarding_note": "Board from Thane Station East — NMMT Bus Bay", "alight_note": "Alight at Vashi Bus Stand", "freq_min": 20, "fare": 20, "journey_min": 35, "from_match": ["thane"], "to_match": ["vashi"]},
    "T02":  {"from_stop": "Thane Station", "to_stop": "Kalyan Station", "key_stops": ["Thane Station", "Diva Junction", "Dombivli Station", "Kalyan Station"], "boarding_note": "Board from Thane Station bus stand, East exit", "alight_note": "Alight at Kalyan Station bus stand", "freq_min": 15, "fare": 20, "journey_min": 40, "from_match": ["thane"], "to_match": ["kalyan"]},
    "C01":  {"from_stop": "CSMT Bus Terminus", "to_stop": "Dadar Station (W)", "key_stops": ["CSMT Bus Terminus", "Grant Road", "Mahalaxmi", "Lower Parel", "Dadar Station (W)"], "boarding_note": "Board from CSMT Bus Terminus — Bay 3 or 4", "alight_note": "Alight at Dadar Station West", "freq_min": 8, "fare": 12, "journey_min": 30, "from_match": ["csmt", "cst", "churchgate"], "to_match": ["dadar"]},
    "C02":  {"from_stop": "CSMT Bus Terminus", "to_stop": "Bandra Station (W)", "key_stops": ["CSMT Bus Terminus", "Parel", "Dadar", "Mahim", "Bandra Station (W)"], "boarding_note": "Board from CSMT Bus Terminus — Bay 2", "alight_note": "Alight at Bandra Station West", "freq_min": 10, "fare": 15, "journey_min": 45, "from_match": ["csmt", "cst", "churchgate"], "to_match": ["bandra"]},
    "GB1":  {"from_stop": "Churchgate Station", "to_stop": "Bandra Station", "key_stops": ["Churchgate Station", "Marine Lines", "Grant Road", "Mumbai Central", "Mahalaxmi", "Lower Parel", "Bandra Station"], "boarding_note": "Board from Churchgate Station bus stop, outside main entrance", "alight_note": "Alight at Bandra Station West", "freq_min": 10, "fare": 15, "journey_min": 40, "from_match": ["churchgate"], "to_match": ["bandra"]},
    "K01":  {"from_stop": "Kurla Station (W)", "to_stop": "BKC", "key_stops": ["Kurla Station (W)", "BKC Gate 1", "BKC"], "boarding_note": "Board from Kurla Station West, Bus Bay 1", "alight_note": "Alight at BKC main gate", "freq_min": 10, "fare": 8, "journey_min": 10, "from_match": ["kurla"], "to_match": ["bkc", "bandra kurla"]},
    # ── NMMT Bus routes — Navi Mumbai ─────────────────────────────────────────
    "NMMT-22": {
        "from_stop": "Kharghar Jal Vihar",
        "to_stop": "Vashi Bus Stand",
        "key_stops": [
            "Kharghar Jal Vihar",
            "Kharghar Sector 20",
            "Juinagar Station",
            "Sanpada",
            "Vashi Bus Stand"
        ],
        "boarding_note": "Board NMMT Bus 22 from Kharghar Jal Vihar bus stop",
        "alight_note": "Alight at Vashi Bus Stand — or at Juinagar Station if needed",
        "freq_min": 20, "fare": 15, "journey_min": 35,
        "from_match": ["kharghar"], "to_match": ["vashi", "juinagar", "sanpada"],
    },
    "NMMT-23": {
        "from_stop": "Panvel Station",
        "to_stop": "Vashi Bus Stand",
        "key_stops": [
            "Panvel Station",
            "Khandeshwar",
            "Mansarovar",
            "Kharghar",
            "Juinagar Station",
            "Sanpada",
            "Vashi Bus Stand"
        ],
        "boarding_note": "Board NMMT Bus 23 from Panvel Station bus stand",
        "alight_note": "Alight at Vashi Bus Stand",
        "freq_min": 25, "fare": 25, "journey_min": 50,
        "from_match": ["panvel"], "to_match": ["vashi", "kharghar", "juinagar"],
    },
    "NMMT-36": {
        "from_stop": "Belapur Station",
        "to_stop": "Vashi Bus Stand",
        "key_stops": [
            "Belapur Station",
            "Nerul Station",
            "Juinagar Station",
            "Sanpada",
            "Vashi Bus Stand"
        ],
        "boarding_note": "Board NMMT Bus 36 from Belapur Station bus stand",
        "alight_note": "Alight at Vashi Bus Stand",
        "freq_min": 20, "fare": 15, "journey_min": 30,
        "from_match": ["belapur", "nerul"], "to_match": ["vashi", "juinagar", "sanpada"],
    },
    "NMMT-41": {
        "from_stop": "Airoli Bus Stand",
        "to_stop": "Vashi Bus Stand",
        "key_stops": [
            "Airoli Bus Stand",
            "Ghansoli",
            "Koparkhairane",
            "Turbhe",
            "Vashi Bus Stand"
        ],
        "boarding_note": "Board NMMT Bus 41 from Airoli Bus Stand",
        "alight_note": "Alight at Vashi Bus Stand",
        "freq_min": 20, "fare": 15, "journey_min": 25,
        "from_match": ["airoli", "ghansoli", "koparkhairane"], "to_match": ["vashi", "turbhe"],
    },
    "NMMT-101": {
        "from_stop": "Nerul Station",
        "to_stop": "Thane Station",
        "key_stops": [
            "Nerul Station",
            "Airoli",
            "Ghansoli",
            "Thane Station"
        ],
        "boarding_note": "Board NMMT Bus 101 from Nerul Station bus stand",
        "alight_note": "Alight at Thane Station",
        "freq_min": 30, "fare": 30, "journey_min": 45,
        "from_match": ["nerul", "airoli"], "to_match": ["thane"],
    },
    "NMMT-106": {
        "from_stop": "CBD Belapur",
        "to_stop": "Thane Station",
        "key_stops": [
            "CBD Belapur",
            "Vashi",
            "Airoli",
            "Thane Station"
        ],
        "boarding_note": "Board NMMT Bus 106 from CBD Belapur bus stand",
        "alight_note": "Alight at Thane Station",
        "freq_min": 25, "fare": 30, "journey_min": 50,
        "from_match": ["belapur"], "to_match": ["thane"],
    },
    "NMMT-111": {
        "from_stop": "Panvel Station",
        "to_stop": "Thane Station",
        "key_stops": [
            "Panvel Station",
            "Kharghar",
            "Vashi",
            "Airoli",
            "Thane Station"
        ],
        "boarding_note": "Board NMMT Bus 111 from Panvel Station",
        "alight_note": "Alight at Thane Station",
        "freq_min": 30, "fare": 40, "journey_min": 70,
        "from_match": ["panvel"], "to_match": ["thane"],
    },
    "NMMT-14": {
        "from_stop": "Juinagar Station",
        "to_stop": "Vashi Bus Stand",
        "key_stops": [
            "Juinagar Station",
            "Sanpada",
            "Vashi Sector 30",
            "Vashi Bus Stand"
        ],
        "boarding_note": "Board NMMT Bus 14 from Juinagar Station bus stop",
        "alight_note": "Alight at Vashi Bus Stand",
        "freq_min": 15, "fare": 10, "journey_min": 15,
        "from_match": ["juinagar"], "to_match": ["vashi", "sanpada"],
    },
    "NMMT-8": {
        "from_stop": "Kharghar Sector 1",
        "to_stop": "Belapur Station",
        "key_stops": [
            "Kharghar Sector 1",
            "Kharghar Sector 12",
            "Kharghar Jal Vihar",
            "Belapur Station"
        ],
        "boarding_note": "Board NMMT Bus 8 from Kharghar Sector 1 bus stop",
        "alight_note": "Alight at Belapur Station",
        "freq_min": 20, "fare": 10, "journey_min": 20,
        "from_match": ["kharghar"], "to_match": ["belapur"],
    },
    "NMMT-51": {
        "from_stop": "Vashi Bus Stand",
        "to_stop": "Panvel Station",
        "key_stops": [
            "Vashi Bus Stand",
            "Sanpada",
            "Juinagar",
            "Nerul",
            "Seawoods",
            "Belapur",
            "Kharghar",
            "Panvel Station"
        ],
        "boarding_note": "Board NMMT Bus 51 from Vashi Bus Stand — Bay 2",
        "alight_note": "Alight at Panvel Station",
        "freq_min": 20, "fare": 25, "journey_min": 55,
        "from_match": ["vashi", "sanpada"], "to_match": ["panvel", "kharghar", "belapur"],
    },
}


# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def get_train_direction(line_id, src, dst):
    line = TRAIN_LINES.get(line_id) or METRO_LINES.get(line_id)
    if not line:
        return ""
    stations = line["stations"]
    if src not in stations or dst not in stations:
        return ""
    termini = line.get("termini", {})
    if stations.index(dst) > stations.index(src):
        return termini.get("north") or termini.get("east") or stations[-1]
    return termini.get("south") or termini.get("west") or stations[0]


def get_train_type(line_id, src, dst):
    if line_id.startswith("metro"):
        return "metro"
    if line_id in ("harbour", "trans_harbour"):
        return "slow"
    line = TRAIN_LINES.get(line_id, {})
    if src in line.get("fast_stations", []) and dst in line.get("fast_stations", []):
        return "fast"
    return "slow"


def get_platform(line_id, station, train_type):
    line = TRAIN_LINES.get(line_id) or METRO_LINES.get(line_id)
    if not line:
        return "1"
    sp = line.get("platforms", {}).get(station, {})
    if isinstance(sp, dict):
        return (sp.get(train_type) or sp.get("slow") or
                sp.get("harbour") or sp.get("trans") or sp.get("metro") or "1")
    return str(sp) or "1"


def find_station_on_line(station):
    key = station.strip().lower()
    results = []
    for lid, line in TRAIN_LINES.items():
        if key in line["stations"]:
            results.append(("train", lid, line))
    for lid, line in METRO_LINES.items():
        if key in line["stations"]:
            results.append(("metro", lid, line))
    return results


def find_interchange(src_id, dst_id):
    all_lines = {**TRAIN_LINES, **METRO_LINES}
    src_s = set(all_lines.get(src_id, {}).get("stations", []))
    dst_s = set(all_lines.get(dst_id, {}).get("stations", []))
    priority = ["csmt", "dadar", "kurla", "thane", "andheri",
                "ghatkopar", "wadala road", "nerul", "bandra", "borivali"]
    common = list(src_s & dst_s)
    common.sort(key=lambda s: priority.index(s) if s in priority else 99)
    return common


def _count_stops(line_id, s1, s2):
    line = TRAIN_LINES.get(line_id) or METRO_LINES.get(line_id)
    if not line:
        return 4
    stations = line["stations"]
    if s1 in stations and s2 in stations:
        return abs(stations.index(s1) - stations.index(s2))
    return 4


def _train_step(mode, line, src, dst, stops, freq, tt, direction, platform):
    train_label = line.get("train_types", {}).get(tt, "Local")
    is_fast = tt == "fast"
    return {
        "mode": mode, "line": line["name"], "line_short": line.get("short", ""),
        "from": src, "to": dst, "stops": stops, "freq_min": freq,
        "color": line["color"], "platform": platform, "train_type": train_label,
        "direction": direction.title() if direction else "",
        "is_fast": is_fast,
        "boarding_tip": f"Board {'Fast' if is_fast else train_label} towards {direction.title() if direction else dst} from Platform {platform}",
        "alight_tip": f"Alight at {dst} — {stops} stop{'s' if stops != 1 else ''}",
    }


def _transfer_step(ic, next_line_name, next_platform):
    return {
        "mode": "Transfer", "line": f"Change at {ic}", "line_short": "Change",
        "from": ic, "to": ic, "stops": 0, "freq_min": 0,
        "color": "#94a3b8", "platform": next_platform,
        "train_type": "", "direction": "", "is_fast": False,
        "boarding_tip": f"Cross to Platform {next_platform} for {next_line_name}",
        "alight_tip": "",
    }


def _bus_step(bus_num, bus):
    return {
        "mode": "Bus", "line": f"BEST Bus {bus_num}", "line_short": bus_num,
        "from": bus["from_stop"], "to": bus["to_stop"],
        "via": bus["key_stops"][1:-1],
        "stops": len(bus["key_stops"]),
        "freq_min": bus["freq_min"], "fare": bus["fare"],
        "journey_min": bus["journey_min"],
        "color": "#10b981", "platform": "—",
        "train_type": "", "direction": bus["to_stop"], "is_fast": False,
        "boarding_tip": bus["boarding_note"],
        "alight_tip": bus["alight_note"],
    }


def _match(src, dst, from_list, to_list):
    """Check if src/dst matches any item in from_list/to_list."""
    return (
        any(m in src or src in m for m in from_list) and
        any(m in dst or dst in m for m in to_list)
    )


# ── MAIN ROUTE FINDER ─────────────────────────────────────────────────────────

def get_real_transit_routes(source: str, destination: str, is_peak: bool) -> list:
    """
    Find best transit routes between any two Mumbai stations.
    Returns up to 3 options covering: Direct train, Interchange,
    Hybrid (multi-modal), Bus, Auto/Cab.
    """
    src = source.strip().lower()
    dst = destination.strip().lower()

    src_lines = find_station_on_line(src)
    dst_lines = find_station_on_line(dst)

    routes = []

    # ── 1. Direct same-line train/metro ───────────────────────────────────────
    for s_type, s_id, s_line in src_lines:
        for d_type, d_id, d_line in dst_lines:
            if s_id != d_id:
                continue
            stations = s_line["stations"]
            if src not in stations or dst not in stations:
                continue
            stops = abs(stations.index(src) - stations.index(dst))
            freq = s_line["freq_peak_min"] if is_peak else s_line["freq_offpeak_min"]
            mode = "Metro" if s_type == "metro" else "Local Train"
            tt = get_train_type(s_id, src, dst)
            direction = get_train_direction(s_id, src, dst)
            platform = get_platform(s_id, src, tt)
            train_label = s_line.get("train_types", {}).get(tt, "Local")
            routes.append({
                "type": "direct_train",
                "name": s_line["name"],
                "modes": [mode],
                "steps": [_train_step(mode, s_line, source, destination, stops, freq, tt, direction, platform)],
                "num_stops": stops, "transfers": 0,
                "frequency_min": freq,
                "description": f"Direct {train_label} — {s_line['name']}",
            })
            break
        if routes:
            break

    # ── 2. Hybrid / multi-modal curated routes ────────────────────────────────
    for hybrid in HYBRID_ROUTES:
        if len(routes) >= 2:
            break
        if not _match(src, dst, hybrid["from_match"], hybrid["to_match"]):
            continue
        # Don't duplicate a direct route we already found
        if routes and routes[0]["type"] == "direct_train" and len(hybrid["modes"]) == 1:
            continue
        routes.append({
            "type": "hybrid",
            "name": hybrid["name"],
            "modes": hybrid["modes"],
            "steps": hybrid["steps"],
            "num_stops": hybrid["num_stops"],
            "transfers": hybrid["transfers"],
            "frequency_min": hybrid["frequency_min"],
            "description": hybrid["description"],
        })

    # ── 3. Standard interchange (common station between lines) ────────────────
    if len(routes) < 2:
        for s_type, s_id, s_line in src_lines:
            for d_type, d_id, d_line in dst_lines:
                if s_id == d_id:
                    continue
                # Check CROSS_NETWORK first
                cn = CROSS_NETWORK.get((s_id, d_id))
                if cn:
                    ic = cn["ic"]
                    pf1 = cn["pf_src"]
                    pf2 = cn["pf_dst"]
                else:
                    ics = find_interchange(s_id, d_id)
                    if not ics:
                        continue
                    ic = ics[0]
                    tt1 = get_train_type(s_id, src, ic)
                    tt2 = get_train_type(d_id, ic, dst)
                    pf1 = get_platform(s_id, src, tt1)
                    pf2 = get_platform(d_id, ic, tt2)

                stops1 = _count_stops(s_id, src, ic)
                stops2 = _count_stops(d_id, ic, dst)
                freq1 = s_line["freq_peak_min"] if is_peak else s_line["freq_offpeak_min"]
                freq2 = d_line["freq_peak_min"] if is_peak else d_line["freq_offpeak_min"]
                mode1 = "Metro" if s_type == "metro" else "Local Train"
                mode2 = "Metro" if d_type == "metro" else "Local Train"
                tt1 = get_train_type(s_id, src, ic)
                tt2 = get_train_type(d_id, ic, dst)
                dir1 = get_train_direction(s_id, src, ic)
                dir2 = get_train_direction(d_id, ic, dst)
                if not cn:
                    pf1 = get_platform(s_id, src, tt1)
                    pf2 = get_platform(d_id, ic, tt2)
                routes.append({
                    "type": "interchange",
                    "name": f"{s_line.get('short','TR')} → {d_line.get('short','TR')} via {ic.title()}",
                    "modes": [mode1, mode2],
                    "steps": [
                        _train_step(mode1, s_line, source, ic.title(), stops1, freq1, tt1, dir1, pf1),
                        _transfer_step(ic.title(), d_line["name"], pf2),
                        _train_step(mode2, d_line, ic.title(), destination, stops2, freq2, tt2, dir2, pf2),
                    ],
                    "num_stops": stops1 + stops2, "transfers": 1,
                    "frequency_min": max(freq1, freq2),
                    "description": f"{s_line['name']} → change at {ic.title()} → {d_line['name']}",
                })
                if len(routes) >= 2:
                    break
            if len(routes) >= 2:
                break

    # ── 4. Bus route ──────────────────────────────────────────────────────────
    if len(routes) < 3:
        for bus_num, bus in BEST_BUS_ROUTES.items():
            if _match(src, dst, bus["from_match"], bus["to_match"]):
                routes.append({
                    "type": "bus",
                    "name": f"BEST Bus {bus_num}",
                    "modes": ["Bus"],
                    "steps": [_bus_step(bus_num, bus)],
                    "num_stops": len(bus["key_stops"]),
                    "transfers": 0,
                    "frequency_min": bus["freq_min"],
                    "description": f"BEST Bus {bus_num}: {bus['from_stop']} → {bus['to_stop']}",
                })
                break

    # ── 5. Auto / Cab — always show as last option ────────────────────────────
    routes.append({
        "type": "cab_auto",
        "name": "Auto / Cab / Rapido",
        "modes": ["Auto/Cab"],
        "steps": [{
            "mode": "Auto/Cab", "line": "Ola / Uber / Rapido / Auto",
            "line_short": "Cab", "from": source, "to": destination,
            "stops": 0, "freq_min": 3, "color": "#f59e0b", "platform": "—",
            "train_type": "", "direction": destination, "is_fast": True,
            "boarding_tip": f"Book Ola / Uber / Rapido from {source.title()}, or hail an Auto from the stand outside the station exit",
            "alight_tip": f"Drop directly at {destination.title()}",
        }],
        "num_stops": 0, "transfers": 0,
        "frequency_min": 3,
        "description": f"Direct Ola / Uber / Rapido / Auto to {destination.title()}",
    })

    # Remove duplicate types, keep best of each
    seen_types = set()
    deduped = []
    for r in routes:
        key = r["type"]
        if key not in seen_types:
            seen_types.add(key)
            deduped.append(r)

    # Always ensure Auto/Cab is included
    has_cab = any(r["type"] == "cab_auto" for r in deduped)
    if not has_cab:
        deduped.append({
            "type": "cab_auto",
            "name": "Auto / Cab / Rapido",
            "modes": ["Auto/Cab"],
            "steps": [{
                "mode": "Auto/Cab",
                "line": "Ola / Uber / Rapido / Auto",
                "line_short": "Cab",
                "from": source, "to": destination,
                "stops": 0, "freq_min": 3,
                "color": "#f59e0b", "platform": "—",
                "train_type": "", "direction": destination,
                "is_fast": True,
                "boarding_tip": f"Book Ola / Uber / Rapido from {source.title()}, or hail an Auto from the stand outside the station exit",
                "alight_tip": f"Drop directly at {destination.title()}",
            }],
            "num_stops": 0, "transfers": 0,
            "frequency_min": 3,
            "description": f"Direct Ola / Uber / Rapido / Auto to {destination.title()}",
        })

    return deduped[:4]