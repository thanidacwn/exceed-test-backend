from fastapi import APIRouter, Body, HTTPException
from typing import Union, Optional, List
from pydantic import BaseModel
import time
from math import ceil
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

def extra_fee(user:User):
    actual_duration = ((user.end_time.total_seconds()*0.0166667) - (user.start_time.total_seconds()*0.0166667))
    if actual_duration > (user.duration*60):
        charge_fee = int(ceil(actual_duration - (user.duration*60))*20)
        return charge_fee
    return 0

def total_cost(user:User):
    total = 0
    extra_duration = user.duration - 2
    if extra_duration > 0:
        total += int((ceil(extra_duration) * 5))
    add_fee = extra_fee(user)
    total += int(add_fee)
    return total

def payment(amount:int, user:User):
    total = total_cost(user)
    if amount > total:
        return f"your change is {amount - total} Baht"
    if amount < total:
        return f"you need to insert {total - amount} more Baht"
    return "Payment successful"

@router.get("/available_lockers")
def find_available_locker() -> List:
    """For checking available lockers."""
    data = collection.find({"is_available": True}, {"_id": False})
    available_lockers = []
    for i in data:
        available_lockers += [i]
    return available_lockers

@router.get("/return_items/{user_id}")
def return_item(user_id):
    """This function is use for return item process.

    It will check if user already done the payment or not before return it.
    """
    data = collection.find_one({"user.user_id": user_id}, {"_id": False})
    print(data)
    if data is None:
        raise HTTPException(
            status_code=400, detail="This user does not rent any locker."
        )
    return {"msg": "return success"}

