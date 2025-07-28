from fastapi import FastAPI
from . import schemas
app=FastAPI()

@app.post('/blog')
def created(blog:schemas.Blog):
    return{'data':f'This blog of title {blog.title} and its {blog.body} have been created '}