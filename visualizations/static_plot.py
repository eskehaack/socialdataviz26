from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data_file = Path(__file__).parent / "../../data/merged_sfpd.csv"
df = pd.read_csv(data_file)

date_col = "incident_date"
incident_category_col = "incident_category"

# clean/prepare
tmp = df.copy()
tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
tmp = tmp.dropna(subset=[date_col])

# filter to drug/narcotic incidents (case-insensitive)
drug = tmp[tmp["incident_category"] == "drug/narcotic"]

# monthly aggregation across the full dataset time range
start_month = (
    pd.to_datetime("01-03-2003", format="%d-%m-%Y").to_period("M").to_timestamp()
)
end_month = (
    pd.to_datetime("01-03-2024", format="%d-%m-%Y").to_period("M").to_timestamp()
)
all_months = pd.date_range(start=start_month, end=end_month, freq="MS")

monthly_counts = (
    drug.set_index(date_col).resample("MS").size().reindex(all_months, fill_value=0)
)

monthly_df = monthly_counts.rename_axis("month").reset_index(name="incident_count")
monthly_df["months_since_start"] = range(len(monthly_df))

# plot (calendar month + year on x-axis)
plt.figure(figsize=(12, 5))
plt.plot(
    monthly_df["month"], monthly_df["incident_count"], linewidth=1, color="#c71dd6"
)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45, ha="right")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.xlabel("Month")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.title("Monthly Drug/Narcotic Incidents in San Francisco (2003-2024)")
plt.savefig("figures/monthly_drug_incidents.png", dpi=300, bbox_inches="tight")
