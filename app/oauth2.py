from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="login")
# Secret_KEY
# Algorithm
# Expiration time t
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    
    
    
# We use this function to verify the access TOKEN, to be sure the access token the user is sending to us when he wants to access any resource
def verify_acces_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        id:str = str(payload.get("user_id"))
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    # 7:26:57
# We can pass this as a dependency to our login, cause it would take the token,id and verify it and then it would extract the id and fetch the user from the db as well if we want it to.
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentails", headers={"WWW-Authenticate":"Bearer"})
    
    
    token = verify_acces_token(token,credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
    



# verify access token returns the user id, which the get_current_user can then use to fetch the user from the db based on this token.



#  We can set up query parameters on our code, this allows us to filter some certain stuffs on our code
# Limit: we pass it as a param in our function and we can  pass it in our search query and pass the value, useful in pagination
# Skip: we pass it in our search parameters as well, this is useful in skipping some certain results used with the query offset
# Search: We use search params to search of filter our results as well.





# Voting/Like requirements
# User should be able to like a post
# user should be able to like a post once
# Retrieving posts should also fetch the total number of likes