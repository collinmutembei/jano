from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, journal

app = FastAPI(
    title="Jano API", description="Personal journaling API service", version="1.0.0"
)

origins = ["http://localhost:8081"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(journal.router, prefix="/journal")
