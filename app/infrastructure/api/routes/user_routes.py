from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User
from app.infrastructure.api.dependencies import get_user_use_cases


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str


router = APIRouter(prefix="/users", tags=["users"])

# Define dependencies at module level
user_use_cases_dependency = Depends(get_user_use_cases)


@router.get("/", response_model=List[User])
async def list_users(user_use_cases: UserUseCases = user_use_cases_dependency) -> List[User]:
    return await user_use_cases.list_users()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest, use_cases: UserUseCases = user_use_cases_dependency
) -> UserResponse:
    try:
        user = await use_cases.create_user(
            username=request.username, email=request.email, full_name=request.full_name
        )
        return UserResponse(
            id=str(user.id), username=user.username, email=user.email, full_name=user.full_name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
