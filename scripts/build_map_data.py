"""Build the data files for the interactive map in docs/.

Reads the cleaned tables in data/processed/ and the division boundaries, and writes:
  docs/data/divisions.geojson   boundaries with English and Bangla names
  docs/data/accidents.json      BRTA monthly figures per division, BRTA deaths by vehicle group,
                                RSF national monthly and annual figures
  docs/data/blackspots.json     accident-prone highway spots, each with its district
  docs/data/districts.geojson   simplified district boundaries with Bangla name, division and spot count

Run from the repository root:  python scripts/build_map_data.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data"

# Boundary file spellings -> names used in the data.
NAME_FIX = {"Chittagong": "Chattogram", "Rajshani": "Rajshahi", "Barisal": "Barishal"}
BANGLA = {
    "Dhaka": "ঢাকা", "Chattogram": "চট্টগ্রাম", "Rajshahi": "রাজশাহী", "Khulna": "খুলনা",
    "Barishal": "বরিশাল", "Sylhet": "সিলেট", "Rangpur": "রংপুর", "Mymensingh": "ময়মনসিংহ",
}


def build_boundaries():
    geo = json.loads((ROOT / "data/raw/geo/divisions.geojson").read_text())
    for feature in geo["features"]:
        name = NAME_FIX.get(feature["properties"]["division"], feature["properties"]["division"])
        feature["properties"] = {"name": name, "name_bn": BANGLA[name]}
    assert {f["properties"]["name"] for f in geo["features"]} == set(BANGLA)
    (OUT / "divisions.geojson").write_text(json.dumps(geo, separators=(",", ":")))


def as_int_rows(df, columns):
    return [[None if pd.isna(v) else int(v) for v in row] for row in df[columns].itertuples(index=False)]


def build_accidents():
    processed = ROOT / "data/processed"
    div = pd.read_csv(processed / "brta_division.csv")
    pop = pd.read_csv(ROOT / "data/raw/division_population_2022.csv").set_index("division")["pop_2022"]
    assert set(div["division"]) == set(BANGLA)

    vehicle = (
        pd.read_csv(processed / "brta_vehicle_deaths.csv")
        .groupby(["year", "month", "vehicle_group"], as_index=False)["deaths"].sum()
    )
    rsf_monthly = pd.read_csv(processed / "monthly_national.csv")
    rsf_monthly = rsf_monthly[rsf_monthly["reported"]]
    rsf_annual = pd.read_csv(processed / "annual_national.csv")
    rsf_annual = rsf_annual[rsf_annual["coverage"] == "full year"]

    payload = {
        "brta": {
            "source_url": "https://brta.gov.bd/pages/static-pages/6922de76933eb65569e1ac54",
            "fields": ["year", "month", "division", "accidents", "deaths", "injuries"],
            "rows": div[["year", "month", "division", "accidents", "deaths", "injuries"]].values.tolist(),
            "vehicle_fields": ["year", "month", "group", "deaths"],
            "vehicle": vehicle.values.tolist(),
        },
        "rsf": {
            "monthly_fields": ["year", "month", "accidents", "deaths", "injuries"],
            "monthly": as_int_rows(rsf_monthly, ["year", "month", "accidents", "deaths", "injuries"]),
            "annual_fields": ["year", "accidents", "deaths", "injuries"],
            "annual": as_int_rows(rsf_annual, ["year", "accidents", "deaths", "injuries"]),
        },
        "population": {k: int(v) for k, v in pop.items()},
    }
    (OUT / "accidents.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return len(div)


HIGHWAY_BN = {
    "N1": "ঢাকা–চট্টগ্রাম–কক্সবাজার", "N2": "ঢাকা–সিলেট–তামাবিল", "N3": "ঢাকা–ময়মনসিংহ",
    "N4": "জয়দেবপুর–টাঙ্গাইল–জামালপুর", "N405": "এলেঙ্গা–বঙ্গবন্ধু সেতু", "N5": "ঢাকা–আরিচা–রংপুর–বাংলাবান্ধা",
    "N6": "কাশিনাথপুর–রাজশাহী–সোনামসজিদ", "N7": "দৌলতদিয়া–খুলনা–মোংলা", "N8": "ঢাকা–মাওয়া–বরিশাল–পটুয়াখালী",
    "N805": "ভাঙ্গা–গোপালগঞ্জ–খুলনা",
}
# All 64 districts: Bangla name and division.
DISTRICTS = {
    "Dhaka": ("ঢাকা", "Dhaka"), "Faridpur": ("ফরিদপুর", "Dhaka"), "Gazipur": ("গাজীপুর", "Dhaka"),
    "Gopalganj": ("গোপালগঞ্জ", "Dhaka"), "Kishoreganj": ("কিশোরগঞ্জ", "Dhaka"), "Madaripur": ("মাদারীপুর", "Dhaka"),
    "Manikganj": ("মানিকগঞ্জ", "Dhaka"), "Munshiganj": ("মুন্সীগঞ্জ", "Dhaka"), "Narayanganj": ("নারায়ণগঞ্জ", "Dhaka"),
    "Narsingdi": ("নরসিংদী", "Dhaka"), "Rajbari": ("রাজবাড়ী", "Dhaka"), "Shariatpur": ("শরীয়তপুর", "Dhaka"),
    "Tangail": ("টাঙ্গাইল", "Dhaka"),
    "Bandarban": ("বান্দরবান", "Chattogram"), "Brahmanbaria": ("ব্রাহ্মণবাড়িয়া", "Chattogram"),
    "Chandpur": ("চাঁদপুর", "Chattogram"), "Chattogram": ("চট্টগ্রাম", "Chattogram"), "Cumilla": ("কুমিল্লা", "Chattogram"),
    "Cox's Bazar": ("কক্সবাজার", "Chattogram"), "Feni": ("ফেনী", "Chattogram"), "Khagrachhari": ("খাগড়াছড়ি", "Chattogram"),
    "Lakshmipur": ("লক্ষ্মীপুর", "Chattogram"), "Noakhali": ("নোয়াখালী", "Chattogram"), "Rangamati": ("রাঙ্গামাটি", "Chattogram"),
    "Bogura": ("বগুড়া", "Rajshahi"), "Joypurhat": ("জয়পুরহাট", "Rajshahi"), "Naogaon": ("নওগাঁ", "Rajshahi"),
    "Natore": ("নাটোর", "Rajshahi"), "Chapainawabganj": ("চাঁপাইনবাবগঞ্জ", "Rajshahi"), "Pabna": ("পাবনা", "Rajshahi"),
    "Rajshahi": ("রাজশাহী", "Rajshahi"), "Sirajganj": ("সিরাজগঞ্জ", "Rajshahi"),
    "Bagerhat": ("বাগেরহাট", "Khulna"), "Chuadanga": ("চুয়াডাঙ্গা", "Khulna"), "Jashore": ("যশোর", "Khulna"),
    "Jhenaidah": ("ঝিনাইদহ", "Khulna"), "Khulna": ("খুলনা", "Khulna"), "Kushtia": ("কুষ্টিয়া", "Khulna"),
    "Magura": ("মাগুরা", "Khulna"), "Meherpur": ("মেহেরপুর", "Khulna"), "Narail": ("নড়াইল", "Khulna"),
    "Satkhira": ("সাতক্ষীরা", "Khulna"),
    "Barguna": ("বরগুনা", "Barishal"), "Barishal": ("বরিশাল", "Barishal"), "Bhola": ("ভোলা", "Barishal"),
    "Jhalokati": ("ঝালকাঠি", "Barishal"), "Patuakhali": ("পটুয়াখালী", "Barishal"), "Pirojpur": ("পিরোজপুর", "Barishal"),
    "Habiganj": ("হবিগঞ্জ", "Sylhet"), "Moulvibazar": ("মৌলভীবাজার", "Sylhet"), "Sunamganj": ("সুনামগঞ্জ", "Sylhet"),
    "Sylhet": ("সিলেট", "Sylhet"),
    "Dinajpur": ("দিনাজপুর", "Rangpur"), "Gaibandha": ("গাইবান্ধা", "Rangpur"), "Kurigram": ("কুড়িগ্রাম", "Rangpur"),
    "Lalmonirhat": ("লালমনিরহাট", "Rangpur"), "Nilphamari": ("নীলফামারী", "Rangpur"), "Panchagarh": ("পঞ্চগড়", "Rangpur"),
    "Rangpur": ("রংপুর", "Rangpur"), "Thakurgaon": ("ঠাকুরগাঁও", "Rangpur"),
    "Jamalpur": ("জামালপুর", "Mymensingh"), "Mymensingh": ("ময়মনসিংহ", "Mymensingh"), "Netrokona": ("নেত্রকোনা", "Mymensingh"),
    "Sherpur": ("শেরপুর", "Mymensingh"),
}
# Boundary file spellings -> current official spellings.
DISTRICT_FIX = {
    "Barisal": "Barishal", "Bogra": "Bogura", "Brahamanbaria": "Brahmanbaria", "Chittagong": "Chattogram",
    "Comilla": "Cumilla", "Jessore": "Jashore", "Maulvibazar": "Moulvibazar", "Nawabganj": "Chapainawabganj",
    "Netrakona": "Netrokona",
}


def simplify(ring, tol):
    """Douglas-Peucker on one ring of [lng, lat] points."""
    if len(ring) < 4:
        return ring
    (x1, y1), (x2, y2) = ring[0], ring[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = (dx * dx + dy * dy) ** 0.5
    def dist(p):
        if norm == 0:
            return ((p[0] - x1) ** 2 + (p[1] - y1) ** 2) ** 0.5
        return abs(dy * p[0] - dx * p[1] + x2 * y1 - y2 * x1) / norm
    i, d = max(((i, dist(p)) for i, p in enumerate(ring[1:-1], 1)), key=lambda t: t[1])
    if d <= tol:
        return [ring[0], ring[-1]]
    return simplify(ring[:i + 1], tol)[:-1] + simplify(ring[i:], tol)


def polygons(geometry):
    return geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]


def contains(geometry, lng, lat):
    """Point in (multi)polygon, even-odd rule over all rings."""
    inside = False
    for poly in polygons(geometry):
        for ring in poly:
            for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
                if (y1 > lat) != (y2 > lat) and lng < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
                    inside = not inside
    return inside


def ring_area(ring):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1])) / 2


def centroid(ring):
    a = ring_area(ring)
    terms = [(x1 * y2 - x2 * y1, x1 + x2, y1 + y2) for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1])]
    return sum(c * x for c, x, _ in terms) / (6 * a), sum(c * y for c, _, y in terms) / (6 * a)


def load_districts():
    geo = json.loads((ROOT / "data/raw/geo/districts.geojson").read_text())
    for f in geo["features"]:
        raw = f["properties"]["shapeName"]
        f["properties"] = {"name": DISTRICT_FIX.get(raw, raw)}
    assert {f["properties"]["name"] for f in geo["features"]} == set(DISTRICTS)
    return geo


def build_districts(geo, spot_counts):
    # Check each district's division against the division boundaries.
    divisions = json.loads((OUT / "divisions.geojson").read_text())["features"]
    out = []
    for f in geo["features"]:
        name = f["properties"]["name"]
        bn_name, division = DISTRICTS[name]
        lng, lat = centroid(max((poly[0] for poly in polygons(f["geometry"])), key=lambda r: abs(ring_area(r))))
        hits = [d["properties"]["name"] for d in divisions if contains(d["geometry"], lng, lat)]
        assert hits in ([division], []), (name, division, hits)
        rings = [[[[round(x, 4), round(y, 4)] for x, y in simplify(r, 0.004)] for r in poly] for poly in polygons(f["geometry"])]
        rings = [[r for r in poly if len(r) >= 4] for poly in rings]
        rings = [poly for poly in rings if poly]
        out.append({"type": "Feature", "properties": {
            "name": name, "name_bn": bn_name, "division": division, "spots": spot_counts.get(name, 0)},
            "geometry": {"type": "MultiPolygon", "coordinates": rings}})
    (OUT / "districts.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": out}, ensure_ascii=False, separators=(",", ":")))


def build_spots(districts):
    spots = pd.read_csv(ROOT / "data/raw/deadly_roads/blackspots.csv")
    assert set(spots["highway"]) <= set(HIGHWAY_BN), set(spots["highway"]) - set(HIGHWAY_BN)
    # A spot listed under two districts ("Dhaka / Manikganj") goes to the district its point falls in.
    def district_of(r):
        if r.district in DISTRICTS:
            return r.district
        hit = [f["properties"]["name"] for f in districts["features"] if contains(f["geometry"], r.lng, r.lat)]
        assert len(hit) == 1 and hit[0] in r.district, (r.name_place, r.district, hit)
        return hit[0]
    spots["district_key"] = [district_of(r) for r in spots.itertuples()]
    # Located at a km post or routed along the highway = exact; upazila centre or estimate = approximate.
    exact = spots["lat_lng_source"].str.contains(r"km post|routed", case=False) & \
        ~spots["lat_lng_source"].str.contains("not located", case=False)
    records = [
        {
            "lat": round(r.lat, 5), "lng": round(r.lng, 5), "highway": r.highway,
            "place": r.name_place, "district": DISTRICTS[r.district_key][0], "district_key": r.district_key,
            "year": int(r.year_listed),
            "detail": None if pd.isna(r.severity_or_rank) else r.severity_or_rank,
            "exact": bool(e), "source_url": r.source_url,
        }
        for r, e in zip(spots.itertuples(), exact)
    ]
    payload = {"highways": HIGHWAY_BN, "spots": records}
    (OUT / "blackspots.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return len(records), int(exact.sum()), spots["district_key"].value_counts().to_dict()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_boundaries()
    n = build_accidents()
    districts = load_districts()
    n_spots, n_exact, spot_counts = build_spots(districts)
    build_districts(districts, spot_counts)
    print(f"wrote {OUT / 'divisions.geojson'}, {OUT / 'accidents.json'} ({n} rows), "
          f"{OUT / 'blackspots.json'} ({n_spots} spots, {n_exact} exact), "
          f"{OUT / 'districts.geojson'} ({len(districts['features'])} districts, {len(spot_counts)} with spots)")
