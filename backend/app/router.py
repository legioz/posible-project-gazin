from fastapi import APIRouter
from app.routes import (
    provisional_front_v1, 
)

router = APIRouter()
router.include_router(provisional_front_v1.router, include_in_schema=False)
