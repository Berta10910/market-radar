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

    if brent > 95:
        alerts.append("🚨 Petrolio sopra $95 — forte tensione mercato")

    if brent > 90:
        alerts.append("⚠ Petrolio sopra $90 — possibile rischio geopolitico")

    if brent < 75:
        alerts.append("📉 Petrolio sotto $75 — possibile rallentamento economico")

    spread = brent - wti

    if spread > 6:
        alerts.append("⚠ Spread Brent-WTI elevato")

    return alerts


def oil_sentiment(title):

    bullish_words = [
        "war",
        "attack",
        "sanctions",
        "iran",
        "tanker",
        "pipeline",
        "conflict"
    ]

    bearish_words = [
        "recession",
        "demand drop",
        "oversupply",
        "production increase"
    ]

    title = title.lower()

    for word in bullish_words:
        if word in title:
            return "🟢 Rialzista petrolio"

    for word in bearish_words:
        if word in title:
            return "🔴 Ribassista petrolio"

    return "🟡 Neutrale"


def calculate_oil_index(articles):

    bullish = 0
    bearish = 0

    for a in articles:

        if a["sentiment"] == "🟢 Rialzista petrolio":
            bullish += 1

        if a["sentiment"] == "🔴 Ribassista petrolio":
            bearish += 1

    if bullish > bearish:
        return "🟢 MERCATO PETROLIO RIALZISTA"

    if bearish > bullish:
        return "🔴 MERCATO PETROLIO RIBASSISTA"

    return "🟡 MERCATO PETROLIO NEUTRALE"


@app.get("/news")
def news():

    try:

        url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey=05b963f904fe4927a2849248c0870371"

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
            "sentiment_index": "🟡 NEUTRALE",
            "news": []
        }

