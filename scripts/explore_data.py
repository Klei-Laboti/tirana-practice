import pandas as pd

df = pd.read_csv("data/apartments.csv")

print("=== Shape ===")
print(f"{df.shape[0]} rows, {df.shape[1]} columns\n")

print("=== First 5 rows ===")
print(df.head().to_string(index=False))

print("\n=== Data Types ===")
print(df.dtypes)

print("\n=== Summary Statistics ===")
print(df.describe().round(1).to_string())

print("\n=== Apartments per Zone ===")
print(df["zone"].value_counts().to_string())
