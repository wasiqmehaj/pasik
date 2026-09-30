from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router

app = FastAPI(title="Pasik API")

app.include_router(auth_router)
app.include_router(profile_router)

@app.get("/")
def root():
    return {"status": "Pasik API is running"}