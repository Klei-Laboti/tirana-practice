import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("output/apartments_rated.csv")

colors = {"GREAT DEAL": "#2ecc71", "FAIR": "#f39c12", "OVERPRICED": "#e74c3c"}

plt.figure(figsize=(10, 6))
for rating, color in colors.items():
    subset = df[df["deal_rating"] == rating]
    plt.scatter(subset["sqm"], subset["price"], c=color, label=rating,
                alpha=0.7, edgecolors="#0b1f33", s=60)

plt.title("Price vs Size — Tirana Apartments")
plt.xlabel("Size (m2)")
plt.ylabel("Price (EUR)")
plt.legend()
plt.tight_layout()
plt.savefig("output/scatter_price_vs_size.png", dpi=150)
print("Saved -> output/scatter_price_vs_size.png")
