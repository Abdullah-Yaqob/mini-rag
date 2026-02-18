from fastapi import FastAPI,APIRouter,Depends, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import os                                    # for handling environment variables
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models.enums.ResponseEnums import ResponseSignal
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error') # this is the logger for the data route

data_router = APIRouter(
    prefix = "/api/v1/data",            #must start with /  #this is the prefix for all routes in this router, so all routes will start with /api/v1/data
    tags = ["api_v1" , "data"]            #this is the tag for all routes in this router, so all routes will be grouped under this tag in the documentation
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str, file : UploadFile,
                      app_settings : Settings = Depends (get_settings)):
    #this is the route for uploading data, it will take a file and a project id as input and return a success message
    data_controller = DataController()
    # validate the file properties like size and type
    is_valid, result_signal = data_controller.validate_uploaded_file(file = file)
    
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = {
                "signal" : result_signal
                }
            )

    project_dir_path = ProjectController().get_project_path(project_id = project_id)
    file_path = data_controller.generate_unique_filename(
        orig_file_name = file.filename,
        project_id = project_id
        )
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        logger.error(f"Error uploading file: {e}")
        
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
            }
        )
    
    return JSONResponse(
        content = {
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "project_dir_path": project_dir_path
        },
       
    )