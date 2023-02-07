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
    actual_duration = (time.time() - user['start_time'])
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

@router.get("/unavailable")
def unavailable_locker() -> List:
    """For checking available lockers."""
    data = collection.find({"is_available": False}, {"_id": False})
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

@router.put("/update/{locker_num}")
def update_locker(locker_num: str, locker_status: bool = Body(), new_user : User |  None = Body()):
    """ Update locker status and user information"""
    user_update = jsonable_encoder(new_user)
    collection.update_one(
        {
            "locker_num": locker_num,
        },
        {"$set": {"is_available": locker_status, "user": user_update}}
    )
    return {"msg": "Locker updated successfully"}


@router.get("/rent/{locker_num}")
def rent_locker(locker_num: str, item: List[str] = Body(), user_id = Body(), duration: int = Body()):
    """ Rent a locker for a specific duration"""
    if locker_num not in ["01", '02', '03', '04', '05', '06']:
        raise HTTPException(status_code=400, detail="Locker not found")
    locker_available = collection.find({"locker_num": locker_num})

    if locker_available[0]["is_available"]  == False:
        raise HTTPException(status_code=400, detail="Locker is not available")
    user = {
		"user_id": user_id,
        "item": item,
        "duration": int(duration),
        "start_time": int(time.time()),
        "end_time": int(time.time()) + (duration * 3600)
        }
    update_locker(locker_num, False, user)
    return {"msg": "Locker rented successfully"}


@router.get("/clear/{locker_num}")
def clear_locker(locker_num: str):
    """ Clear a locker"""
    if locker_num not in ["01", '02', '03', '04', '05', '06']:
        raise HTTPException(status_code=400, detail="Locker not found")
    locker_available = collection.find({"locker_num": locker_num})
    if locker_available[0]["is_available"]  == True:
        raise HTTPException(status_code=400, detail="Locker is already available")
    update_locker(locker_num, True, None)
    return {"msg": "Locker cleared successfully"}
