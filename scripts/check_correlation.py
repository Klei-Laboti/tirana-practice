"""
Provon pse feature importance tregon bedrooms me lart se sqm.
Hipoteza: sqm gjenerohet nga bedrooms, pra jane te korreluara.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/apartments.csv")

cols = ["sqm", "bedrooms", "bathrooms", "floor", "price"]
corr = df[cols].corr()

print("=== Matrica e korrelacionit ===\n")
print(corr.round(3).to_string())

print("\n=== Korrelacionet kryesore me price ===")
for c in ["sqm", "bedrooms", "bathrooms", "floor"]:
    print(f"  {c:12s} {corr.loc[c, 'price']:>7.3f}")

print(f"\nsqm <-> bedrooms: {corr.loc['sqm', 'bedrooms']:.3f}")
print("Nese ky numer eshte i larte (>0.7), features mbivendosen -")
print("modeli mund t'i japi meritat njerit ne vend te tjetrit.\n")

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(corr, cmap="RdYlBu_r", vmin=-1, vmax=1)

ax.set_xticks(range(len(cols)))
ax.set_yticks(range(len(cols)))
ax.set_xticklabels(cols, rotation=45, ha="right")
ax.set_yticklabels(cols)

for i in range(len(cols)):
    for j in range(len(cols)):
        val = corr.iloc[i, j]
        color = "white" if abs(val) > 0.6 else "black"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                color=color, fontsize=10)

plt.colorbar(im, label="Korrelacioni")
plt.title("Korrelacioni mes features")
plt.tight_layout()
plt.savefig("output/correlation_matrix.png", dpi=150)
print("Saved -> output/correlation_matrix.png")