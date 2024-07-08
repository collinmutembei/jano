from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.schemas import AuthToken, User, UserCredentials
from src.models import User as UserModel
from src.database import get_db
from src.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register", response_model=User)
def register_user(credentials: UserCredentials, db: Session = Depends(get_db)):
    db_user = (
        db.query(UserModel).filter(UserModel.username == credentials.username).first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(credentials.password)
    new_user = UserModel(username=credentials.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=AuthToken)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = (
        db.query(UserModel).filter(UserModel.username == form_data.username).first()
    )
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return AuthToken(access_token=access_token)


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserCredentials,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"Not authorized to update user {user_id}"
        )
    updated_user = user_update.model_dump(exclude_unset=True)
    for key, value in updated_user.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
