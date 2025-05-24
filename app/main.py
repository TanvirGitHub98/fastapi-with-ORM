from fastapi import FastAPI,HTTPException,status,Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='3149',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connected Successfully!!!")
except Exception as error:
    print("Database connection failled",error)
    

app=FastAPI()

class Posts(BaseModel):
    title:str
    content:str
    published: bool

@app.get('/')
async def root():
    return{"message":"Welcome to fastapi"}

@app.get('/post')
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts=cursor.fetchall()
    return {"posts":posts}

@app.post('/post',status_code=status.HTTP_201_CREATED)
async def submit_post(post:Posts):
    cursor.execute("""INSERT INTO posts(title,content,published)VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return{ "newPost":new_post}

@app.get('/post/{id}')
async def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",str(id))
    post=cursor.fetchone()
    
    return{"post":post}

@app.put('/post/{id}')
async def update_post(id:int,post:Posts):
    cursor.execute("""UPDATE posts set title=%s,content=%s,published=%s where id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    return{"data":updated_post}

@app.delete('/post/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id{id} Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

