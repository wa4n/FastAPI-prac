from typing import Optional, List
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import Models, Schemas, Utility
from ..Models import Post
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users'] 
)




@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Schemas.UserOut)
def create_user(user: Schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_email = db.query(Models.User.email).filter(Models.User.email == user.email).first()

    if user_email:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"email in use")

    hashed_pass = Utility.hash(user.password)
    user.password = hashed_pass

    new_user = Models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=Schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id}, not found")
    return user
