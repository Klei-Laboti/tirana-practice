import pandas as pd

df = pd.read_csv("data/apartments.csv")

rooms = int(input("How many rooms? "))
filtered = df[df["rooms"] == rooms].sort_values("price_per_sqm")

print(f"\n=== {len(filtered)} apartments with {rooms} room(s) ===\n")
for _, row in filtered.iterrows():
    print(f"  {row['zone']:20s} | {row['sqm']}m2 | {row['price']:>10,} EUR | {row['price_per_sqm']:,} EUR/m2")

filtered.to_csv(f"output/apartments_{rooms}rooms.csv", index=False)
print(f"\nSaved -> output/apartments_{rooms}rooms.csv")
