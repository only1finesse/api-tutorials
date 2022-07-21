from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI
from models import Gender, Role, User

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("06a6f016-95bb-4304-91ac-86ee738b430b"), 
        first_name="Rene",
        last_name="Shen",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    ), 
    User(
        id=UUID("06a3f016-95bb-4304-91ac-86ee738b430b"),
        first_name="Alec",
        last_name="Baldwin",
        gender=Gender.female,
        roles=[Role.admin, Role.user] 
    )
]


@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/api/users")
async def fetch_users():
    return db;

@app.post("/api/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db: 
        if user.id == user_id:
            db.remove(user)
            return "Deleted"
        else:
            return "This user does not exist"
