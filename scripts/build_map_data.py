"""Build the data files for the interactive map in docs/.

Reads the cleaned BRTA division table and the division boundaries, and writes:
  docs/data/divisions.geojson   boundaries with English and Bangla names
  docs/data/accidents.json      monthly accidents, deaths and injuries per division

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


def build_accidents():
    div = pd.read_csv(ROOT / "data/processed/brta_division.csv")
    pop = pd.read_csv(ROOT / "data/raw/division_population_2022.csv").set_index("division")["pop_2022"]
    assert set(div["division"]) == set(BANGLA)
    rows = div[["year", "month", "division", "accidents", "deaths", "injuries"]].values.tolist()
    payload = {
        "source": "BRTA monthly road accident reports",
        "source_url": "https://brta.gov.bd/pages/static-pages/6922de76933eb65569e1ac54",
        "fields": ["year", "month", "division", "accidents", "deaths", "injuries"],
        "rows": rows,
        "population": {k: int(v) for k, v in pop.items()},
    }
    (OUT / "accidents.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return len(rows)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_boundaries()
    n = build_accidents()
    print(f"wrote {OUT / 'divisions.geojson'} and {OUT / 'accidents.json'} ({n} rows)")
