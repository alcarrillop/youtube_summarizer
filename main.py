from fastapi import FastAPI
from routes import videos, transcriptions, summaries
import uvicorn


app = FastAPI()

# Including the routers for different functionalities
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(transcriptions.router, prefix="/transcriptions", tags=["transcriptions"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])

# Additional configurations or routes can be added here

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
