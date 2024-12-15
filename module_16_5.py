            # Домашнее задание по теме "Шаблонизатор Jinja 2."


from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, constr, conint
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Пустой список для хранения пользователей
users = []

# Определение модели пользователя
class User(BaseModel):
    id: int
    username: constr(min_length=5, max_length=20)
    age: conint(ge=0)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Возвращает главную страницу со списком пользователей."""
    return templates.TemplateResponse("main.html", {"request": request, "users": users})

@app.post("/user/{username}/{age}", response_model=User)
def create_user(username: constr(min_length=5, max_length=20), age: conint(ge=0)):
    """Добавляет нового пользователя и возвращает его"""
    new_id = (users[-1].id + 1) if users else 1  # Максимальный ID + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_user(request: Request, user_id: int):
    """Возвращает пользователя по ID."""
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    """Удаляет пользователя по ID."""
    for index, user in enumerate(users):
        if user.id == user_id:
            del users[index]
            return {"detail": f"User {user_id} deleted"}
    raise HTTPException(status_code=404, detail="User was not found")

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(user_id: int, username: constr(min_length=5, max_length=20), age: conint(ge=0)):
    """Обновляет информацию о пользователе."""
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# Добавляем несколько пользователей для тестирования
create_user("UrbanUser", 24)
create_user("UrbanTest", 22)
create_user("Capybara", 60)





