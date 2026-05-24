from app.main import app
import uvicorn
from app.core.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    print("🚀 Starting Network Infrastructure Monitoring System...")
    print("📍 Access: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )