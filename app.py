from flask import Flask, render_template, abort
import pandas as pd
import joblib
import os

app = Flask(__name__)

MODEL_PATH = "models/price_model.joblib"
FEATURES = ["sqm", "bedrooms", "bathrooms", "floor"]


def load_listings():
    return pd.read_csv("data/apartments.csv")


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def grade(price_per_sqm, avg):
    if price_per_sqm < avg * 0.85:
        return "deal", "Oferte"
    elif price_per_sqm > avg * 1.15:
        return "high", "I shtrenjte"
    return "fair", "Normal"


def build_listings(df, avg):
    items = []
    for i, row in df.iterrows():
        css_class, label = grade(row["price_per_sqm"], avg)
        item = row.to_dict()
        item["id"] = i
        item["badge_class"] = css_class
        item["badge_label"] = label
        items.append(item)
    return items


@app.route("/")
def home():
    df = load_listings()
    avg = df["price_per_sqm"].mean()
    listings = build_listings(df, avg)
    stats = {
        "count": len(df),
        "avg_sqm": round(avg),
        "avg_price": round(df["price"].mean()),
        "zones": df["zone"].nunique(),
    }
    return render_template("index.html", listings=listings, stats=stats)


@app.route("/good-deals")
def good_deals():
    df = load_listings()
    avg = df["price_per_sqm"].mean()
    cheap = df[df["price_per_sqm"] < avg]
    listings = build_listings(cheap, avg)
    stats = {
        "count": len(listings),
        "avg_sqm": round(avg),
        "avg_price": round(cheap["price"].mean()) if len(cheap) else 0,
        "zones": cheap["zone"].nunique(),
    }
    return render_template("index.html", listings=listings, stats=stats)


@app.route("/listing/<int:id>")
def listing_detail(id):
    df = load_listings()
    if id < 0 or id >= len(df):
        abort(404)

    avg = df["price_per_sqm"].mean()
    row = df.iloc[id]
    css_class, label = grade(row["price_per_sqm"], avg)

    listing = row.to_dict()
    listing["badge_class"] = css_class
    listing["badge_label"] = label

    predicted = None
    diff_pct = None
    model = load_model()
    if model is not None:
        X = pd.DataFrame([{f: row[f] for f in FEATURES}])
        predicted = round(float(model.predict(X)[0]))
        diff_pct = round((predicted - row["price"]) / predicted * 100, 1)

    return render_template(
        "listing.html",
        listing=listing,
        id=id,
        avg=round(avg),
        predicted=predicted,
        diff_pct=diff_pct,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
