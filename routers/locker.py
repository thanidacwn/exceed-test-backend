from fastapi import APIRouter, Body, HTTPException
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
def find_available_locker() -> List:
    """For checking available lockers."""
    data = collection.find({"is_available": True}, {"_id": False})
    available_lockers = []
    for i in data:
        available_lockers += [i]
    return available_lockers


@router.get("/return_items/{user_id}")
def return_item(user_id) -> any:
    """This function is use for return item process.

    It will check if user already done the payment or not before return it.
    """
    data = collection.find_one({"user.uer_id": user_id}, {"_id": False})
    print(data)
    if data is None:
        raise HTTPException(
            status_code=400, detail="This user does not rent any locker."
        )
    return {"msg": "return success"}
