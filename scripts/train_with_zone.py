import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

df = pd.read_csv("data/apartments.csv")

# PA zone
f1 = ["sqm", "bedrooms", "bathrooms", "floor"]
X1 = df[f1]

# ME zone (one-hot encoding: cdo zone behet nje kolone 0/1)
X2 = pd.get_dummies(df[f1 + ["zone"]], columns=["zone"])

y = df["price"]

print(f"Features PA zone: {X1.shape[1]}")
print(f"Features ME zone: {X2.shape[1]}\n")

results = []
for name, X in [("PA zone", X1), ("ME zone", X2)]:
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    m = LinearRegression()
    m.fit(X_tr, y_tr)
    pred = m.predict(X_te)
    results.append((name, r2_score(y_te, pred), mean_absolute_error(y_te, pred)))

print("=== Sa rendesi ka nje feature i vetem? ===")
print(f"{'Model':12s} {'R2':>8s} {'MAE (EUR)':>14s}")
print("-" * 36)
for name, r2, mae in results:
    print(f"{name:12s} {r2:>8.3f} {mae:>14,.0f}")
