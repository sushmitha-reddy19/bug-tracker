import pytest
from app import app, BUGS

@pytest.fixture(autouse=True)
def reset():
    BUGS.clear()

@pytest.fixture
def client():
    return app.test_client()

def test_create_bug(client):
    r = client.post('/bugs', json={'title': 'Crash', 'severity': 'high'})
    assert r.status_code == 201 and r.json['status'] == 'open'

def test_empty_title_rejected(client):
    assert client.post('/bugs', json={'title': ' ', 'severity': 'low'}).status_code == 400

def test_invalid_severity_rejected(client):
    assert client.post('/bugs', json={'title': 'x', 'severity': 'urgent'}).status_code == 400

def test_list_filter_and_pagination(client):
    client.post('/bugs', json={'title': 'a', 'severity': 'low'})
    client.post('/bugs', json={'title': 'b', 'severity': 'high'})
    r = client.get('/bugs?page=1&size=1&status=open')
    assert r.status_code == 200 and len(r.json['items']) == 1 and r.json['pages'] == 2

def test_invalid_page_handled(client):
    assert client.get('/bugs?page=nope').status_code == 400

def test_update_and_delete(client):
    bug = client.post('/bugs', json={'title': 'x', 'severity': 'medium'}).json
    assert client.patch(f"/bugs/{bug['id']}", json={'status': 'closed'}).json['status'] == 'closed'
    assert client.delete(f"/bugs/{bug['id']}").status_code == 200
