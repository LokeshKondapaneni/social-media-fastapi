from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from ..database import get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session= Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with given id- {id}')
    return user