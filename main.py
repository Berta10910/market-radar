from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prices import get_prices
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Market Radar API running"}

@app.get("/prices")
def prices():
    return get_prices()

@app.get("/alerts")
def alerts():

    prices = get_prices()

    brent = prices["brent"]
    wti = prices["wti"]

    alerts = []

    # livello psicologico petrolio
    if brent > 90:
        alerts.append("⚠ Brent above $90 — possible supply tension")

    if brent < 80:
        alerts.append("⚠ Brent below $80 — demand weakness")

    # spread Brent / WTI
    spread = brent - wti

    if spread > 5:
        alerts.append("⚠ Brent-WTI spread widening — geopolitical risk possible")

    return alerts

@app.get("/news")
def news():

    try:

       url = "https://newsapi.org/v2/everything?q=oil OR opec OR iran OR tanker OR middle east&language=en&sortBy=publishedAt&pageSize=5&apiKey=05b963f904fe4927a2849248c0870371"

        r = requests.get(url)

        data = r.json()

        articles = []

        if "articles" in data:

            for a in data["articles"]:
                articles.append({
                    "title": a["title"],
                    "url": a["url"]
                })

        return articles

    except Exception as e:

        return [{"title": "News service unavailable", "url": "#"}]






