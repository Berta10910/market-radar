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
        "iran",
        "hormuz",
        "tanker",
        "pipeline",
        "sanctions",
        "opec cuts",
        "supply disruption"
    ]

    bearish_words = [
        "recession",
        "demand drop",
        "oversupply",
        "production increase",
        "inventory build"
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


import feedparser


import feedparser

@app.get("/news")
def news():

    feeds = [
        "https://www.oilprice.com/rss/main",
        "https://www.reuters.com/markets/commodities/rss"
    ]

    articles = []

    try:

        for feed_url in feeds:

            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:5]:

                sentiment = oil_sentiment(entry.title)

                articles.append({
                    "title": entry.title,
                    "url": entry.link,
                    "sentiment": sentiment
                })

        articles = articles[:5]

        index = calculate_oil_index(articles)

        return {
            "sentiment_index": index,
            "news": articles
        }

    except Exception:

        return {
            "sentiment_index": "🟡 MERCATO NEUTRALE",
            "news": []
        }



