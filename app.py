# app.py
from fastapi import FastAPI
from controllers import training_controller, auth_controller

app = FastAPI(title="Grithub API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Grithub API!"}

app.include_router(training_controller.router)
app.include_router(auth_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
