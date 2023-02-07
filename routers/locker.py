from fastapi import APIRouter, Body
from typing import Union, Optional
from pydantic import BaseModel
from datetime import timedelta
import time
from math import ceil

router = APIRouter(
    prefix="/locker",
    tags=["locker"],
    responses={404: {"description": "Not found"}},
)

class User(BaseModel):
    user_id : str
    items : list[str]
    duration : time
    start_time : timedelta
    end_time : timedelta


class Locker(BaseModel):
    locker_num : int
    is_available : bool
    user : Union[User, None]

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







