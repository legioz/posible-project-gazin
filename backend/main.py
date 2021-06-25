from fastapi import FastAPI
from api.router import router as api_router
from core.config import PROJECT_NAME, DEBUG

VERSION = '0.0.2'

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

app.include_router(api_router, prefix='/api')
