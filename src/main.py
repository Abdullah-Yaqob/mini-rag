from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env") #this will load the environment variables from the .env file

from routes import base



app = FastAPI()
app.include_router(base.base_router)

