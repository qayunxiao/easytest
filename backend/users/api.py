from ninja import  Router
from ninja import  Schema
from django.contrib.auth.models import  User
from django.contrib import auth

from backend.common import response,Error

router = Router(tags=["users"])

class RegisterIN(Schema):
    username:str
    password:str
    confirm_pwd:str

@router.post("/register")
def user_register(request,payload:RegisterIN):
    if payload.password != payload.confirm_pwd:
        return response(Error.PAWD_ERROR)
    user = User.objects.filter(username=payload.username)
    print(user,type(user))
    if user:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=payload.username,password=payload.password)
    user_info={
        "id":user.id,
        "username":user.username,
    }
    return response(result=user_info)


class LoginIN(Schema):
    username:str
    password:str

@router.post("/login")
def user_login(request,payload:LoginIN):
    user_name=payload.username
    user_pwd=payload.password
    print(user_name,user_pwd)
    user =auth.authenticate(username=user_name,password=user_pwd)
    if (user is not None) and (user.is_active is True):
        user_info={
            "id":user.id,
            "username":user.username,
        }
        return response(result=user_info)
    else:
        return response(error=Error.USER_OR_PAWD_ERROR)