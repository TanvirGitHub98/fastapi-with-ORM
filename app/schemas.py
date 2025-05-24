from pydantic import BaseModel

class Post(BaseModel):
    title:str
    content:str
    published:bool
    
class PostResponse(BaseModel):
    title:str
    content:str  
    class Config:
        orm_mode=True  
    