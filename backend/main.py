from fastapi import FastAPI
from app.auth.router import router as auth_router

app = FastAPI(title="Pasik API")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "Pasik API is running"}