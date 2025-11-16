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

HARDCODED_USER = {
    "email": "Dev@gmail.com",
    "password": make_password("Dev@1997"),  # hashed password
    "id": 1,
    "role": {"name": "admin"}
}

class LoginController:
    @staticmethod
    def login_user(email: str, password: str):
        try:
            import pdb
            pdb.set_trace()
            # Check if email matches
            if email != HARDCODED_USER["email"]:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Check password
            if not check_password(password, HARDCODED_USER["password"]):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # JWT generation
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            expire = datetime.utcnow() + access_token_expires

            payload = {
                "sub": str(HARDCODED_USER["id"]),
                "email": HARDCODED_USER["email"],
                "role": HARDCODED_USER["role"]["name"],
                "exp": expire
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            return {
                "message": "Login successful",
                "user_id": HARDCODED_USER["id"],
                "email": HARDCODED_USER["email"],
                "access_token": token,
                "token_type": "bearer",
                "role": HARDCODED_USER["role"]["name"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"login failed: {str(e)}")
        
        
    @staticmethod
    def login_user1(email: str, password: str):
        try:
            user = UserAccount.objects.get(email=email, is_active=True)
        except UserAccount.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        
        try:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"login failed: {str(e)}")
