from typing import Any

from ninja import  Schema

class ModuleIn(Schema):
     name:str
     project_id:int
     parent_id:int = 0

class ProjectIn(Schema):
     project_id: int


class ModuleOut(Schema):
     name:str
     project_id:int
     parent_id:int = 0
     create_time : Any