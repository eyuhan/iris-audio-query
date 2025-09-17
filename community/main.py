from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_database, RESET_DATABASE, engine
from app.routers import audio
from app.config import AppConfig

app = FastAPI(
    title="IRIS Audio Query API",
    description="A FastAPI application with IRIS database integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    init_database(reset_data=RESET_DATABASE)

# Include routers
app.include_router(audio.router)

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "IRIS Audio Query API is running"}

@app.get("/health")
def health_check():
    """Health check endpoint with more details."""
    return {
        "status": "healthy",
        "service": "iris-audio-query-community",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=AppConfig.HOST, port=AppConfig.PORT)