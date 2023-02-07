from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
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
    duration: int
    start_time: int
    end_time: int


class Locker(BaseModel):
    locker_num: str
    is_available: bool
    user: Union[User, None]

def extra_fee(user:User):
    actual_duration = (user['end_time'] - user['start_time'])
    user_duration = user['duration']*3600
    if actual_duration > (user_duration):
        charge_fee = ceil((actual_duration - user_duration)/360)*20
        return charge_fee
    return 0

def total_cost(user:User):
    total = 0
    extra_duration = user['duration'] - 2
    if extra_duration > 0:
        total += extra_duration * 5
    add_fee = extra_fee(user)
    total += add_fee
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

@router.get("/return_items/{user_id}/{amount}")
def return_item(user_id, amount: int):
    """This function is use for return item process.

    It will check if user already done the payment or not before return it.
    """
    data = collection.find_one({"user.user_id": user_id}, {"_id": False})
    if data is None:
        raise HTTPException(
            status_code=400, detail="This user does not rent any locker."
        )
    msg = payment(amount, data['user'])
    return {"msg": msg}

@router.get("/total_fee/{locker_id}")
def show_fee(locker_id: str):
    data = collection.find({"locker_num": locker_id})
    cost = total_cost(data[0]['user'])
    return {"msg": f"your total cost is {cost} Bath"}

if __name__=='__main__':
    user = {
        'user_id': '1234',
        'item': ['apple'],
        'duration': 2,
        'start_time': 1675734534
    }