# BRTA monthly road accident reports

Official monthly reports from the **Bangladesh Road Transport Authority (BRTA)**, published on
[brta.gov.bd](https://brta.gov.bd/pages/static-pages/6922de76933eb65569e1ac54) as scanned PDF letters, one per
month, January 2023 to September 2026 (45 months, none missing).

BRTA collects the figures through its divisional offices. They are usually lower than the Road Safety Foundation
(RSF) counts, which come from news reports, so the two series are kept separate.

The PDFs are scanned images, so page 1 of each report was transcribed by hand:

| File | Contents |
|---|---|
| `../brta_monthly_reports.csv` | Accidents, deaths and injuries for each of the 8 divisions plus the printed total, every month |
| `../brta_vehicle_deaths.csv` | Deaths by vehicle type (13 categories), March 2023 onward |

**Checks.** For every month, the 8 division rows add up to the printed total for accidents, deaths and injuries,
and the vehicle deaths add up to the printed death total. Three reports have vehicle figures that do not add up in
the original document itself (Feb, Apr and May 2025, off by 1–2 deaths). They are kept as printed and flagged in
the `note` column.

Every row links to the PDF it came from in `source_url`.
