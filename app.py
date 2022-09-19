from cgitb import text
from datetime import datetime
from lib2to3.pytree import Base
import string
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

# Posts Model
# esquema de cómo van a lucir las publicacinones
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False
#creando rutas
@app.get('/') #Get método HTTP y '/' nombre de la ruta 
def read_root():
    return {"Welcome": "Bienvenido a mi REST API"}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts') 
#creando una función que cuando visite /posts a través del método post
def save_post(post: Post):
    post.id = str(uuid()) #genera un string aleatorio y se la asigna a la propiedad id de la publicación 
    posts.append(post.dict()) #después lo convierte en diccionario y luego lo añade a arreglo
    return posts[-1]


@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts: #recorre por cada publicación la lista de publicaciones 
        if post["id"] == post_id: #si el id de cada publicación es igual a cada parametro que me están pasando retorna esa publicación
            return post
    raise HTTPException(status_code=404, detail="Post no encontrado")

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "la publicación ha sido eliminada"}
    raise HTTPException(status_code=404, detail="Post no encontrado")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatedPost.title
            posts[index]["content"] = updatedPost.content
            posts[index]["author"] = updatedPost.author
            posts[index]["created_at"] = updatedPost.created_at
            posts[index]["published_at"] = updatedPost.published_at
            posts[index]["published"] = updatedPost.published
            return {"message": "la publicación ha sido actualizada"}  
    raise HTTPException(status_code=404, detail="Post no encontrado")
