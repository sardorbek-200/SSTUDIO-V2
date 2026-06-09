from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=["shop-cart"])

@router.get("/")
async def view_cart():
    return {"cart": []}
