from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from routers import locker
import os

load_dotenv(".env")
username = os.getenv("username")
password = os.getenv("password")

client = MongoClient(
    f"mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
)

db = client["exceed08"]
collection = db["locker_management_collection"]

app = FastAPI()
app.include_router(locker.router)

@app.get("/")
def root():
    return {"msg": "welcome to group8 root page สุดเท่"}
