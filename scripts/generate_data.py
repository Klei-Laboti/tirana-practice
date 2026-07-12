import pandas as pd
import random

random.seed(42)

# Cdo zone ka nje cmim baze per m2 (Blloku me i shtrenjte)
zone_base = {
    "Bllok": 2200,
    "Komuna e Parisit": 1900,
    "21 Dhjetori": 1600,
    "Selvia": 1500,
    "Ali Demi": 1250,
    "Medreseja": 1200,
    "Fresk": 1100,
    "Kinostudio": 1050,
    "Astir": 1000,
    "Yzberisht": 900,
}

rows = []
for _ in range(120):
    zone = random.choice(list(zone_base.keys()))
    bedrooms = random.randint(1, 4)
    sqm = random.randint(35 + bedrooms * 12, 55 + bedrooms * 25)
    bathrooms = 1 if bedrooms <= 2 else random.choice([1, 2])
    floor = random.randint(1, 10)

    ppsm = zone_base[zone]
    ppsm += bathrooms * 40      # banjo shtese rrit vleren
    ppsm += floor * 8           # kati me i larte pak me i shtrenjte
    ppsm += random.randint(-120, 120)   # zhurma e tregut

    price = int(round(sqm * ppsm, -2))

    rows.append({
        "zone": zone,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "floor": floor,
        "sqm": sqm,
        "price": price,
        "price_per_sqm": ppsm,
    })

df = pd.DataFrame(rows)
df.to_csv("data/apartments.csv", index=False)
print(f"Generated {len(df)} apartments -> data/apartments.csv")
print(df.head().to_string(index=False))
