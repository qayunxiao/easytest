# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 14:42
# @Author  : alvin
# @File    : module_api.py
# @Software: PyCharm

from ninja import Router
from django.shortcuts import get_object_or_404
from ninja.params import Query

from backend.common import response, Error, model_to_dict
from cases.models import Module
from projects.models import Project
from module.api_schema import ModuleIn, ProjectIn

router = Router(tags=["cases"])

