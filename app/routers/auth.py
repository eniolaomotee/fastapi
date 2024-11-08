from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas,models,utils,oauth2
from sqlalchemy.orm import Session



router = APIRouter(
    tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
# Using the Oauth password request form
def login_user(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):

# Using the normal way with schemas etc.
# def login_user(user_credentials:schemas.UserLogin,db:Session=Depends(get_db)):

    # When getting data from the dict(user_credentials) it returns the username and the password not the email and the password we do have on our normal dict previously so we'd need to check it against "user_credentials.username"

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    # So here we're verifying if the password on the database and the password being sent are the same via our hashing function.
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    
    # Create a token
    # return a token
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
        
    
    