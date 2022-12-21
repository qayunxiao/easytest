# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 14:42
# @Author  : alvin
# @File    : module_api.py
# @Software: PyCharm
from typing import List

import requests
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja.params import Query
from ninja.pagination import PaginationBase, paginate
from backend.common import response, Error, model_to_dict
from cases.models import TestCase
from module.models import Module
from projects.models import Project
from cases.api_schema import CaseIn, CaseDebugIn, CaseAssertIn,CaseOut
from backend.pagination import CustomPagination


router = Router(tags=["cases"])
'''

{
  "name": "alvin case",
  "module_id": 1,
  "url": "http://httpbin.org/get",
  "method": "get",
  "header": {},
  "params_type": "params",
  "params_body": {},
  "response": "string",
  "assert_type": "include",
  "assert_text": "hello",
  "extract_list": [
    "string"
  ]
}

'''
@router.post("/create", auth=None)
def create_case(request, data: CaseIn):
    """
    创建模块
    auth=None 该接口不需要认证
    """
    print("TestCase data",data)
    module = Module.objects.filter(id=data.module_id)
    if len(module) == 0:
        return response(error=Error.MODULE_NOT_EXIST)
    res=TestCase.objects.create(**data.dict())
    return response(item=model_to_dict(res))

@router.post("/debug", auth=None)
def debug_case(request, data: CaseDebugIn):
    global resp
    print("data",data)
    url = data.url
    method = data.method
    header=data.header
    params_type=data.params_type
    params_body=data.params_body
    print(url,method,header,params_type,params_body)
    if method not in ["get","post","put","delete"]:
        return response(error=Error.CASE_METHOD_ERROR)

    if params_type not in ["params","form","json"]:
        return response(error=Error.CASE_PARAMS_ERROR)

    if method == "get":
        resp=requests.get(url,headers=header).text
        print(resp)

    if method == "post":
        if params_type == "form":
            resp = requests.post(url,headers=header,data=params_body).text
        elif params_type == "json" :
            resp = requests.post(url,headers=header,data=params_body).text
        else:
            return  response(error=Error.CASE_PARAMS_ERROR)

    if method == "delete":
        if params_type == "form":
            resp = requests.delete(url,headers=header,data=params_body).text
        elif params_type == "json" :
            resp = requests.delete(url,headers=header,data=params_body).text
        else:
            return  response(error=Error.CASE_PARAMS_ERROR)

    return response(item={ "response": resp })


@router.post("/assert", auth=None)
def assert_case(request, data: CaseAssertIn):

# {
#     "response": "{\n  \"args\": {}, \n  \"headers\": {\n    \"Accept\": \"*/*\", \n    \"Accept-Encoding\": \"gzip, deflate\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"python-requests/2.26.0\", \n    \"X-Amzn-Trace-Id\": \"Root=1-63a29f3c-1953b265494646c2023c7fc4\"\n  }, \n  \"origin\": \"110.251.46.41\", \n  \"url\": \"http://httpbin.org/get\"\n}",
#     "assert_type": "include",
#     "assert_text": "org"
# }

     print("data",data)
     resp =data.response
     assert_type=data.assert_type
     assert_text=data.assert_text
     if assert_type not in ["include","equal"]:
         return response(error=Error.CASE_ASSERT_ERROR)
     if  assert_type == "include":
         if assert_text in resp:
             return  response()
         else:
             return response(success=False)
     elif assert_type == "equal":
         if assert_text == resp:
             return  response()
         else:
             return response(success=False)
     return  response()


@router.get("/{case_id}/", auth=None)
def get_case_detail(request, case_id: int):
    case=get_object_or_404(TestCase,id=case_id)
    if case.is_delete is True:
        return  response(error=Error.CASE_IS_DELETE)
    data = {
        "id":case.id,
        "name":case.name,
        "url":case.url,
        "method":case.method,
        "create_time":case.create_time
    }
    return response(item=data)

@router.delete("/{case_id}/", auth=None)
def delete_case(request, case_id: int):
    case=get_object_or_404(TestCase,id=case_id)
    case.is_delete=True
    case.save()
    return response()

@router.get("/list", auth=None, response=List[CaseOut])
@paginate(CustomPagination)
def case_list(request, **kwargs):
    res =TestCase.objects.filter(is_delete=False).all()
    print(res)
    return res