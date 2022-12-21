from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
import  requests

for p in range(5):
    json_data ={
        "name": "三级模块"+str(p),
        "project_id": 1,
        "parent_id": 8
    }
    r=requests.post("http://127.0.0.1:8000/api/cases/",
                    json=json_data)
    print(r.json())