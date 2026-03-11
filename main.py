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

    if brent > 90:
        alerts.append("⚠ Brent above $90 — possible supply tension")

    if brent < 80:
        alerts.append("⚠ Brent below $80 — demand weakness")

    spread = brent - wti

    if spread > 5:
        alerts.append("⚠ Brent-WTI spread widening — geopolitical risk possible")

    return alerts


def oil_sentiment(title):

    bullish_words = [
        "war",
        "attack",
        "sanctions",
        "iran",
        "houthi",
        "tanker",
        "pipeline",
        "conflict",
        "opec cuts",
        "supply disruption"
    ]

    bearish_words = [
        "recession",
        "demand drop",
        "oversupply",
        "production increase",
        "inventory build",
        "economic slowdown"
    ]

    title = title.lower()

    for word in bullish_words:
        if word in title:
            return "🟢 Bullish Oil"

    for word in bearish_words:
        if word in title:
            return "🔴 Bearish Oil"

    return "🟡 Neutral"


def calculate_oil_index(articles):

    bullish = 0
    bearish = 0

    for a in articles:

        if a["sentiment"] == "🟢 Bullish Oil":
            bullish += 1

        if a["sentiment"] == "🔴 Bearish Oil":
            bearish += 1

    if bullish > bearish:
        return "🟢 BULLISH OIL SENTIMENT"

    if bearish > bullish:
        return "🔴 BEARISH OIL SENTIMENT"

    return "🟡 NEUTRAL OIL SENTIMENT"


@app.get("/news")
def news():

    try:

        url = "https://newsapi.org/v2/everything?q=oil OR opec OR iran OR tanker OR middle east&language=en&sortBy=publishedAt&pageSize=5&apiKey=05b963f904fe4927a2849248c0870371"

        r = requests.get(url)
        data = r.json()

        articles = []

        if "articles" in data:

            for a in data["articles"]:

                sentiment = oil_sentiment(a["title"])

                articles.append({
                    "title": a["title"],
                    "url": a["url"],
                    "sentiment": sentiment
                })

        index = calculate_oil_index(articles)

        return {
            "sentiment_index": index,
            "news": articles
        }

    except Exception:

        return {
            "sentiment_index": "🟡 NEUTRAL",
            "news": []
        }

