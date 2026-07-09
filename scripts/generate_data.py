"""Generate fake apartment listing data for Tirana."""

import csv
import os
import random

random.seed(42)

ZONES = ["Bllok", "Komuna e Parisit", "Ali Demi", "Astir",
         "Yzberisht", "Don Bosko", "Fresku", "21 Dhjetori"]

LISTINGS = []
for _ in range(50):
    zone = random.choice(ZONES)
    rooms = random.randint(1, 4)
    sqm = random.randint(40, 130)
    price = round(sqm * random.uniform(800, 2200) + random.gauss(0, 5000))
    LISTINGS.append({
        "zone": zone,
        "rooms": rooms,
        "sqm": sqm,
        "price": price
    })

os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "apartments.csv")

with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["zone", "rooms", "sqm", "price"])
    writer.writeheader()
    writer.writerows(LISTINGS)

print(f"Generated {len(LISTINGS)} listings -> {output_path}")
