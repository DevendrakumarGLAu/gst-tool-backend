from fastapi import APIRouter
from controller.login_controller import LoginController
from schemas.schema import LoginRequest, LoginResponse

login_router = APIRouter()

@login_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    return LoginController.login_user(request.email, request.password)