
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, "users": users})


@app.get('/user/{user_id}')
async def read_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, "user": users[user_id-1]})


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: int = Path(ge=18, le=120, description='Enter age')) -> dict:
    user_id = len(users) + 1
    users.append(User(id=user_id, username=username, age=age))
    return {"message": f"User {user_id} is registered"}


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: Annotated[str, Path(min_length=5, max_length=20,
                                                                  description='Enter username')],
                      age: int = Path(ge=18, le=120, description='Enter age')) -> dict:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return {"message": f"User {user_id} is updated"}
        else:
            raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> dict:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": f"User {user_id} has been deleted"}
    raise HTTPException(status_code=404, detail="User was not found")
