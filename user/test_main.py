from fastapi.testclient import TestClient 
from .main import app 

client= TestClient(app) 

data = {"name": "user5","email":"user5@gmail.com","password":"user5"}

#Testcase for post api
def test_create():
    response=client.post("/create",json=data)
    if response.status_code == 400:
        assert response.json() == {"detail":"User already exists"}
    else:
        assert response.status_code == 201

#Testcase for get api
def test_retrieve():
    response=client.get("/read",json=data)
    if response.status_code == 400:
        assert response.json() == "User not found"
    else:
        assert response.status_code == 200
        assert response.json()

#Testcase for put api
def test_update():
    response=client.put("/update/",json={"name":"ravi","email":"ravi123@gmail.com"})
    if response.status_code == 404:
        assert response.json()
    else:
        assert response.status_code == 202 

#Testcase for delete api
def test_delete():
    response=client.delete("/delete/",json=data)
    if response.status_code == 404:
        assert response.json()
    else:
        assert response.status_code == 204
    


    