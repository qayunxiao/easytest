from typing import Any

from ninja import  Schema

class ProjectIn(Schema):
     name:str
     describe:str = None
     image:str = None

class ProjectOut(Schema):
     id:str
     name:str
     describe:str
     image:str
     create_time : Any