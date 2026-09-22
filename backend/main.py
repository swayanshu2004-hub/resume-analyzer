from fastapi import FastAPI
from backend.api import router

app = FastAPI(title="Resume Analyzer API")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Resume Analyzer Backend is Running"}