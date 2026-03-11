from fastapi import FastAPI
from prices import get_prices

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Market Radar API running"}

@app.get("/prices")
def prices():
    return get_prices()