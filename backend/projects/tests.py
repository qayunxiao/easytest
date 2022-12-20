from django.test import TestCase

# Create your tests here.
import  requests

for p in range(10):
    json_data ={
        "name": "订单系统"+ str(p),
        "describe": "订单系统"+str(p)+"描述",
        "images": "dsdsadad.jpg"
    }
    r=requests.post("http://127.0.0.1:8000/api/projects/create",
                  json=json_data)
    print(r.json())