# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 9:12
# @Author  : alvin
# @File    : module_api.py
# @Software: PyCharm
from ninja import  NinjaAPI
from ninja.security import HttpBearer
from users.api import router as users_router
from projects.api import router as projects_router
from module.api import router as module_router
from cases.api  import router as cases_router
from django.contrib.sessions.models import Session


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
api.add_router("/module/",module_router)
api.add_router("/cases/",cases_router)


