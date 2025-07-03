# main.py
# This file serves as the entry point for the FastAPI application.
from fastapi import FastAPI
from app.core.app_factory import create_app  # Fixed import path
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.vx_api_perms_utils import VxAPIPermsUtils
from fastapi.responses import JSONResponse

app = create_app()

# Explicitly set root route as public
VxAPIPermsUtils.set_perm_get(path='/', perm=VxAPIPermsEnum.PUBLIC)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Gram Sevak Seva portal"}

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
    uvicorn.run(app, host="localhost", port=8000)