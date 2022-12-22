from django.test import TestCase

# Create your tests here.

# Create your tests here.
import  requests

for p in range(2):
    json_data ={
        "name": "三级1模块系统权限"+str(p),
        "project_id": 2,
        "parent_id": 13
    }
    r=requests.post("http://127.0.0.1:8000/api/module/create",
                    json=json_data)
    print(r.json())