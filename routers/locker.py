from fastapi import APIRouter, Body
from typing import Union, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/locker",
    tags=["locker"],
    responses={404: {"description": "Not found"}},
)