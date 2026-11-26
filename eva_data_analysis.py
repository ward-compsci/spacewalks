import matplotlib.pyplot as plt
import pandas as pd

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open("./eva-data.json", "r", encoding="ascii")  # Force encoding for Windows
output_file = open("./eva-data.csv", "w", encoding="utf-8")
GRAPH_FILE = "./cumulative_eva_graph.png"

# Load json into Pandas dataframe
eva_df = pd.read_json(input_file, convert_dates=["date"], encoding="ascii")
eva_df["eva"] = eva_df["eva"].astype(float)
# Remove rows where `duration` or `date` is missing or invalid
eva_df.dropna(axis=0, subset=["duration", "date"], inplace=True)

# Write formatted input to csv
eva_df.to_csv(output_file, index=False, encoding="utf-8")

eva_df.sort_values("date", inplace=True)

# Calculate cumulative time spent in space
eva_df["duration_hours"] = eva_df["duration"].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_df["cumulative_time"] = eva_df["duration_hours"].cumsum()

plt.plot(eva_df["date"], eva_df["cumulative_time"], "ko-") # Solid black line
plt.xlabel("Year")
plt.ylabel("Total time spent in space to date (hours)")
plt.tight_layout()
plt.savefig(GRAPH_FILE)
plt.show()
