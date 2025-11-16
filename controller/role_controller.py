from fastapi import HTTPException
from django.utils import timezone

from role.models import Role

class RoleController:

    def create_role(name: str, description: str = None, created_by: str = None):
        if Role.objects.filter(name=name).exists():
            raise HTTPException(status_code=400, detail="Role already exists")
        role = Role.objects.create(
            name=name,
            description=description,
            created_by=created_by
        )
        return role

    @staticmethod
    def get_roles():
        return Role.objects.filter(is_active=True)

    @staticmethod
    def get_role(role_id: int):
        try:
            return Role.objects.get(id=role_id, is_active=True)
        except Role.DoesNotExist:
            raise HTTPException(status_code=404, detail="Role not found")

    @staticmethod
    def update_role(role_id: int, name: str = None, description: str = None, updated_by: str = None):
        role = RoleController.get_role(role_id)
        if name:
            role.name = name
        if description:
            role.description = description
        role.updated_by = updated_by
        role.save()
        return role

    @staticmethod
    def delete_role(role_id: int, deleted_by: str = None):
        role = RoleController.get_role(role_id)
        role.is_active = False
        role.deleted_at = timezone.now()
        role.deleted_by = deleted_by
        role.save()
        return role
