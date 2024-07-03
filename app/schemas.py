from datetime import datetime
from typing import Optional
import email_validator
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes= True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]= None

class PostBase(BaseModel):
    """
    Base Post instance model
    """
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse
    class Config:
        from_attributes = True # Previous versions use orm_mode

class PostOut(BaseModel):
    Posts: Post
    votes: int

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir: bool