import pandas as pd

df = pd.read_csv("data/apartments.csv")

# Average price per sqm by zone
print("=== Average Price per m2 by Zone ===")
zone_avg = df.groupby("zone")["price_per_sqm"].mean().sort_values()
for zone, avg in zone_avg.items():
    print(f"  {zone:20s} {avg:,.0f} EUR/m2")

# Overall average
overall_avg = df["price_per_sqm"].mean()
print(f"\n  Overall average: {overall_avg:,.0f} EUR/m2")

# Find deals (below 90% of overall average)
threshold = overall_avg * 0.9
deals = df[df["price_per_sqm"] < threshold].copy()
deals = deals.sort_values("price_per_sqm")

print(f"\n=== Best Deals (below {threshold:,.0f} EUR/m2) ===")
print(f"Found {len(deals)} apartments:\n")
for _, row in deals.head(10).iterrows():
    print(f"  {row['zone']:20s} | {row['rooms']}R | {row['sqm']}m2 | {row['price']:>10,} EUR | {row['price_per_sqm']:,} EUR/m2")

# Save deals to CSV
deals.to_csv("output/best_deals.csv", index=False)
print(f"\nSaved {len(deals)} deals -> output/best_deals.csv")
