from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.auth.router import router as auth_router
from app.tickets.router import router as ticket_router
from app.users.router import router as users_router

app = FastAPI(title="AI Support Ticket System")

# Configure CORS
cors_origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ticket_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
