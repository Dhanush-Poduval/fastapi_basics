from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
app=FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    


@app.post('/blog',status_code=201)
def create(blog:schemas.Blog , db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title , body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@app.get('/blog',response_model=List[schemas.ShowBlog])
def all( db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()

    return blogs

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id , request:schemas.Blog,db:Session=Depends(get_db)):
    pass

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first() #gives the first result only
    if not blog:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Blog with {id} not available")
    return blog
@app.delete('/blog/{id}')
def destroy(id ,db:Session=Depends(get_db) ):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'done'}

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.post('/user')
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get('/user',response_model=List[schemas.ShowUser])
def see_user(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

