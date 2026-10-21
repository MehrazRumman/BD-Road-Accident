"""Build the data files for the interactive map in docs/.

Reads the cleaned tables in data/processed/ and the division boundaries, and writes:
  docs/data/divisions.geojson   boundaries with English and Bangla names
  docs/data/accidents.json      BRTA monthly figures per division, BRTA deaths by vehicle group,
                                RSF national monthly and annual figures

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


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_boundaries()
    n = build_accidents()
    print(f"wrote {OUT / 'divisions.geojson'} and {OUT / 'accidents.json'} ({n} rows)")
