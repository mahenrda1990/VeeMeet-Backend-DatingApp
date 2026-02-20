from fastapi import FastAPI
from app.api import auth, profile, filters, discover, likes, spotlight, users

app = FastAPI(title="Dating App API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(filters.router, prefix="/filters", tags=["Filters"])
app.include_router(discover.router, prefix="/discover", tags=["Discover"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])
app.include_router(spotlight.router, prefix="/spotlight", tags=["Spotlight"])
app.include_router(users.router, prefix="/users", tags=["Users"])
