from fastapi import FastAPI
from api.routes.recommend import router as recommend_router

app = FastAPI(
    title="Anime Recommendation API",
    version="0.1.0",
)

# Register routes
app.include_router(
    recommend_router,
    prefix="/api",
    tags=["recommendations"],
)

@app.get("/")
def root():
    return {"message": "Anime RecSys API running!"}
