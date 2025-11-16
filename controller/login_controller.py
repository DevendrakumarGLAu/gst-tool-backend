from django.contrib.auth.hashers import check_password
from fastapi import HTTPException
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import jwt
import os

from registration.models import UserAccount

SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class LoginController:
    @staticmethod
    def login_user(email: str, password: str):
        try:
            user = UserAccount.objects.get(email=email, is_active=True)
        except UserAccount.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        
        # print("DB Password Hash:", user.password)
        
        # hashed_password = make_password(password)
        # print("Entered Password:", hashed_password)

        if not check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # jwt
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + access_token_expires

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.name,
            "exp": expire
        }

        # In a real app, generate and return a JWT here
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.name
                }
