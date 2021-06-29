from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    auth_token = request.headers.get('Authorization') if request.headers.get('Authorization') else None
    return templates.TemplateResponse('index.html', {'request': request, 'auth_token': auth_token})


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/create', response_class=HTMLResponse)
async def create(request: Request, update: int=None):
    return templates.TemplateResponse('create.html', {'request': request, 'update': update})


# @router.get('/update', response_class=HTMLResponse)
# async def update(request: Request):
#     return templates.TemplateResponse('update.html', {'request': request})


