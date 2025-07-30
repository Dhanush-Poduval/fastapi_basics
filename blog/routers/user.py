from fastapi import FastAPI,Depends,Response,status,HTTPException,APIRouter
from .. import schemas,models,database

from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
router=APIRouter()
get_db=database.get_db
pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post('/user')
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get('/user',response_model=List[schemas.ShowUser])
def see_user(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users
@router.get('/user/{id}',response_model=schemas.ShowUser)
def see_specific_user(id,db:Session=Depends(get_db),):
    users=db.query(models.User).filter(models.User.id==id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f"User of {id} does not exist")
    return users