from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.pets.routers import router as pets_router
from app.users.routers import router as users_router

app = FastAPI(title="Pet Finder API")

app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(users_router)
app.include_router(pets_router)