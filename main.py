from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import  RealDictCursor
import time
from . import models
from database import engine, SessionLoacl

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLoacl()
    try:
        yield db
    finally:
        db.close()
        

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5433, database='fast_api', user='postgres', password='root', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Database connect was not established")
        print("Error:",  error)
        time.sleep(2)

    
posts = [
    {
        "id": 1, 
        "title": "virat's 81 century", 
        "content":"Virat had scored a 100 in yesterday's test match against Austrila",
        "published":True,
        "rating":5
    },
    {
        "id": 2, 
        "title": "most valuable company", 
        "content":"Nvidia is the most valuable company in the world",
        "published":True,
        "rating":3
    }
]


# to find a post by id
def get_post_by_id(id: int)-> int:
    for post in posts:
        if post['id'] == id:
            return post
    return None


# to find a index of post with id
def get_post_index(id: int)-> int:
    for index, post in enumerate(posts):
        if post['id'] == id:
            return index
    return None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM POST""")
    db_posts = cursor.fetchall()
    return {
        "data": db_posts
    }


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO POST(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.put("/post/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE POST SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id '{id}' does not exist")
    return {
        "data": updated_post
    }


@app.get("/post/latest")
async def get_latest_post():
    latest_post = posts[len(posts)-1]
    return {
        "data": latest_post
    }


@app.get("/post/{id}")
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM POST WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= f"post with id '{id}' was not found"
            )
    return {
        "data": post
    }


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM POST WHERE id = %s RETURNING * """, (str(id),))
    deletd_post = cursor.fetchone()
    conn.commit()
    if not deletd_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id '{id}' was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
