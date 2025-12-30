from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(title="AI Support Ticket System")


@app.get("/health")
def health_check():
    return {"status": "ok"}
