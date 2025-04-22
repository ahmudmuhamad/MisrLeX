from fastapi import FastAPI, APIRouter
import os
from dotenv import load_dotenv
load_dotenv()


router = APIRouter(
    prefix="/api/v0",
    tags=["api_v0"],
)


@router.get("/")
async def root():
    return {
        "APP_NAME": os.getenv("APP_NAME"),
        "APP_VERSION": os.getenv("APP_VERSION")
        }
