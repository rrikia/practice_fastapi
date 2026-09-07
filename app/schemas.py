from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint

# class that extends BaseModel
# stores schema for a request to create_post
# Pydantic model, schema for request

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  

# inherits class PostBase 
# Schema for a post for the request to create a post
class PostCreate(PostBase):    
    pass

# Need the library of pydantic of email validator
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# "Shape" of the user's info that is sent back as a response 
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Model schema for the HTTP response
# Schema to return a post to a user 
class Post(PostBase):
    id: int
    # The lower three are inherited from PostBase
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int
    # Return a pydantic model UserOut, called owner
    owner: UserOut
    # Config code, so that Pydantic can see that the response model is a dict
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    # dir stands for direction 
    # validate that its value is only 0 or 1 
    # le=1 means <= 1
    dir: Annotated[int, Field(le=1, ge=0)]
