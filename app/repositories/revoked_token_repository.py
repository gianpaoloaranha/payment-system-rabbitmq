from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.revoked_token import RevokedToken


class RevokedTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_revoked(self, jti: str) -> bool:
        return await self.session.get(RevokedToken, jti) is not None

    async def revoke(self, jti: str, expires_at: datetime) -> None:
        self.session.add(RevokedToken(jti=jti, expires_at=expires_at))
        await self.session.commit()
