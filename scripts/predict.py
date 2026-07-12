import joblib
import pandas as pd

# Ngarko modelin e ruajtur (pa e ritrajnuar!)
model = joblib.load("models/price_model.joblib")
print("Model loaded from models/price_model.joblib\n")

# Nje apartament i sajuar
apartment = pd.DataFrame([{
    "sqm": 85,
    "bedrooms": 2,
    "bathrooms": 1,
    "floor": 4,
}])

print("=== Apartment ===")
print(apartment.to_string(index=False))

predicted = model.predict(apartment)[0]
print(f"\nPredicted price: {predicted:,.0f} EUR")
print(f"Price per m2:    {predicted / 85:,.0f} EUR/m2")
