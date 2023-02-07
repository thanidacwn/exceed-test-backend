from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Union, Optional, List
from pydantic import BaseModel, BaseConfig
from database.mongo_connection import *
import time, datetime


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


@router.put("/update/{locker_num}")
def update_locker(locker_num: str, locker_status: bool = Body(), new_user : User |  None = Body()):
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
    if locker_num not in ["01", '02', '03', '04', '05', '06']:
        raise HTTPException(status_code=400, detail="Locker not found")
    locker_available = collection.find({"locker_num": locker_num})

    if locker_available["is_available" == False]:
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
    if locker_num not in ["01", '02', '03', '04', '05', '06']:
        raise HTTPException(status_code=400, detail="Locker not found")
    locker_available = collection.find({"locker_num": locker_num})
    if locker_available["is_available" == True]:
        raise HTTPException(status_code=400, detail="Locker is already available")
    update_locker(locker_num, True, None)
    return {"msg": "Locker cleared successfully"}

