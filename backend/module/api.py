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

router = Router(tags=["module"])


@router.post("/create", auth=None)
def create_module(request, data: ModuleIn):
    """
    创建模块
    auth=None 该接口不需要认证
    """
    print("module data",data)
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    module = Module.objects.filter(name=data.name,project_id=data.project_id)
    if len(module) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)
    res=Module.objects.create(**data.dict())
    return response(item=model_to_dict(res))

def node_tree(nodes, current_node):
    """
    递归：获取节点的子节点
    """
    for node in nodes:
        if node["parent_id"] == current_node["id"]:
            current_node["children"].append(node)
            node_tree(nodes, node)

    return current_node


def child_node(nodes, current_node):
    """
    判断有没有子节点
    """
    print("child_node ->nodes",nodes)
    for node in nodes:
        print("child_node ->node",node)
        if node["parent_id"] == current_node["id"]:
            return True
    return False


@router.get("/tree", auth=None)
def get_module_tree(request, filters: ProjectIn = Query(...)):
    """
    获取模块树ModuleIn
    """
    modules = Module.objects.filter(project_id=filters.project_id, is_delete=False)
    print(get_module_tree,modules)
    data_node = []
    for n in modules:
        data_node.append({
            "id": n.id,
            "parent_id": n.parent_id,
            "label": n.name,
            "children": [],
        })
    print("data_node->",data_node)
    data = []

    for n in data_node:
        is_child = child_node(data_node, n)  # --> True/False

        if (n["parent_id"] == 0) and (is_child is False):
            data.append(n)
        elif (n["parent_id"] == 0) and (is_child is True):
            ret = node_tree(data_node, n)
            data.append(ret)
    print("data->",data)
    return response(item=data)

@router.delete("/{module_id}/", auth=None)
def project_delete(request, module_id: int):
    """
    模块删除
    auth=None 该接口不需要认证
    """
    module= get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()

    return response()
