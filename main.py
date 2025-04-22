from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
from routes.base import router 



app.include_router(router)


