from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routers import (auth_router, users_router,
                          tasks_router, transactions_router)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HomeBase API",
    description="Task and finance management for home",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(transactions_router)

@app.get("/")
def root():
    return {"message": "HomeBase API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}