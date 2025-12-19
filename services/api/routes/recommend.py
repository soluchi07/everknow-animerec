from fastapi import APIRouter, Query, HTTPException
import joblib
from pathlib import Path

router = APIRouter()

ARTIFACTS_PATH = Path("/app/ml/artifacts")
MODEL_FILENAME = "hybrid_recommender_engine.joblib"

engine = joblib.load(ARTIFACTS_PATH / MODEL_FILENAME)

@router.get("/recommendations/{user_id}")
def recommend(
    user_id: int,
    limit: int = Query(10, ge=1, le=50)
):
    try:
        results = engine.recommend(user_id, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return {
        "user_id": user_id,
        "num_results": len(results),
        "recommendations": results,
    }
