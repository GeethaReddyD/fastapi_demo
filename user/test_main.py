from fastapi.testclient import TestClient 
from .main import app 

client= TestClient(app) 

data = {"name": "user5","email":"user5@gmail.com","password":"user5"}

# Testcase for post API.
def create_user():
    response=client.post("/users",json=data)
    if response.status_code == 400:
        assert response.json() == {"detail":"User already exists"}
    assert response.status_code == 201

# Testcase for get API.
def user_list():
    response=client.get("/users",json=data)
    if response.status_code == 400:
        assert response.json() == "User not found"
    assert response.status_code == 200
    assert response.json()

# Testcase for put API.
def user_update():
    response=client.put("/users/4",json={"name":"ravi","email":"ravi123@gmail.com"})
    if response.status_code == 404:
        assert response.json()

    assert response.status_code == 202 

# Testcase for delete API.
def user_delete():
    response=client.delete("/users/4",json=data)
    if response.status_code == 404:
        assert response.json()
    
    assert response.status_code == 204
    
        
    
    