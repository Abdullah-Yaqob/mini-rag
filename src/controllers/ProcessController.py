from .BaseController import BaseController
from .ProjectController import ProjectController   
import os

class ProcessController(BaseController):

    def __init__(self):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id = self.project_id)

def get_file_extension(self, file_id : str):
    return os.path.splitext(file_id)[1]