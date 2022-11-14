import sqlalchemy

from databases import Database
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List

DATA_BASE_URL = 'sqlite+aiosqlite:///example.db'
database = Database(DATA_BASE_URL)

metadata = sqlalchemy.MetaData()
posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("created_date", sqlalchemy.DATETIME),
    sqlalchemy.Column("rubrics", sqlalchemy.String)
)
app = FastAPI()

class Message(BaseModel):
    detail: str
    class Config:
        schema_extra = {
            "example": {
                "detail": "Post not found."
            }
        }


class Post(BaseModel):
    id: int
    text: str
    created_date: datetime
    rubrics: str


class DefaultResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Ok."
            }
        }


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/posts", status_code=200, 
    response_model=List[Post],
    description="Get 20 posts sorted by created time from database.")
async def read_posts():
    return await database.fetch_all("SELECT * FROM posts ORDER BY created_date LIMIT 20")


@app.delete("/posts/{id}", 
    status_code=200, 
    description="Delete post from database.", 
    response_model=DefaultResponse,
    responses={404: {"model": Message}})
async def delete_post(id: int):
    query = posts.delete().where(posts.c.id == id)
    
    res = await database.execute(query)
    
    if (res == 0):
        raise HTTPException(status_code=404, detail="Post not found.")      

    return {
        "message": "Ok."
    }

@app.get("/posts/{id}", 
    status_code=200, 
    description="Get post from database.", 
    response_model=Post,
    responses={404: {"model": Message}})
async def get_post(id: int):
    query = posts.select().where(posts.c.id == id)
    
    res = await database.fetch_one(query)
    if (res is None):
        raise HTTPException(status_code=404, detail="Post not found.")      

    return res


@app.get("/", response_class=HTMLResponse)
async def send():
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <title>Posts</title>
        </head>

        <body>
            <p><a href="/docs">Docs</a></p>
        </body>
    </html>
    """


@app.get("/posts", status_code=200, 
    response_model=List[Post],
    description="Get 20 posts sorted by created time from database.")
async def read_posts():
    return await database.fetch_all("SELECT * FROM posts ORDER BY created_date LIMIT 20")
