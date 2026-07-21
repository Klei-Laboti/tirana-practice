"""
Krahasim modelesh mbi te njejtat te dhena.
Nuk prek train_model.py as models/price_model.joblib.
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

RANDOM_STATE = 42
BASE_FEATURES = ["sqm", "bedrooms", "bathrooms", "floor"]

df = pd.read_csv("data/apartments.csv")
y = df["price"]

X_base = df[BASE_FEATURES]
X_zone = pd.get_dummies(df[BASE_FEATURES + ["zone"]], columns=["zone"])

print(f"Dataset: {len(df)} rreshta")
print(f"Features PA zone: {X_base.shape[1]} | ME zone: {X_zone.shape[1]}\n")

models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(
        n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1
    ),
    "XGBoost": XGBRegressor(
        n_estimators=150, learning_rate=0.05, max_depth=3,
        subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0,
        random_state=RANDOM_STATE, verbosity=0
    ),
    "LightGBM": LGBMRegressor(
        n_estimators=300, learning_rate=0.08, max_depth=4,
        min_child_samples=5, min_split_gain=0.0, num_leaves=15,
        random_state=RANDOM_STATE, verbose=-1
    ),
}

results = []
fitted = {}

for feature_set, X in [("PA zone", X_base), ("ME zone", X_zone)]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    for name, model in models.items():
        m = type(model)(**model.get_params())
        m.fit(X_train, y_train)
        pred = m.predict(X_test)

        results.append({
            "features": feature_set,
            "model": name,
            "r2": r2_score(y_test, pred),
            "mae": mean_absolute_error(y_test, pred),
            "rmse": mean_squared_error(y_test, pred) ** 0.5,
        })
        fitted[(feature_set, name)] = m

res = pd.DataFrame(results)

print("=" * 62)
print(f"{'Features':10s} {'Model':20s} {'R2':>8s} {'MAE':>11s} {'RMSE':>11s}")
print("=" * 62)
for _, r in res.iterrows():
    print(f"{r['features']:10s} {r['model']:20s} {r['r2']:>8.3f} "
          f"{r['mae']:>11,.0f} {r['rmse']:>11,.0f}")
print("=" * 62)

best = res.loc[res["r2"].idxmax()]
print(f"\nMe i miri: {best['model']} ({best['features']}) -> R2 = {best['r2']:.3f}\n")

res.to_csv("output/model_comparison.csv", index=False)
print("Saved -> output/model_comparison.csv")

best_model = fitted[(best["features"], best["model"])]
joblib.dump(best_model, "models/best_model.joblib")
print("Saved -> models/best_model.joblib")

fig, ax = plt.subplots(figsize=(10, 5.5))
names = list(models.keys())
x = np.arange(len(names))
w = 0.38

pa = [res[(res.model == n) & (res.features == "PA zone")]["r2"].values[0] for n in names]
me = [res[(res.model == n) & (res.features == "ME zone")]["r2"].values[0] for n in names]

b1 = ax.bar(x - w/2, pa, w, label="PA zone", color="#94a3b8", edgecolor="#0b1f33")
b2 = ax.bar(x + w/2, me, w, label="ME zone", color="#12a1a8", edgecolor="#0b1f33")

for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.015,
                f"{h:.3f}", ha="center", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel("R² score")
ax.set_ylim(min(0, min(pa) - 0.1), 1.08)
ax.axhline(0, color="#0b1f33", linewidth=0.8)
ax.set_title("Krahasimi i modeleve — me dhe pa zonen")
ax.legend()
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig("output/model_comparison.png", dpi=150)
print("Saved -> output/model_comparison.png")

xgb = fitted[("ME zone", "XGBoost")]
imp = pd.Series(xgb.feature_importances_, index=X_zone.columns).sort_values()

plt.figure(figsize=(9, 7))
plt.barh(imp.index, imp.values, color="#12a1a8", edgecolor="#0b1f33")
plt.title("Feature importance — XGBoost (me zone)")
plt.xlabel("Rendesia relative")
plt.tight_layout()
plt.savefig("output/feature_importance.png", dpi=150)
print("Saved -> output/feature_importance.png")