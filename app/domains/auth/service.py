import secrets
from datetime import datetime, timedelta
from typing import cast

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.core.logging_conf import logger
from app.core.security import (
    create_refresh_token,
    create_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.domains.auth.password import validate_password
from app.domains.auth.repository import UserRepository
from app.domains.auth.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    Login,
    RefreshRequest,
    Register,
    ResetPasswordRequest,
    TokenResponse,
    UpdateProfile,
    VerifyEmailRequest,
)
from db.models.user_model import Users


class AuthService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    def register(self, db: Session, data: Register) -> Users:
        validate_password(data.password)
        already = self.repo.find_by_email(db, data.email)
        if already:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already exists")
        verify_token = secrets.token_urlsafe(32)
        user = Users(
            email=data.email,
            password=hash_password(data.password),
            username=data.username,
            surname=data.surname,
            role="user",
            verify_token=verify_token,
        )
        created = self.repo.create(db, user)
        link = f"{settings.VERIFY_REDIRECT_URL}/api/v1/auth/verify-email?token={verify_token}"
        logger.info("Verify email: %s", link)
        return created

    def login(self, db: Session, data: Login) -> TokenResponse:
        user = self.repo.find_by_email(db, data.email)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not user.is_verified:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Email not verified")
        payload = {"sub": user.email, "role": user.role}
        access = create_token(data=payload)
        refresh = create_refresh_token(data=payload)
        return TokenResponse(access_token=access, refresh_token=refresh)

    def refresh(self, db: Session, data: RefreshRequest) -> TokenResponse:
        payload = decode_token(data.refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user = self.repo.find_by_email(db, email)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        if not user.is_verified:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Email not verified")
        user_payload = {"sub": user.email, "role": user.role}
        access = create_token(data=user_payload)
        refresh = create_refresh_token(data=user_payload)
        return TokenResponse(access_token=access, refresh_token=refresh)

    def change_password(
        self, db: Session, user: Users, data: ChangePasswordRequest
    ) -> None:
        if not verify_password(data.current_password, user.password):
            msg = "Current password is incorrect"
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=msg)
        validate_password(data.new_password)
        self.repo.update(db, cast(int, user.id), {"password": hash_password(data.new_password)})

    def update_profile(self, db: Session, user: Users, data: UpdateProfile) -> Users:
        updated = self.repo.update(db, cast(int, user.id), data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated

    def verify_email(self, db: Session, data: VerifyEmailRequest) -> None:
        user = db.exec(
            select(Users).where(Users.verify_token == data.token)
        ).first()
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid verification token")
        user.is_verified = True
        user.verify_token = None
        db.add(user)
        db.commit()

    def forgot_password(self, db: Session, data: ForgotPasswordRequest) -> None:
        user = self.repo.find_by_email(db, data.email)
        if not user:
            return
        token = secrets.token_urlsafe(32)
        expires = datetime.now() + timedelta(
            minutes=settings.RESET_TOKEN_EXPIRE_MINUTES
        )
        self.repo.update(db, cast(int, user.id), {
            "reset_token": token,
            "reset_token_expires": expires,
        })
        link = f"{settings.VERIFY_REDIRECT_URL}/api/v1/auth/reset-password?token={token}"
        logger.info("Reset password: %s", link)

    def reset_password(self, db: Session, data: ResetPasswordRequest) -> None:
        validate_password(data.new_password)
        user = db.exec(
            select(Users).where(Users.reset_token == data.token)
        ).first()
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
        if not user.reset_token_expires or user.reset_token_expires < datetime.now():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Reset token expired")
        self.repo.update(db, cast(int, user.id), {
            "password": hash_password(data.new_password),
            "reset_token": None,
            "reset_token_expires": None,
        })
