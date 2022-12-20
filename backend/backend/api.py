# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 9:12
# @Author  : alvin
# @File    : api.py
# @Software: PyCharm

from ninja import  NinjaAPI
from users.api import router as users_router

api = NinjaAPI()

api.add_router("/users/",users_router)

