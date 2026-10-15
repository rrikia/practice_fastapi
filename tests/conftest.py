from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from typing import Generator
from app.config import settings
from app.database import get_db, Base
from app.main import app
from typing import Generator

load_dotenv(".env")

database_password = os.getenv("DATABASE_PASSWORD")
print("Password is not none", database_password is not None)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
                            )


# Safety check: drop_all() deletes everything, so refuse to run on a non-test database
if not settings.DATABASE_NAME.endswith("_test"):
    raise RuntimeError(
        f"Refusing to run tests on '{settings.DATABASE_NAME}'. "
        "The test database name must end with '_test'."
    )

# Any fixtures defined in here will be available to all test files in the tests directory
# engine responsible for sqlalchemy to connect to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database, use a session
TestSessionLocal = sessionmaker(
    autoflush=False, 
    bind=engine
    )

@pytest.fixture (scope="function")
def session() -> Generator[Session, None, None]:
    # drop all the tables in the test database to ensure a clean state
    # no need to worry about duplicate users
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function that runs before each test to set up the test database
# the client fixture will call the session fixture before it runs 
# Use session to access the test database 
@pytest.fixture (scope="function")
def client(session) -> Generator[TestClient, None, None]:
    # Create a dependency
    # Returns a generator that yields a database session and ensures that the session is closed after use
    # Basically returning the session local 
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # yield is used: run our code before we return our test client 
    yield TestClient(app)
    # run our code after our test finishes 

@pytest.fixture
def test_user (client):
    user_data = {"email":"you7@gmail.com",
                 "password":"password12377"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # Return the data of the newly created user 
    # so test_login_user can use it to log in
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

database_password = os.getenv("DATABASE_PASSWORD")
print("Password is not none", database_password is not None)
