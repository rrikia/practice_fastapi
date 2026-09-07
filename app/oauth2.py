from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# Our log in endpoint 
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Expiration time of token, once a user has logged in

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    # data variable is the payload of the token
    # make a copy of it
    to_encode = data.copy()

    # Expiration time of 30 minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expire time to the dict to_encode
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        # First decode the user's token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # We extract the id from the payload 
        id: str = payload.get("user_id")

        # If there's no id, throw an error 
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

# Pass this as a dependecy
# Take the token, extract the user's id, verify that the token is correct
# 
def get_current_user(token: str = Depends(oauth2_schema), 
                     db: Session = Depends(database.get_db)):
    # when sth is wrong, credentials is wrong, or sth wrong with JWT token
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user