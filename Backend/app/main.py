from app.core.app_configs import create_app

app = create_app()

app.get("/")


async def read_root():
    return {"message": "Welcome to Gram Sevak Seva portal"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
