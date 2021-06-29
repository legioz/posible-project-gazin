from fastapi.testclient import TestClient
from api.routes.developer_v1 import router
from main import app

client = TestClient(app)

auth_token = None
dev_id = None


def test_login():
    global auth_token
    response = client.post(
        '/api/auth/token/',
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'username': 'admin', 'password': 'admin'}
    )
    assert response.status_code == 200
    auth_token = response.json().get('access_token')


def test_create_dev():
    global dev_id
    response = client.post(
        '/api/developers',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
        json={
            'name': 'Luiz Felipe',
            'sex': 'M',
            'hobby': 'Academia e Luta de Braço',
            'birthdate': '1997-02-01',
        }
    )
    assert response.status_code == 200
    dev_id = response.json().get('id')


def test_read_all_dev():
    response = client.get(
        '/api/developers', 
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_dev():
    response = client.get(
        f'/api/developers/{dev_id}',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
    )
    assert response.status_code == 200


def test_update_dev():
    response = client.put(
        f'/api/developers/{dev_id}',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
        json={
            'name': 'Luiz Felipe Lima',
            'sex': 'M',
            'hobby': 'Natação',
            'birthdate': '1997-02-10',
        }
    )
    assert response.status_code == 200


def test_delete_dev():
    client.delete(
        f'/api/developers/{dev_id}',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
    )
    response = client.get(
        f'/api/developers/{dev_id}',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
    )
    assert response.status_code == 404