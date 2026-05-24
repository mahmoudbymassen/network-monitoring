from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.database import engine, Base
from datetime import datetime

# Routers
from .routers.appareil import router as appareil_router
from .routers.scan import router as scan_router
from .routers.alerte import router as alerte_router
from .routers.dashboard import router as dashboard_router
from .routers.topology import router as topology_router
from .routers.export import router as export_router
from .routers.report import router as report_router

settings = get_settings()

app = FastAPI(
    title="Network Infrastructure Monitoring System",
    description="Outil professionnel de découverte, monitoring et visualisation du réseau",
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(appareil_router, prefix="/api/appareils", tags=["Appareils"])
app.include_router(scan_router, prefix="/api/scan", tags=["Scan"])
app.include_router(alerte_router, prefix="/api/alertes", tags=["Alertes"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(topology_router, prefix="/api/topology", tags=["Topology"])
app.include_router(export_router, prefix="/api/export", tags=["Export"])
app.include_router(report_router, prefix="/api/report", tags=["Report"])

# Startup Event
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables verified successfully!")
    print("🚀 Network Monitoring System started successfully!")
    print("📍 Access: http://127.0.0.1:8000/docs")

@app.get("/")
async def root():
    return {
        "message": "Network Infrastructure Monitoring System",
        "status": "running",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }