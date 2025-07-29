from fastapi import FastAPI
from . import schemas,models
from .database import engine
app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post('/blog')
def created(blog:schemas.Blog):
    return{'data':f'This blog of title {blog.title} and its {blog.body} have been created '}