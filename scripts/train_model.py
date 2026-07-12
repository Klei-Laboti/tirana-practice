import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Ngarko te dhenat
df = pd.read_csv("data/apartments.csv")

# 2. Zgjidh features (X) dhe target (y)
features = ["sqm", "bedrooms", "bathrooms", "floor"]
X = df[features]
y = df["price"]

# 3. Ndaj ne train dhe test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training rows: {len(X_train)} | Test rows: {len(X_test)}\n")

# 4. Trajno modelin
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Vleresoje mbi te dhenat qe s'i ka pare kurre
predictions = model.predict(X_test)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print("=== Model Performance (test set) ===")
print(f"  R2 score:            {r2:.3f}")
print(f"  Mean Absolute Error: {mae:,.0f} EUR\n")

print("=== Coefficients ===")
for name, coef in zip(features, model.coef_):
    print(f"  {name:12s} {coef:>12,.0f} EUR")
print(f"  {'intercept':12s} {model.intercept_:>12,.0f} EUR\n")

# 6. Ruaje modelin
joblib.dump(model, "models/price_model.joblib")
print("Saved -> models/price_model.joblib")
