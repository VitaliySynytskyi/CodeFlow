import os
import tempfile
from config import Config
import pytest

from app import create_app, db
from models import User


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@test.com',
        'password': 'testpassword',
    })

    assert response.status_code == 302
    assert User.query.filter_by(username='testuser').first() is not None


def test_login(client):
    # register user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@test.com',
        'password': 'testpassword',
    })

    # login user
    response = client.post('/login', data={
        'email': 'testuser@test.com',
        'password': 'testpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Hello, testuser!' in response.data


def test_logout(client):
    # register user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@test.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    })

    # login user
    client.post('/login', data={
        'email': 'testuser@test.com',
        'password': 'testpassword'
    })

    # logout user
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'You have been logged out.' in response.data
