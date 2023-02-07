from fastapi import APIRouter, Body
from typing import Union, Optional, List
from pydantic import BaseModel
from datetime import timedelta, datetime
from database.mongo_connection import *

router = APIRouter(
    prefix="/locker",
    tags=["locker"],
    responses={404: {"description": "Not found"}},
)

class User(BaseModel):
    user_id: str
    item: List[str]
    duration: timedelta
    start_time: datetime
    end_time: datetime

class Locker(BaseModel):
    locker_num: str
    is_available: bool
    user: Union[User, None]


@router.get("/available_lockers")
def find_available_locker()->List:
    """ For checking available lockers."""
    data = collection.find({"is_available": True})
    for i in data:
        print(i)


