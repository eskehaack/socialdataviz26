from pathlib import Path

import plotly.express as px
import pandas as pd


data_file = Path(__file__).parent / "../../data/merged_sfpd.csv"
df = pd.read_csv(data_file)

df = df[df["incident_category"] == "drug/narcotic"].copy()
df["hour"] = pd.to_datetime(
    df["incident_time"], format="%H:%M:%S", errors="coerce"
).dt.hour
groups = df.groupby(["incident_year", "hour"]).size()
groups = groups.reset_index(name="count")

fig = px.line(
    groups,
    x="hour",
    y="count",
    color="incident_year",
    labels={"hour": "Hour", "count": "Incident Count", "incident_year": "Year"},
    title="Drug/Narcotic Incidents by Hour and Year",
)

fig.update_traces(visible="legendonly")
fig.update_yaxes(showgrid=False)
fig.update_layout(
    {
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    }
)

fig.write_html(Path(__file__).parent / "interactive_plot.html")
