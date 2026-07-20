from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


def load_listings():
    df = pd.read_csv("data/apartments.csv")
    return df


@app.route("/")
def home():
    df = load_listings()
    listings = df.to_dict(orient="records")
    return render_template("index.html", listings=listings, count=len(listings))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
