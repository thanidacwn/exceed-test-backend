from fastapi import FastAPI
from routers import locker


app = FastAPI()
app.include_router(locker.router)


@app.get("/")
def root():
    """ Root page of the API """
    return {"msg": "welcome to group8 root page สุดเท่"}
