from pathlib import Path

import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

data_file = Path(__file__).parent / "../../data/merged_sfpd.csv"
df = pd.read_csv(data_file)

lat, lon = 37.7749, -122.4194

# Parse date safely
drugs = df[df["incident_category"] == "drug/narcotic"].copy()
drugs["incident_date"] = pd.to_datetime(drugs["incident_date"], errors="coerce")

# monthly aggregation across the full dataset time range
start_month = (
    pd.to_datetime("01-03-2003", format="%d-%m-%Y").to_period("M").to_timestamp()
)
end_month = (
    pd.to_datetime("01-03-2024", format="%d-%m-%Y").to_period("M").to_timestamp()
)
all_months = pd.date_range(start=start_month, end=end_month, freq="MS")

# Build HeatMapWithTime structure: list of frames, each frame is list of [lat, lon]
drugs_time = []
labels = []

for month in all_months:
    month_points = drugs.loc[
        drugs["incident_date"].dt.to_period("M") == month.to_period("M"),
        ["latitude", "longitude"],
    ].dropna()
    drugs_time.append(month_points.values.tolist())
    labels.append(month.strftime("%b %Y"))

# Fallback if no data in selected week
if not any(len(frame) for frame in drugs_time):
    raise ValueError("No drug/narcotic incidents found for year=2025 and ISO week=10.")

m = folium.Map([lat, lon], zoom_start=12, tiles="CartoDB positron")

HeatMapWithTime(
    data=drugs_time,
    index=labels,
    auto_play=True,
    max_opacity=0.8,
    radius=18,
    min_speed=5,
    gradient={0.3: "#d39eda", 1: "#c71dd6"},
).add_to(m)

out_file = Path(__file__).parent / "heatmap_with_time.html"
m.save(out_file.as_posix())
