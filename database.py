import os
import django
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from django.conf import settings

# Build DATABASE_URL from Django's settings
db_settings = settings.DATABASES['default']
DATABASE_URL = (
    f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}@"
    f"{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
