import pytest
from app import schemas
from jose import jwt
from app.config import settings


# Test the root endpoint
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    # To see the actual payload returned by the endpoint, 
    # use response.json() to get the JSON response

    assert response.json() == {"message": "Hello World"}


# Each test should be independent of each other

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    # must delete this user whenever you run the test again, otherwise it will fail 
    # because of unique constraint on email

    # print(res.json())
    # assert res.json().get("email") == "hello123@gmail.com"

    # To validate the response against the UserOut schema, we can use the ** operator to unpack the dictionary 
    # returned by res.json() into the UserOut model. 
    # This ensures that the response matches the expected structure defined in the schema.

    # .dict() is changed to model_dump() in Pydantic v2 
    # new_user = schemas.UserOut(**res.json())

    # this is equivalent to the above line, but more explicit and clear
    new_user = schemas.UserOut.model_validate(res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# No need to have the trailing slash: /login 
# Check in the corresponding routers file: routers/auth.py
# we have to send the data as form data, not JSON, because we are using OAuth2PasswordRequestForm
# test_user and client are fixtures defined in conftest.py, 
# so we can use them as parameters in the test function
def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == (str) (test_user['id'])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# Different scenarios: wrong email, wrong password, both wrong, missing email, missing password
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
