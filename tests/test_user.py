from app import schemas
from jose import jwt
import pytest
from app.config import settings
   
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


    
    
    

# Right now as it stands our tests are dependent on eachother which is bad practice. You don't want to make your tests be dependent on eachother instead they should be a standalone unit independently.


def test_create_user(client):
    res = client.post("/users/", json={"email":"virgil@gmail.com","password":"virgil"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "virgil@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client,create_test_user):
    res = client.post("/login",data={"username":create_test_user['email'],"password":create_test_user['password']})
    
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == create_test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
    
    
# Here we're testing wrong credentials to see if it passes or not, and we're using parametrize, you can see from the function we checked for a wrong password and it returned a 403 which we are testing for
    
@pytest.mark.parametrize("email,password,status_code", [
("wrongemail@gmail.com","password123",403),
("virgil@gmail.com","wrongpassword",403),
("wrongemail@gmail.com","wrongpassword",403),
(None,"password123",422),
('virgil@gmail.com',None,422)
])
def test_incorrect_login(create_test_user,client,email,password,status_code):
    res = client.post("/login", data={"username": email,'password':password})
    
    assert res.status_code == status_code
