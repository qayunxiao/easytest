# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 9:12
# @Author  : alvin
# @File    : api.py
# @Software: PyCharm
from datetime import datetime
from ninja import  NinjaAPI
from ninja.security import HttpBearer
from users.api import router as users_router
from projects.api import router as projects_router

from django.contrib.sessions.models import Session
from backend.settings import SESSION_COOKIE_AGE

class InvalidToken(Exception):
    """无效的token"""
    pass


class OverdueToken(Exception):
    """过期的token"""
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        自动定义认证token处理
        """
        try:
            session = Session.objects.get(pk=token)
            # # 有效时间
            # SESSION_COOKIE_AGE
            # # 当前时间
            # datetime
            # # token/session
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """无效token返回类型 """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(OverdueToken)
def on_overdue_token(request, exc):
    """过期token返回类型 """
    return api.create_response(request, {"detail": "Overdue token supplied"}, status=401)



api.add_router("/users/",users_router)
api.add_router("/projects/",projects_router)

