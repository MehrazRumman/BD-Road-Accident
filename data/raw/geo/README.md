# Boundaries

`divisions.geojson`: the 8 divisions of Bangladesh (simplified), from
[geoBoundaries](https://www.geoboundaries.org) ADM1, CC BY 4.0, as packaged in
[Deadly Roads: Bangladesh 2000–2025](https://github.com/ahasan722/bangladesh-road-crashes-2000-2025)
(`assets/basemap/divisions.geojson`). Copied unchanged; three names use older spellings
(Chittagong, Rajshani, Barisal) and are normalised by `scripts/build_map_data.py`.

`districts.geojson`: the 64 districts (geoBoundaries ADM2, simplified release, downloaded 2026-10-21 from
[wmgeolab/geoBoundaries](https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/BGD/ADM2/geoBoundaries-BGD-ADM2_simplified.geojson)).
Source: Bangladesh Bureau of Statistics and OCHA ROAP, licensed
[CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/). Copied unchanged; older spellings (Bogra, Comilla,
Jessore, ...) are normalised and the geometry simplified further by `scripts/build_map_data.py`.
