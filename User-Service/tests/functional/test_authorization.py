import json

def test_register(test_client):
    payload = json.dumps({   
        "name" : "Admin",
        "email" : "Admin@admin.com",
        "password" : "Test@123"
    })
    response = test_client.post(
        '/register',
        data=payload,
        headers={"Content-Type": "application/json"})
    if response.status_code == 400:
        assert b'User already exists!!' in response.data
    else:
        assert response.status_code == 200
        assert b'New user created' in response.data

def test_login(test_client):
    payload = json.dumps({
        "email" : "Admin@admin.com",
        "password": "Test@123"
    })
    response = test_client.post(
        '/login',
        data=payload,
        headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert b"token" in response.data 