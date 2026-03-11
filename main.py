from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prices import get_prices

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
