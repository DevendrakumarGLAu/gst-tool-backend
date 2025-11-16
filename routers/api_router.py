from fastapi import APIRouter
from api_v1.login_router import login_router  # import the APIRouter instance, not module

api_router = APIRouter()

# Include all routers here
api_router.include_router(login_router, prefix="/auth", tags=["Login"])

# role router
from api_v1.role import role_router
api_router.include_router(role_router, prefix="/role", tags=['Roles'])

# gst calculation
from api_v1.gst_tool import gst_router
api_router.include_router(gst_router, prefix="/gst", tags=["GSTCalculation"])