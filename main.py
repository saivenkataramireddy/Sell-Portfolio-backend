from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from database import engine, Base
from routers import users, skills, journey, certifications, projects, contact
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Portfolio API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register Routers
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(journey.router)
app.include_router(certifications.router)
app.include_router(projects.router)
app.include_router(contact.router)

@app.get("/")
def home():
    return {"message":"Portfolio Backend Running Successfully"}