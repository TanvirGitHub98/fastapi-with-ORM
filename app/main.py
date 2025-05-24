from fastapi import FastAPI,Depends,HTTPException,Response,status
from .database import Base,get_db,engine
from . import models
from sqlalchemy.orm import Session
from .schemas import Post,PostResponse
from typing import List
from .routers import post

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
@app.get('/')
async def root():
    return{"Message":"Welcome to FastAPi Project"}
