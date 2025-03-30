from fastapi import FastAPI
from src.api import router as api_router
from src.flow_api import router as flow_router

app = FastAPI()

app.include_router(api_router, prefix="/crew")
app.include_router(flow_router, prefix="/flow")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
