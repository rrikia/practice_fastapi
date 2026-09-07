from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# We need the app from main.py 

# Create a router object
router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )


# Create a user, like the route create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Before creating a user, hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) 
    db.add(new_user)
    # Commit the change to the database
    db.commit()
    db.refresh(new_user) # Pull new values back from DB (like generated ID)
    return new_user

# Get user by id 
# Remember to specify response model
# /users/{id}
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exist")
    return user