from flask import Flask, render_template, abort
import pandas as pd

app = Flask(__name__)


def load_listings():
    return pd.read_csv("data/apartments.csv")


@app.route("/")
def home():
    df = load_listings()
    listings = df.to_dict(orient="records")
    return render_template("index.html", listings=listings, count=len(listings))


@app.route("/listing/<int:id>")
def listing_detail(id):
    df = load_listings()
    if id < 0 or id >= len(df):
        abort(404)
    listing = df.iloc[id].to_dict()
    return render_template("listing.html", listing=listing, id=id)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
