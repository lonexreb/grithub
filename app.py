from fastapi import FastAPI
from controllers import training_controller, auth_controller, gamification_controller
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Grithub API", version="1.0")

# Include API routes first
app.include_router(auth_controller.router)
app.include_router(training_controller.router)
app.include_router(gamification_controller.router)

# Mount static files at the root. This will serve index.html by default.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)