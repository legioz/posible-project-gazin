from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel
from core.databases import Connection
from fastapi import Depends, APIRouter, HTTPException, Form
import secrets
from .auth_v1 import get_current_user

router = APIRouter()


class DeveloperIn(BaseModel):
    name: str
    sex: str
    hobby: str
    birthdate: date


class DeveloperOut(BaseModel):
    id: int
    name: str
    sex: str
    hobby: str
    birthdate: date
    is_deleted: bool
    inserted_on: datetime
    updated_on: Optional[datetime]=None


@router.post('')
async def create_developer(data: DeveloperIn, user=Depends(get_current_user)):
    """
    Create a developer
    """
    try:
        args = [data.name, data.sex, data.hobby, data.birthdate]
        if data.sex not in ['M', 'F']:
            raise Exception()
        with Connection() as db:
            sql = '''
                INSERT INTO developer
                (name, sex, hobby, birthdate) VALUES 
                (%s, %s, %s, %s)
                RETURNING id
            '''
            result = db.query_dict(sql, args)
            id = result[0].get('id') if result else None
        return {'ok': True, 'id': id}
    except:
        raise HTTPException(400, 'Bad Request')


@router.get('', response_model=List[DeveloperOut])
async def read_developers(name: str=None, sex: str=None, hobby: str=None, birthdate: date=None, user=Depends(get_current_user)):
    """
    Retornar os dados de todos os desenvolvedores cadastrados,
    ou utiliza o *query parameters* para realizar um filtro.
    """
    try:
        sql_args = ''
        args = []
        if name:
            sql_args += f' AND name LIKE %s'
            args.append(f'%{name}%')
        if sex:
            sql_args = f' AND sex = %s'
            args.append(sex)
        if hobby:
            sql_args += f' AND hobby LIKE %s'
            args.append(f'%{hobby}%')
        if birthdate:
            sql_args += f' AND birthdate = %s'
            args.append(birthdate)
        with Connection() as db:
            sql = '''
                SELECT *
                FROM developer
                WHERE 1 = 1
                  AND is_deleted = 0
                  {}
            '''.format(sql_args)
            result = db.query_dict(sql, args)
        devs = result if result else None
        if not devs:
            raise Exception()
        return devs
    except:
        raise HTTPException(404, 'Not Found')


@router.get('/{id}', response_model=DeveloperOut)
async def read_developer(id: int, user=Depends(get_current_user)):
    """
    Filtrar devs buscando ID específico passado via *path parameters*
    """
    try:
        with Connection() as db:
            sql = '''
                SELECT *
                FROM developer
                WHERE 1 = 1
                  AND is_deleted = 0
                  AND id = %s
            '''
            result = db.query_dict(sql, [id])
        dev = result[0] if result else None
        if dev is None:
            raise Exception()
        return dev
    except:
        raise HTTPException(404, 'Not Found')


@router.put('/{id}')
async def update_developer(id: int, data: DeveloperIn, user=Depends(get_current_user)):
    """
    Atualiza um desenvolvedor já cadastrado
    """
    try:
        args = [
            data.name, 
            data.sex, 
            data.hobby, 
            data.birthdate, 
            id
        ]
        if data.sex not in ['M', 'F']:
            raise Exception()
        with Connection() as db:
            sql_check = '''
                SELECT *
                FROM developer
                WHERE id = %s
            '''
            result = db.query_dict(sql_check, [id])
            if not result:
                raise Exception()
            sql = '''
                UPDATE developer
                SET updated_on = NOW(),
                    name = %s,
                    sex = %s,
                    hobby = %s,
                    birthdate = %s
                WHERE is_deleted = 0
                  AND id = %s
            '''
            db.execute(sql, args)
        return {'ok': True}
    except:
        raise HTTPException(400, 'Bad Request')


@router.delete('/{id}')
async def delete_developer(id: int, user=Depends(get_current_user)):
    """
    Realizar a **deleção lógica** de um desenvolvedor específico
    """
    try:
        with Connection() as db:
            sql_check = '''
                SELECT *
                FROM developer
                WHERE id = %s
            '''
            result = db.query_dict(sql_check, [id])
            if not result:
                raise Exception()
            sql = '''
                UPDATE developer
                SET is_deleted = 1
                WHERE id = %s
            '''
            db.execute(sql, [id])
        return {'ok': True} 
    except:
        raise HTTPException(400, 'Bad Request')
