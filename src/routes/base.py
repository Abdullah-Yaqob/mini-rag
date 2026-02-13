from fastapi import FastAPI,APIRouter
import os # for handling environment variables

base_router = APIRouter(
    prefix = "/api/v1", #this is the prefix for all routes in this router, so all routes will start with /api/v1
    tags = ["api_v1"] #this is the tag for all routes in this router, so all routes will be grouped under this tag in the documentation
)

@base_router.get("/")
async def welcome(): #this is the first route, it will return a welcome message and the app version
                     #async is used to make the route non-blocking, so it can handle multiple requests at the same time
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    
    return {
        "message": f"Welcome to the {app_name} app!",
        "version": app_version
    }