from fastapi import UploadFile, Depends
from .BaseController import BaseController
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os

class DataController (BaseController):

    def __init__ (self):
        super().__init__() #this will call the __init__ method of the BaseController, which will initialize the app_settings attribute, so we can use it in the DataController without having to initialize it again
        self.size_scale = 1024 * 1024 # this is the scale for converting the file size from bytes to megabytes, because the FILE_MAX_SIZE is in megabytes, so we need to convert the file size to megabytes before comparing it with the FILE_MAX_SIZE


    def validate_uploaded_file(self, file : UploadFile): # this method will validate the file properties like size and type, it will return True if the file is valid and False if the file is invalid
            
            if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
                return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

            if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
                return False, ResponseSignal.FILE_SIZED_EXCEEDED.value

            return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    
    def generate_unique_filename(self, orig_file_name : str, project_id : str):
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id = project_id)

        clean_file_name = self.get_clean_file_name(
            orig_file_name = orig_file_name
            )
        
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + clean_file_name
            )
        
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + clean_file_name
            )
        
        return new_file_path

    
    def get_clean_file_name(self, orig_file_name : str):
        clean_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())
        
        clean_file_name = clean_file_name.replace(' ', '_')
        
        return clean_file_name
