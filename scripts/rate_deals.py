import pandas as pd

df = pd.read_csv("data/apartments.csv")

avg = df["price_per_sqm"].mean()

def rate(price_per_sqm):
    if price_per_sqm < avg * 0.85:
        return "GREAT DEAL"
    elif price_per_sqm > avg * 1.15:
        return "OVERPRICED"
    else:
        return "FAIR"

df["deal_rating"] = df["price_per_sqm"].apply(rate)

print("=== Deal Rating Summary ===")
print(df["deal_rating"].value_counts().to_string())

print(f"\n=== Top 10 GREAT DEALS ===\n")
greats = df[df["deal_rating"] == "GREAT DEAL"].sort_values("price_per_sqm")
for _, row in greats.head(10).iterrows():
    print(f"  {row['zone']:20s} | {row['rooms']}R | {row['sqm']}m2 | {row['price']:>10,} EUR | {row['price_per_sqm']:,} EUR/m2")

df.to_csv("output/apartments_rated.csv", index=False)
print(f"\nSaved {len(df)} apartments with ratings -> output/apartments_rated.csv")
