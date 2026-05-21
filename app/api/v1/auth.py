from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import created_response, success_response
from app.domains.auth.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    Login,
    RefreshRequest,
    Register,
    ResetPasswordRequest,
    UpdateProfile,
    UserResponse,
    VerifyEmailRequest,
)
from app.domains.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service() -> AuthService:
    return AuthService()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/register", status_code=201)
def register(db: SessionDep, service: AuthServiceDep, data: Register):
    user = service.register(db, data)
    return created_response(UserResponse.model_validate(user), "User created successfully")


@router.post("/verify-email")
def verify_email(db: SessionDep, service: AuthServiceDep, data: VerifyEmailRequest):
    service.verify_email(db, data)
    return success_response(message="Email verified successfully")


@router.post("/login")
def login(db: SessionDep, service: AuthServiceDep, data: Login):
    token = service.login(db, data)
    return success_response(token, "Login successful")


@router.post("/refresh")
def refresh(service: AuthServiceDep, data: RefreshRequest):
    token = service.refresh(data)
    return success_response(token, "Token refreshed")


@router.post("/forgot-password")
def forgot_password(db: SessionDep, service: AuthServiceDep, data: ForgotPasswordRequest):
    service.forgot_password(db, data)
    return success_response(message="If the email exists, a reset link has been sent")


@router.post("/reset-password")
def reset_password(db: SessionDep, service: AuthServiceDep, data: ResetPasswordRequest):
    service.reset_password(db, data)
    return success_response(message="Password reset successfully")


@router.post("/logout")
def logout(current_user: CurrentUserDep):
    return success_response(message="Logout successful")


@router.patch("/profile")
def update_profile(
    db: SessionDep,
    service: AuthServiceDep,
    current_user: CurrentUserDep,
    data: UpdateProfile,
):
    user = service.update_profile(db, current_user, data)
    return success_response(UserResponse.model_validate(user), "Profile updated")


@router.post("/change-password")
def change_password(
    db: SessionDep,
    service: AuthServiceDep,
    current_user: CurrentUserDep,
    data: ChangePasswordRequest,
):
    service.change_password(db, current_user, data)
    return success_response(message="Password changed successfully")
