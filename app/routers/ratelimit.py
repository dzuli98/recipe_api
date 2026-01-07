from fastapi import APIRouter, Depends
from ..dependencies.rate_limit import fixed_window_rate_limiter, sliding_window_rate_limiter


router = APIRouter(prefix="/rate-limit",
                   tags=["RateLimit"])

@router.get('/protected-data', dependencies=[Depends(sliding_window_rate_limiter)])
async def get_protected_data():
    # This endpoint is protected by rate limiter.
    return {"message": "You have successfully accessed protected data!"}