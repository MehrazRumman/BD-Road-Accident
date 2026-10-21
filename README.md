# Bangladesh Road Accidents 2021–2026

![Python](https://img.shields.io/badge/Python-3-blue) ![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![pandas](https://img.shields.io/badge/pandas-matplotlib-150458)

An analysis of road accidents in Bangladesh from **January 2021 to September 2026**. The project collects
Road Safety Foundation figures published in the press, cleans them into source-linked tables, and analyses deaths by
year, vehicle type, division and time of year in Jupyter notebooks.

| 2025 at a glance | |
|---|---|
| Road deaths | **7,359** (about 20 a day) |
| Accidents | **7,584** |
| Injured | **16,476** |
| Motorcycle share of deaths | **36%** |

![Road deaths per year](figures/01_deaths_per_year.png)

## Data

All figures are from the **Road Safety Foundation (RSF)**, a Bangladeshi NGO that counts road accidents reported by
national newspapers, online portals and TV, and publishes monthly and annual reports. RSF does not publish a
downloadable dataset, so the numbers are transcribed from the press articles that reproduce its reports.

| Source | Used for |
|---|---|
| [Deadly Roads: Bangladesh 2000–2025](https://github.com/ahasan722/bangladesh-road-crashes-2000-2025) (CC BY 4.0) | Most RSF annual, monthly and breakdown figures, each with its press citation |
| `data/raw/rsf_manual_additions.csv` | Extra RSF months for 2021–2022, checked against the original articles |
| BBS Census 2022 | Population by division |

Every row in `data/processed/` has a `source` and a `source_url` column pointing to the article it came from.

### Processed tables

| File | Contents |
|---|---|
| `monthly_national.csv` | Accidents, deaths, injuries per month (69 months; 49 with a report) |
| `annual_national.csv` | Annual totals 2021–2025, plus a partial 2026 |
| `vehicle_deaths.csv` | Deaths by vehicle type (motorcycle, three-wheeler, bus, truck, ...) |
| `division.csv` | Accidents, deaths or share of accidents by division |
| `time_of_day.csv` | Share of accidents by time of day |
| `eid_periods.csv` | Accidents and deaths during Eid travel windows |

## Project structure

```
BD-Road-Accident/
├── data/
│   ├── raw/                  # source data as collected (never edited by hand after download)
│   │   ├── deadly_roads/     # RSF figures from the Deadly Roads project, with citations
│   │   ├── rsf_manual_additions.csv
│   │   └── division_population_2022.csv
│   └── processed/            # clean tables written by 01_data_cleaning.ipynb
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   └── 02_analysis.ipynb
├── figures/                  # charts saved by 02_analysis.ipynb
└── requirements.txt
```

## Notebooks

1. [`notebooks/01_data_cleaning.ipynb`](notebooks/01_data_cleaning.ipynb): loads the raw files, fixes wrong
   years, removes duplicates and other organisations' figures, checks coverage and consistency, and writes the
   processed tables.
2. [`notebooks/02_analysis.ipynb`](notebooks/02_analysis.ipynb): deaths by year, vehicle type, division, month,
   season, Eid and time of day.

## Key findings

- Road deaths rose from **6,284 (2021) to 7,359 (2025)**, about 20 a day. 2026 is running about 15% lower than
  2025 for the same months.
- **Motorcycles account for 35–40% of all road deaths** every year. Three-wheelers come second.
- Accidents broadly follow population across divisions. **Dhaka** has the most, and **Rajshahi** has more than its
  population share would suggest.
- Deaths per day are **highest from January to July** and lowest from August to October. **Eid travel** windows
  have 26–51% more deaths per day than normal.

## Charts

### By year

| | |
|---|---|
| ![Deaths per year](figures/01_deaths_per_year.png) | ![Accidents, deaths and injuries indexed](figures/02_indexed_trend.png) |

### By vehicle

| | |
|---|---|
| ![Motorcycle deaths per year](figures/03_motorcycle_deaths.png) | ![Deaths by vehicle type](figures/04_vehicle_mix.png) |

![Motorcycle share of monthly deaths](figures/05_motorcycle_share_monthly.png)

### By division

| | |
|---|---|
| ![Division share of accidents vs population](figures/06_division_share.png) | ![Division with fewest accidents](figures/07_division_lowest.png) |

### Time of year and day

![Deaths per day by month](figures/08_monthly_heatmap.png)

| | |
|---|---|
| ![Seasonal index](figures/09_seasonal_index.png) | ![Eid travel deaths](figures/10_eid.png) |

![Time of day](figures/11_time_of_day.png)

## Limitations

- RSF counts **media-reported** accidents only, so the real toll is higher. The WHO's modelled estimate for 2021 is
  about five times RSF's count.
- 20 of the 69 months have no RSF report that could be confirmed.
- Full vehicle-type and division tables exist only for the months the press reproduced them.

## Run it

```bash
git clone https://github.com/MehrazRumman/BD-Road-Accident.git
cd BD-Road-Accident
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

Run `01_data_cleaning.ipynb` first, then `02_analysis.ipynb`.
