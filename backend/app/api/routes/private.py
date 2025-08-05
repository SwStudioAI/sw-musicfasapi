from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import SessionDep
from app.crud import create_user
from app.models import UserCreate, UserPublic

router = APIRouter(tags=["private"], prefix="/private")



class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user_private(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user (private endpoint).
    """
    user_create = UserCreate(
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False,
    )
    user = create_user(session=session, user_create=user_create)
    return user
