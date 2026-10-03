from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_session
from app.models.user import User
from app.repositories.payment_repository import PaymentRepository
from app.repositories.revoked_token_repository import RevokedTokenRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService, InvalidTokenError
from app.services.payment_service import PaymentService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(UserRepository(session), RevokedTokenRepository(session))


def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(PaymentRepository(session))


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    try:
        return await service.get_current_user(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
