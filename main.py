from fastapi import FastAPI
from routers import locker


app = FastAPI()
app.include_router(locker.router)

@app.get("/")
def root():
    return {"msg": "welcome to group8 root page สุดเท่"}

