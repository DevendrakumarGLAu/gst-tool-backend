import os
import django



# Set your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # change to your project settings path
django.setup()

from fastapi import FastAPI
from routers.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="GST Management API", version="1.0")
# origins = [
#     "http://localhost:4200",  # Angular dev server
#     "http://127.0.0.1:4200",
#     '*'
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can also use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE etc
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to gst Management API"}


# start command
# uvicorn main:app --reload
