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

@app.get("/news")
def news():

    url = "https://newsapi.org/v2/everything?q=oil OR iran OR opec OR war&language=en&sortBy=publishedAt&pageSize=5&apiKey=YOUR_API_KEY"

    r = requests.get(url)

    data = r.json()

    articles = []

    for a in data["articles"]:
        articles.append({
            "title": a["title"],
            "url": a["url"]
        })

    return articles

