import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/apartments.csv")

# 1. Histogram of price per sqm
plt.figure(figsize=(10, 5))
plt.hist(df["price_per_sqm"], bins=20, color="#12a1a8", edgecolor="#0b1f33")
plt.axvline(df["price_per_sqm"].mean(), color="red", linestyle="--", label="Average")
plt.title("Distribution of Price per m2 in Tirana")
plt.xlabel("Price per m2 (EUR)")
plt.ylabel("Number of Apartments")
plt.legend()
plt.tight_layout()
plt.savefig("output/price_distribution.png", dpi=150)
print("Saved -> output/price_distribution.png")

# 2. Bar chart of average price per zone
plt.figure(figsize=(10, 6))
zone_avg = df.groupby("zone")["price_per_sqm"].mean().sort_values()
bars = plt.barh(zone_avg.index, zone_avg.values, color="#12a1a8", edgecolor="#0b1f33")
plt.axvline(df["price_per_sqm"].mean(), color="red", linestyle="--", label="Overall Average")
plt.title("Average Price per m2 by Zone")
plt.xlabel("Price per m2 (EUR)")
plt.legend()
plt.tight_layout()
plt.savefig("output/zone_comparison.png", dpi=150)
print("Saved -> output/zone_comparison.png")
