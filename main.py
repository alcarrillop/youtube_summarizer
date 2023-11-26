from fastapi import FastAPI
from routes.routes import router as youtube_router

app = FastAPI()

# Include the YouTube processing router
app.include_router(youtube_router, prefix="/youtube", tags=["youtube"])

# Additional configurations or routes can be added here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
