from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["shop-orders"])

@router.get("/")
async def list_orders():
    return {"orders": []}
