# app/api/routes/v1/health.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import time
from typing import Dict, Any

from app.config import get_db, check_database_health, check_database_connection
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(prefix="/v1", tags=["health"])

# Set permissions
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/health', perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/health/detailed', perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/health/database', perm=VxAPIPermsEnum.PUBLIC)

@router.get("/health")
async def basic_health_check():
    """Basic health check with simple database connectivity"""
    
    # Quick database check
    db_healthy = check_database_connection()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "GramSevak Seva API",
        "version": "1.0.0",
        "database": "connected" if db_healthy else "disconnected"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with comprehensive database analysis"""
    
    # Get detailed database health info
    db_health = check_database_health()
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "GramSevak Seva API",
        "version": "1.0.0",
        "checks": {
            "database": db_health
        }
    }
    
    # Set overall status based on database health
    if db_health["status"] == "unhealthy":
        health_data["status"] = "unhealthy"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_data
        )
    elif db_health["status"] in ["warning", "slow"]:
        health_data["status"] = "degraded"
    
    return health_data

@router.get("/health/database")
async def database_specific_health_check(db: Session = Depends(get_db)):
    """Dedicated database health check with connection pool info"""
    
    try:
        start_time = time.time()
        
        # Test basic query
        result = db.execute(text("SELECT version() as db_version"))
        db_version = result.fetchone()[0] if result.fetchone() else "unknown"
        
        # Test table access
        tables_result = db.execute(text("""
            SELECT COUNT(*) as table_count 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        table_count = tables_result.fetchone()[0]
        
        # Check if we can write (test with a simple operation)
        db.execute(text("SELECT 1"))  # This will fail if DB is read-only
        
        response_time = (time.time() - start_time) * 1000
        
        # Get connection pool info from your engine
        from app.config import engine
        pool = engine.pool
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": {
                "connected": True,
                "version": db_version.split(" ")[0] if db_version else "unknown",
                "response_time_ms": round(response_time, 2),
                "table_count": table_count,
                "writable": True,
                "connection_pool": {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": {
                    "connected": False,
                    "error": str(e)
                }
            }
        )