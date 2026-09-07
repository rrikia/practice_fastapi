from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Each user has a unique email
    # filter the users by comparing the email of the user that tries to log ing
    # in the request
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # verify the password of the request

    if not utils.verify(user_credentials.password, user.password):
        # If wrong password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # Inside the payload, the data we want is only user_id
    access_token = oauth2.create_access_token(data = {"user_id": str(user.id)})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}