from fastapi import APIRouter
from schemas.role_schema import RoleCreateRequest, RoleUpdateRequest, RoleResponse
from controller.role_controller import RoleController
from typing import List

role_router = APIRouter()

@role_router.post("/", response_model=RoleResponse)
def create_role(request: RoleCreateRequest):
    role = RoleController.create_role(
        name=request.name,
        description=request.description,
        created_by=request.created_by
    )
    return role

@role_router.get("/", response_model=List[RoleResponse])
def list_roles():
    return RoleController.get_roles()

@role_router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int):
    return RoleController.get_role(role_id)

@role_router.post("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, request: RoleUpdateRequest):
    return RoleController.update_role(
        role_id=role_id,
        name=request.name,
        description=request.description,
        updated_by=request.updated_by
    )

@role_router.delete("/{role_id}", response_model=RoleResponse)
def delete_role(role_id: int, deleted_by: str = None):
    return RoleController.delete_role(role_id, deleted_by=deleted_by)
