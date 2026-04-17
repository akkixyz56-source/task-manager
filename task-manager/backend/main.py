from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine

from auth import router as auth_routes
from routes import project_routes
from routes import task_routes
from routes import analytics_routes


# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# ✅ CORS (VERY IMPORTANT — must be here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(analytics_routes.router)


# Test route
@app.get("/")
def home():
    return {"message": "API Running"}