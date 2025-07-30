from fastapi import APIRouter,Depends
from .. import schemas,database,models
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends,Response,status,HTTPException
from .. import schemas,models

from sqlalchemy.orm import Session
from typing import List




router=APIRouter(
    tags=['blogs']
)

@router.get('/blog',response_model=List[schemas.ShowBlog])
def all( db:Session=Depends(database.get_db)):
    blogs=db.query(models.Blog).all()

    return blogs

@router.post('/blog',status_code=201)
def create(blog:schemas.Blog , db:Session=Depends(database.get_db)):
    new_blog=models.Blog(title=blog.title , body=blog.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}')
def destroy(id ,db:Session=Depends(database.get_db) ):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'done'}

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id , request:schemas.Blog,db:Session=Depends(database.get_db)):
    pass

@router.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response,db:Session=Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first() #gives the first result only
    if not blog:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Blog with {id} not available")
    return blog