# Deadly Roads: Bangladesh 2000–2025 (upstream data)

These three CSVs are copied unchanged from
[ahasan722/bangladesh-road-crashes-2000-2025](https://github.com/ahasan722/bangladesh-road-crashes-2000-2025)
(`data/raw/`, downloaded 2026-10-21), licensed CC BY 4.0. See `LICENSE.txt`.

| File | Contents |
|---|---|
| `monthly.csv` | Monthly accidents / deaths / injuries from RSF, BJKS and SCRF press reports |
| `national_yearly.csv` | Annual national series from police, RSF, BJKS, WHO and others |
| `breakdowns.csv` | Long-format breakdowns (vehicle, victim, division, time of day, road class, ...) |

Every row carries the `citation_url` of the press article it was transcribed from.
The figures themselves belong to their publishers (mainly the Road Safety Foundation).

Known issues in these files are fixed in `notebooks/01_data_cleaning.ipynb`, not here.
