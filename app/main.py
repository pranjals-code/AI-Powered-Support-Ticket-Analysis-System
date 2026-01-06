from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.tickets.router import router as ticket_router

app = FastAPI(title="AI Support Ticket System")

app.include_router(auth_router)
app.include_router(ticket_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
