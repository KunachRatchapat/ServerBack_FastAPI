from typing import Optional

from pydantic import BaseModel


class Register(BaseModel):
    username: str
    password: str
    email: str
    surname: str


class Login(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    email: str
    username: str
    surname: str
    role: str
    is_verified: bool = False


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UpdateProfile(BaseModel):
    username: Optional[str] = None
    surname: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class VerifyEmailRequest(BaseModel):
    token: str
