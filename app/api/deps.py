from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.security import decode_token
from app.database.engine import get_session
from app.domains.auth.repository import UserRepository
from db.models.user_model import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> Users:
    payload = decode_token(token=token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = UserRepository().find_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


CurrentUserDep = Annotated[Users, Depends(get_current_user)]


def get_current_admin_user(current_user: Users = Depends(get_current_user)) -> Users:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


AdminUserDep = Annotated[Users, Depends(get_current_admin_user)]
