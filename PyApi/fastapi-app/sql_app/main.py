from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

from . import crud, models, schemas
from .database import SessionLocal, engine
from .helper import VerifyToken

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def get_current_user(response: Response, token: str = Depends(token_auth_scheme), db: Session = Depends(get_db)): 
#     """A valid access token is required to access this route"""
#     try: 
#         result = VerifyToken(token.credentials).verify()  # 👈 updated code
@app.get("/api/private")
def private(response: Response, token: str = Depends(token_auth_scheme)): 
    """A valid access token is required to access this route"""
 
    result = VerifyToken(token.credentials).verify()  

    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
 
    return result

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@app.post('/users/{user_id}/home-works/', response_model=schemas.HomeWork)
def create_home_work_for_user(user_id: int, home_work: schemas.HomeWorkCreate, db: Session = Depends(get_db)):
    return crud.create_user_home_work(db=db, home_work=home_work, user_id=user_id)


@app.get('/home-works/', response_model=List[schemas.HomeWork])
def read_home_works(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    home_works = crud.get_home_works(db, skip=skip, limit=limit)

    return home_works