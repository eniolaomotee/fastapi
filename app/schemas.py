from pydantic import BaseModel,EmailStr, conint,Field
from datetime import datetime
from typing import Optional,Literal
# Schemas define how you structure getting your data from the users and response model structures how you can send data to the user ie not sending all the data from the post table to the user.

class PostBase(BaseModel):
    title: str
    content : str
    published: bool = True 
    
    
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
        
    class Config:
        from_attributes = True

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id : int
    owner: UserOut
    
    class Config:
        from_attributes = True 

# Make sure you inherit from BaseModel and not PostBase
class PostOut(BaseModel):
    Post: Post
    votes:int
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
        
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type:str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: int = Field(...,ge=0,le=1)