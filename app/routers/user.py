from fastapi import FastAPI,Depends,status,HTTPException,Response,APIRouter
from .. import models,utils,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create User
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):  
    
    # Hash the password - user.password
    hashed_passwrord = utils.hash(user.password)
    user.password = hashed_passwrord
    
    new_user = models.User(**user.dict())
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()                    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"email address already exists please try another")
        
    return new_user

# Get User 
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} not found")
    
    
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session = Depends(get_db)):
    
    user_to_delete = db.query(models.User).filter(models.User.id == id)
    
    
    
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")

    user_to_delete.delete(synchronize_session=False)
    
    db.commit()
    
    
    
# Testing with pytest