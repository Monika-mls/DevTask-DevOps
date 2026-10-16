import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'test.db')})
    return app.test_client()


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'DevTask' in response.data


def test_add_and_complete_task(client):
    response = client.post('/add', data={'title': 'Finish DevOps project'}, follow_redirects=True)
    assert b'Finish DevOps project' in response.data
    assert b'Pending' in response.data
    response = client.post('/toggle/1', follow_redirects=True)
    assert b'Completed' in response.data


def test_delete_task(client):
    client.post('/add', data={'title': 'Temporary task'})
    response = client.post('/delete/1', follow_redirects=True)
    assert b'Temporary task' not in response.data


def test_reject_blank_task(client):
    response = client.post('/add', data={'title': '   '}, follow_redirects=True)
    assert b'No tasks yet' in response.data


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}
