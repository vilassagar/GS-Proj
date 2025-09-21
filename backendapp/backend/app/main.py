# main.py
# This file serves as the entry point for the FastAPI application.
from fastapi import FastAPI
from app.core.app_factory import create_app  # Fixed import path
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.vx_api_perms_utils import VxAPIPermsUtils
from fastapi.responses import JSONResponse
from app.api.routes.v1 import health
import logging
import os
app = create_app()

# Explicitly set root route as public
VxAPIPermsUtils.set_perm_get(path='/', perm=VxAPIPermsEnum.PUBLIC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Gram Sevak Seva portal"}

# Add startup event to your app
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting GramSevak Seva API")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'unknown')}")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'unknown')}")
    logger.info(f"Database URL configured: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
    logger.info("✅ Application startup complete")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info("🛑 Shutting down GramSevak Seva API")
    
# Handle common browser requests that cause 404s
@app.get("/.well-known/gpc.json")
async def gpc_json():
    return JSONResponse(
        status_code=200,
        content={"gpc": False}
    )

@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(
        status_code=204,  # No Content
        content={}
    )

@app.get("/robots.txt")
async def robots():
    return JSONResponse(
        status_code=200,
        content="User-agent: *\nDisallow: /",
        media_type="text/plain"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)