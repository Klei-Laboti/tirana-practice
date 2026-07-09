import pandas as pd
import random

random.seed(42)

zones = ["Bllok", "Komuna e Parisit", "Ali Demi", "Astir", "Yzberisht",
         "21 Dhjetori", "Fresk", "Medreseja", "Selvia", "Kinostudio"]

apartments = []
for _ in range(100):
    zone = random.choice(zones)
    rooms = random.randint(1, 4)
    sqm = random.randint(40, 150)
    price_per_sqm = random.randint(800, 2500)
    price = sqm * price_per_sqm
    apartments.append({
        "zone": zone,
        "rooms": rooms,
        "sqm": sqm,
        "price": price,
        "price_per_sqm": price_per_sqm
    })

df = pd.DataFrame(apartments)
df.to_csv("data/apartments.csv", index=False)
print(f"Generated {len(df)} apartments -> data/apartments.csv")
