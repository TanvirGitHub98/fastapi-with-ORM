from fastapi import FastAPI,APIRouter,Depends,HTTPException,Response,status
from typing import List
from sqlalchemy.orm import Session
from .. import models
from .. database import get_db
from ..schemas import PostResponse,Post

router=APIRouter(
    prefix='/post',
    tags=['Post']
)


@router.get('/',response_model=List[PostResponse])
async def get_all_data(db:Session=Depends(get_db)):
    data=db.query(models.Post).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No data found in database")
    return data

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=PostResponse)
async def submit_post(post:Post, db:Session=Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get('/{id}',response_model=PostResponse)
async def get_post(id:int,db:Session=Depends(get_db)):
    data=db.query(models.Post).filter(models.Post.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Data Found for id-{id}")
    return data

@router.put('/{id}',response_model=PostResponse)
async def update_post(id:int,post:Post,db:Session=Depends(get_db)):
  data=db.query(models.Post).filter(models.Post.id==id).first()
  if not data:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No data found in database fro id-{id}')
  data.title=post.title
  data.content=post.content
  data.published=post.published
  db.commit()
  db.refresh(data)
  return data   

@router.delete('/{id}')
async def delete_post(id:int,db:Session=Depends(get_db)):
    data=db.query(models.Post).filter(models.Post.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Data for id-{id} Not Found in database')
    db.delete(data)
    db.commit()
    #db.refresh(data)
    return  f'Data Deleted Successfully For id-{id}'