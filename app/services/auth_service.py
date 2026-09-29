from datetime import datetime, timezone
from uuid import UUID

import jwt
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.revoked_token_repository import RevokedTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserRequest


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AuthService:
    def __init__(self, users: UserRepository, revoked_tokens: RevokedTokenRepository):
        self.users = users
        self.revoked_tokens = revoked_tokens

    async def register(self, request: CreateUserRequest) -> User:
        email = request.email.lower()
        if await self.users.get_by_email(email):
            raise EmailAlreadyRegisteredError

        try:
            return await self.users.create(email, hash_password(request.password))
        except IntegrityError:
            # Outro request cadastrou o mesmo e-mail entre a checagem e o insert.
            await self.users.session.rollback()
            raise EmailAlreadyRegisteredError

    async def login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email.lower())
        if user is None:
            verify_password(password, DUMMY_PASSWORD_HASH)
            raise InvalidCredentialsError
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError

        return create_access_token(subject=str(user.id))

    async def get_current_user(self, token: str) -> User:
        payload = await self._decode_valid_token(token)
        user = await self.users.get_by_id(UUID(payload["sub"]))
        if user is None:
            raise InvalidTokenError
        return user

    async def logout(self, token: str) -> None:
        payload = await self._decode_valid_token(token)
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await self.revoked_tokens.revoke(payload["jti"], expires_at)

    async def _decode_valid_token(self, token: str) -> dict:
        try:
            payload = decode_access_token(token)
        except jwt.InvalidTokenError:
            raise InvalidTokenError

        if await self.revoked_tokens.is_revoked(payload["jti"]):
            raise InvalidTokenError
        return payload
