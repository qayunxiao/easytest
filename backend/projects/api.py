import os
import hashlib
from ninja import File
from ninja.files import UploadedFile
from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from ninja.pagination import paginate
from backend.common import response, Error, model_to_dict
from backend.pagination import CustomPagination
from backend.settings import IMAGE_DIR
from projects.models import Project
from projects.api_schema import ProjectIn, ProjectOut
from cases.models import Module, TestCase

router = Router(tags=["projects"])


@router.post("/", auth=None)
def create_project(request, data: ProjectIn):
    """
    创建项目
    auth=None 该接口不需要认证
    """
    project = Project.objects.filter(name=data.name)
    if len(project) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)

    if data.image == "":
        data.image = "default_project_image.png"
    Project.objects.create(**data.dict())
    return response()


@router.get("/list", auth=None, response=List[ProjectOut])
@paginate(CustomPagination)
def project_list(request, **kwargs):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    data = Project.objects.filter(is_delete=False).all()
    print(type(data))
    for p in data:
        print(p.id,p.name,p.describe,p.image)
    return Project.objects.filter(is_delete=False).all()


@router.get("/{project_id}/", auth=None)
def project_details(request, project_id: int):
    """
    获取项目详情
    auth=None 该接口不需要认证
    """
    project = get_object_or_404(Project, id=project_id)
    if project.is_delete is True:
        return response(error=Error.PROJECT_IS_DELETE)

    data = {
        "id": project.id,
        "name": project.name,
        "describe": project.describe,
        "image": project.image,
        "create_time": project.create_time
    }
    return response(item=data)


@router.put("/{project_id}/", auth=None)
def project_update(request, project_id: int,  payload: ProjectIn):
    """
    项目更新
    auth=None 该接口不需要认证
    """
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()

    return response()


@router.delete("/{project_id}/", auth=None)
def project_delete(request, project_id: int):
    """
    项目删除
    auth=None 该接口不需要认证
    """
    project = get_object_or_404(Project, id=project_id)
    project.is_delete = True
    project.save()

    return response()


@router.post("/upload", auth=None)
def project_image_upload(request, file: UploadedFile = File(...)):
    """
    项目图片上传
    """
    # 判断文件后缀名
    suffix = file.name.split(".")[-1]
    if suffix not in ["png", "jpg", "jpeg", "gif"]:
        return response(error=Error.FILE_TYPE_ERROR)

    # 判断文件大小 1024 * 1024 * 2 = 2MB
    if file.size > 2097152:
        return response(error=Error.FILE_SIZE_ERROR)

    # 文件名生成md5
    file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
    file_name = file_md5 + "." + suffix

    # 保存到本地
    upload_file = os.path.join(IMAGE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return response(item={"name": file_name})


@router.get("/{project_id}/cases", auth=None)
def project_case_list(request, project_id: int):
    """
    通过项目ID 获取用例列表
    auth=None 该接口不需要认证
    """
    project = get_object_or_404(Project, id=project_id)
    if project.is_delete is True:
        return response(error=Error.PROJECT_IS_DELETE)

    modules = Module.objects.filter(project_id=project.id)
    cases_list = []
    for m in modules:
        cases = TestCase.objects.filter(module_id=m.id)
        for c in cases:
            cases_list.append(model_to_dict(c))

    return response(item=cases_list)
