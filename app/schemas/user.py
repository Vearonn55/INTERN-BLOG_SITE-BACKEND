from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class UserRegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: EmailStr
    password: constr(min_length=6)

class RegisterResponse(BaseModel):
    message: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

class UserDeleteMessageOut(BaseModel):
    message: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }

class UserRoleUpdateSchema(BaseModel):
    role: constr(min_length=1)

class UsersListResponse(BaseModel):
    users: List[UserOut]

    model_config = {
        "from_attributes": True
    }
