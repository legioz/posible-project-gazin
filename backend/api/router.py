from fastapi import APIRouter
from api.routes import (
    auth_v1, 
    developer_v1
)

router = APIRouter()

router.include_router(auth_v1.router, prefix='/auth', tags=['Auth'], include_in_schema=False)
router.include_router(developer_v1.router, prefix='/developers', tags=['Developers'])
