from fastapi import FastAPI,HTTPException,status,Response,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from . database import  engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

# try:
#     conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='3149',cursor_factory=RealDictCursor)
#     cursor=conn.cursor()
#     print("Database connected Successfully!!!")
# except Exception as error:
#     print("Database connection failled",error)
    

app=FastAPI()



class Posts(BaseModel):
    title:str
    content:str
    published: bool

@app.get('/')
async def root():
    return{"message":"Welcome to fastapi"}

@app.get('/post')
async def get_posts(db:Session=Depends(get_db)):
    #without ORM
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()
    # return {"posts":posts}
    
    #with ORM
    post=db.query(models.Post).all()
    return{"Data":post}

@app.post('/post',status_code=status.HTTP_201_CREATED)
async def submit_post(post:Posts,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published)VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)# it work similar like RETURNING *
    
    return{ "newPost":new_post}

@app.get('/post/{id}')
async def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",str(id))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    return{"post":post}

@app.put('/post/{id}')
async def update_post(id:int,post:Posts,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts set title=%s,content=%s,published=%s where id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    
    
    #This is one way we can update but here we cannot use refresh
    # get_post=db.query(models.Post).filter(models.Post.id==id).update({models.Post.title:post.title,models.Post.content:post.content,models.Post.published:post.published})
   
   
    #This is second way to update data
    get_post=db.query(models.Post).filter(models.Post.id==id).first()
    if get_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data of id-{id} Not Found in database")
    get_post.title=post.title
    get_post.content=post.content
    get_post.published=post.published
    db.commit()
    db.refresh(get_post)
    
    return{"data":get_post}

@app.delete('/post/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    # if deleted_post==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id{id} Not found")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data of Id-{id} Not found")
    
    db.delete(post)
    db.commit()
    return {"Message":"Data of id-{id} Deleted Successfully"}