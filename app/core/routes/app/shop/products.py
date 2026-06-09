from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["shop-products"])

@router.get("/")
async def list_products():
    return {"products": []}
