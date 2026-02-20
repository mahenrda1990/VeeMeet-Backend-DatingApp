from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import auth, profile, filters, discover, likes, spotlight, users
import os

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Dating App API")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(filters.router, prefix="/filters", tags=["Filters"])
app.include_router(discover.router, prefix="/discover", tags=["Discover"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])
app.include_router(spotlight.router, prefix="/spotlight", tags=["Spotlight"])
app.include_router(users.router, prefix="/users", tags=["Users"])
