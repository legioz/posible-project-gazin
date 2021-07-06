from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from core.databases import Connection
from core.config import SECRET_KEY
import secrets
from passlib import pwd
from pydantic import BaseModel


router = APIRouter()

ALGORITHM = 'HS512'
ACCESS_TOKEN_EXPIRE_MINUTES = 15 * 999
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token/')


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_new_session_key():
    return secrets.token_urlsafe(20) + pwd.genword(entropy=100, length=20)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with Connection() as db:
            sql = '''
                SELECT * 
                FROM user 
                WHERE username = %s 
                  AND is_active = 1 
                LIMIT 1
            '''
            result = db.query_dict(sql, [username])
            user = result[0] if result else None
    return user


def authenticate_user(username: str, password: str):
    try:
        user = get_user(username)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail='Database connection error')
    if not user:
        return False
    if not verify_password(password, user.get('password')):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'iat': datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
    except Exception:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@router.post('/token/', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    """
    Authenticate user and generate **access token** 
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.get('username')}, 
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
