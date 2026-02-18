from fastapi import FastAPI,APIRouter,Depends
import os                                    # for handling environment variables
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix = "/api/v1",                      #this is the prefix for all routes in this router, so all routes will start with /api/v1
    tags = ["api_v1"]                        #this is the tag for all routes in this router, so all routes will be grouped under this tag in the documentation
)

@base_router.get("/")
async def welcome(app_settings : Settings = Depends(get_settings)):                                  #this is the first route, it will return a welcome message and the app version async is used to make the route non-blocking, so it can handle multiple requests at the same time

   # app_settings = get_settings()  using Depends is a better way to get the settings, because it will automatically handle the caching of the settings, so we don't have to worry about it
   # #aslo it make the architecture of the app cleaner and more modular, because we can easily swap out the settings implementation if we want to in the future without having to change the code in the route

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    
    return {
        "message": f"Welcome to the {app_name} app!",
        "version": app_version
    }