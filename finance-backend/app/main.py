from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from .database import init_db
from .routes import user_routes, record_routes, dashboard_routes
from .core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Finance Dashboard Backend API"
)

# Initialize database
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


# Include routes
app.include_router(user_routes.router)
app.include_router(record_routes.router)
app.include_router(dashboard_routes.router)


@app.get("/", tags=["health"])
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Finance Dashboard Backend API",
        "version": settings.app_version
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/dashboard", response_class=HTMLResponse, tags=["ui"])
def get_dashboard():
    """Serve the dashboard UI"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dashboard.html")
    try:
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Dashboard not found</h1>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
